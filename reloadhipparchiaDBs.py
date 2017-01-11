# -*- coding: utf-8 -*-
# !../bin/python
"""
	HipparchiaServer: an interface to a database of Greek and Latin texts
	Copyright: E Gunderson 2016-17
	License: GNU GENERAL PUBLIC LICENSE 3
		(see LICENSE in the top level directory of the distribution)
"""

import pickle
import gzip
import os
import re
from dbhelpers import *
from multiprocessing import Process, Manager
from mpclass import MPCounter

config = configparser.ConfigParser()
config.read('config.ini')

datadir = config['io']['datadir'] + 'sqldumps/'

dbconnection = psycopg2.connect(user=config['db']['DBUSER'], host=config['db']['DBHOST'],
								port=config['db']['DBPORT'], database=config['db']['DBNAME'],
								password=config['db']['DBPASS'])

# dbconnection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cursor = dbconnection.cursor()


def retrievedb(location):
	"""
	decompress the data and get the db ready for reloading
	:param pickleddb:
	:param location:
	:return:
	"""

	f = gzip.open(location, 'rb')
	dbcontents = pickle.load(f)
	f.close()

	return dbcontents


def resetdb(dbname, structuremap, cursor):
	"""
	empty out a db and get it ready for reloaded data
	:param dbname:
	:param cursor:
	:return:
	"""

	query = 'DROP TABLE IF EXISTS public.' + dbname
	cursor.execute(query)
	dbconnection.commit()

	query = 'CREATE TABLE public.' + dbname + ' ('
	for column in structuremap:
		if column[0] == 'index':
			query += column[0] + ' ' + column[1] + ' DEFAULT nextval(\'' + dbname + '\'::regclass), '
		else:
			query += column[0] + ' ' + column[1] + ', '
	query = query[:-2] + ') WITH ( OIDS=FALSE );'
	cursor.execute(query)
	dbconnection.commit()

	if re.search(r'(gr|lt|in|dp|ch)\d\d\d\d', dbname) is not None:
		query = 'DROP INDEX IF EXISTS public.' + dbname + '_mu_trgm_idx'
		cursor.execute(query)
		dbconnection.commit()

		query = 'DROP INDEX IF EXISTS public.' + dbname + '_st_trgm_idx'
		cursor.execute(query)
		dbconnection.commit()

	query = 'GRANT SELECT ON TABLE ' + dbname + ' TO hippa_rd;'
	cursor.execute(query)
	dbconnection.commit()

	return


def reloadwhoeldb(dbcontents, cursor):
	"""
	the pickle package itself should tell you all you need to know to call reloadoneline() repeatedly
	note that the dbname is stored in the file and need not be derived from the filename itself
	:param dbcontents:
	:return:
	"""
	dbname = dbcontents['dbname']
	structure = dbcontents['structure']
	data = dbcontents['data']

	count = 0
	for line in data:
		count += 1
		# 32k is the limit?
		if count % 5000 == 0:
			dbconnection.commit()
		if count % 50000 == 0:
			print('\t\tlongdb: ', dbname, '[ @ line ', count, ']')
		reloadoneline(line, dbname, structure, cursor)

	dbconnection.commit()

	return


def reloadoneline(insertdata, dbname, dbstructurelist, cursor):
	"""
	restore everything to a db
	remember that the db itself should have pickled it structure
	and the values that came out then should still be tuples now
	:param dbname:
	:param cursor:
	:return:
	"""

	insertstring = ' ('
	insertvals = '('
	for label in dbstructurelist:
		insertstring += label[0] + ', '
		insertvals += '%s, '

	insertstring = insertstring[:-2] + ')'
	insertvals = insertvals[:-2] + ')'

	q = 'INSERT INTO ' + dbname + insertstring + ' VALUES ' + insertvals
	d = insertdata

	try:
		cursor.execute(q, d)
	except psycopg2.DatabaseError as e:
		print('insert into ', dbname, 'failed at while attempting', d)
		print('Error %s' % e)

	return


def buildfilesearchlist(datadir, memory):
	"""
	look down inside datadir and its subdirs for anything named *.pickle.gz
	obviously quite dangerous if you don't keep a close watch on the contents of those directories
	:param datadir:
	:return: a list of DirEntries
	"""

	suffix = '.pickle.gz'

	for entry in os.scandir(datadir):
		if entry.is_dir():
			buildfilesearchlist(entry.path, memory)
		elif suffix in entry.name:
			memory.append(entry)

	entries = []
	pickles = re.compile(r'\.pickle\.gz$')
	for m in memory:
		if re.search(pickles, m.path):
			entries.append(m)

	paths = []
	for e in entries:
		paths.append(e.path)

	return paths


def recursivereload(datadir):
	"""
	aim me at a directory and I will unpack all of the pickles and put them in the db
	:return:
	"""

	dbc = setconnection(config)
	cur = dbc.cursor()

	structuremap = {
		'authors': strauthors,
		'works': strworks,
		'greek_dictionary': strgreek_dictionary,
		'latin_dictionary': strlatin_dictionary,
		'greek_lemmata': strgreek_lemmata,
		'latin_lemmata': strlatin_lemmata,
		'greek_morphology': strgreek_morphology,
		'latin_morphology': strlatin_morphology,
		'builderversion': strbuilderversion
	}

	print('scanning the filesystem')
	dbpaths = buildfilesearchlist(datadir, [])
	totaldbs = len(dbpaths)

	print('dropping any old tables and creating new ones')

	authorfinder = re.compile(r'(gr|lt|in|dp|ch)\d\d\d\d$')
	for db in dbpaths:
		dbcontents = retrievedb(db)
		if dbcontents['dbname'] in structuremap:
			resetdb(dbcontents['dbname'], structuremap[dbcontents['dbname']], cur)
		elif re.search(authorfinder, dbcontents['dbname']):
			resetdb(dbcontents['dbname'], strindividual_authorfile, cur)
	dbc.commit()

	print('beginning to reload the databases:', totaldbs, 'found')
	manager = Manager()
	count = MPCounter()
	dbs = manager.list(dbpaths)
	workers = int(config['io']['workers'])

	jobs = [Process(target=mpreloader, args=(dbs, count, totaldbs)) for i in
			range(workers)]

	for j in jobs: j.start()
	for j in jobs: j.join()

	return


def mpreloader(dbs, count, totaldbs):
	"""
	mp reader reloader
	:return:
	"""
	authorfinder = re.compile(r'(gr|lt|in|dp|ch)\d\d\d\d$')

	dbc = setconnection(config)
	cur = dbc.cursor()

	while len(dbs) > 0:
		try:
			db = dbs.pop()
			dbcontents = retrievedb(db)
		except:
			dbcontents = {}
			dbcontents['dbname'] = ''

		count.increment()
		if count.value % 200 == 0:
			print('\t', str(count.value), 'of', str(totaldbs), 'databases restored')

		# print('loading',dbcontents['dbname'])

		if dbcontents['dbname'] != '':
			reloadwhoeldb(dbcontents, cur)

		if re.search(authorfinder, dbcontents['dbname']):
			query = 'CREATE INDEX ' + dbcontents['dbname'] + '_mu_trgm_idx ON public.' + dbcontents['dbname'] + \
					' USING gin (accented_line COLLATE pg_catalog."default" gin_trgm_ops)'
			cur.execute(query)
			dbc.commit()

			query = 'CREATE INDEX ' + dbcontents['dbname'] + '_st_trgm_idx ON public.' + dbcontents['dbname'] + \
					' USING gin (stripped_line COLLATE pg_catalog."default" gin_trgm_ops)'
			cur.execute(query)
			dbc.commit()

	dbc.commit()
	del dbc

	return


# everything
recursivereload(datadir)

# support only
# recursivereload(datadir+'/supportdbs/')

# gk only
# recursivereload(datadir+'/workdbs/greekauthors/')

# lt only
# recursivereload(datadir+'/workdbs/latinauthors/')