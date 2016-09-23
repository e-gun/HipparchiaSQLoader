# -*- coding: utf-8 -*-
#!../bin/python
import psycopg2
import configparser
import pickle
import gzip
import time
import os
import re
from dbstructures import *

config = configparser.ConfigParser()
config.read('config.ini')

datadir = config['io']['datadir']+'sqldumps/'


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
			query += column[0]+' '+column[1]+' DEFAULT nextval(\'' + dbname + '\'::regclass), '
		else:
			query += column[0] + ' ' + column[1] + ', '
	query = query[:-2] + ') WITH ( OIDS=FALSE );'
	cursor.execute(query)
	
	query = 'GRANT SELECT ON TABLE ' + dbname + ' TO hippa_rd;'
	cursor.execute(query)
	
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
		if count % 20000 == 0:
			dbconnection.commit()
			print('largedb:',dbname,'\n\tcommitting at',count)
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
		insertvals	+= '%s, '
	
	insertstring = insertstring[:-2] + ')'
	insertvals = insertvals[:-2] + ')'
	
	q = 'INSERT INTO ' + dbname + insertstring + ' VALUES ' + insertvals
	d = insertdata
	
	try:
		cursor.execute(q,d)
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
		if re.search(pickles,m.path):
			entries.append(m)
	
	return entries


def recursivereload(datadir, cursor):
	"""
	aim me at a directory and I will unpack all of the pickles and put them in the db
	:param cursor:
	:return:
	"""
	structuremap = {
		'authors': strauthors,
		'works': strworks,
		'greek_dictionary': strgreek_dictionary,
		'latin_dictionary': strlatin_dictionary,
		'greek_lemmata': strgreek_lemmata,
		'latin_lemmata': strlatin_lemmata,
		'greek_morphology': strgreek_morphology,
		'latin_morphology': strlatin_morphology
		}
	
	workfinder = re.compile(r'(gr|lt)\d\d\d\dw\d\d\d')

	dbs = buildfilesearchlist(datadir,[])
	
	count = 0
	for db in dbs:
		count += 1
		if count % 250 == 0:
			print(str(count),'of',str(len(dbs)),'databases restored')
		
		dbcontents = retrievedb(db.path)
		
		if dbcontents['dbname'] in structuremap:
			resetdb(dbcontents['dbname'], structuremap[dbcontents['dbname']], cursor)
		elif re.search(workfinder,dbcontents['dbname']):
			resetdb(dbcontents['dbname'], strindividual_work, cursor)
		
		reloadwhoeldb(dbcontents, cursor)
	
	return


# everything
recursivereload(datadir, cursor)

# support only
# recursivereload(datadir+'/supportdbs/', cursor)

# gk only
# recursivereload(datadir+'/workdbs/greekauthors/', cursor)

# lt only
# recursivereload(datadir+'/workdbs/latinauthors/', cursor)