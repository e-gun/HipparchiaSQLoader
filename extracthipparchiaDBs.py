# -*- coding: utf-8 -*-
#!../bin/python
"""
	HipparchiaSQLoader: archive/restore a database of Greek and Latin texts
	Copyright: E Gunderson 2016
	License: GPL 3 (see LICENSE in the top level directory of the distribution)
"""

import pickle
import gzip
import os
from dbhelpers import *
from multiprocessing import Process, Manager
from mpclass import MPCounter


config = configparser.ConfigParser()
config.read('config.ini')

datadir = config['io']['datadir']+'sqldumps/'

dbconnection = psycopg2.connect(user=config['db']['DBUSER'], host=config['db']['DBHOST'],
                                port=config['db']['DBPORT'], database=config['db']['DBNAME'],
                                password=config['db']['DBPASS'])
cursor = dbconnection.cursor()

def fetchit(dbname, dbstructurelist, cursor):
	"""
	pull everything from a db
	:param dbname:
	:param cursor:
	:return:
	"""
	
	
	slectstring = ''
	for label in dbstructurelist:
		slectstring += label[0]+','
	slectstring = slectstring[:-1]
	
	q = 'SELECT '+slectstring+' from '+dbname
	cursor.execute(q)
	results = cursor.fetchall()

	return results


def pickleprep(dbname, dbstructurelist, dbcontents):
	"""
	take the fetchaller results and pickle them
	:param dbname:
	:return:
	"""
	pickleddb = {}
	pickleddb['dbname'] = dbname
	pickleddb['structure'] = dbstructurelist
	pickleddb['data'] = dbcontents
	
	return pickleddb


def storeit(location, pickleddb):
	"""
	compress the data and tuck the db away
	:param pickleddb:
	:param location:
	:return:
	"""

	#with open(location, 'wb') as f:
	#	pickle.dump(pickleddb, f)
	
	f = gzip.open(location,'wb')
	pickle.dump(pickleddb, f, pickle.HIGHEST_PROTOCOL)
	f.close()
	
	return


def archivesupportdbs(location,cursor):
	"""
	take all of the non-work dbs and store them
	
	:return:
	"""
	intermediatedir = 'supportdbs/'
	if not os.path.exists(location + intermediatedir):
		os.makedirs(location+intermediatedir)
		
	suffix = '.pickle.gz'
	
	# map the names to the varaibles containing their structures
	dbs = {'authors': strauthors,
	       'works': strworks,
	       'greek_dictionary': strgreek_dictionary,
	       'latin_dictionary': strlatin_dictionary,
	       'greek_lemmata': strgreek_lemmata,
	       'latin_lemmata': strlatin_lemmata,
	       'greek_morphology': strgreek_morphology,
	       'latin_morphology': strlatin_morphology
	       }
	for db in dbs:
		dbcontents = fetchit(db,dbs[db],cursor)
		pickleddb = pickleprep(db, dbs[db], dbcontents)
		storeit(location+intermediatedir+db+suffix,pickleddb)
	
	return


def archivesinglework(db, structure, location, cursor):
	"""
	pickle and save a single work
	:param location:
	:param cursor:
	:return:
	"""

	suffix = '.pickle.gz'
	# suffix = '.pickle'
	
	dbcontents = fetchit(db, structure, cursor)
	pickleddb = pickleprep(db, structure, dbcontents)
	storeit(location + db + suffix, pickleddb)
	
	return


def archiveallworks(location, workstructure, cursor):
	"""
	search for the lot of them and then do it
	:param location:
	:param cursor:
	:return:
	"""
	
	intermediatedir = 'workdbs/'
	if not os.path.exists(location + intermediatedir):
		os.makedirs(location+intermediatedir)
	
	if not os.path.exists(location + intermediatedir + 'greekauthors/'):
		os.makedirs(location + intermediatedir + 'greekauthors/')
	
	if not os.path.exists(location + intermediatedir + 'latinauthors/'):
		os.makedirs(location + intermediatedir + 'latinauthors/')
	
	# a more interesting set of queries could output things like 5th c prose
	q = 'SELECT universalid FROM authors ORDER BY universalid'
	cursor.execute(q)
	authorids = cursor.fetchall()
	
	manager = Manager()
	count = MPCounter()
	authors = manager.list(authorids)
	workers = int(config['io']['workers'])
	
	jobs = [Process(target=mpauthorarchiver, args=(count, location, intermediatedir, workstructure, authors)) for i in
	        range(workers)]
	
	for j in jobs: j.start()
	for j in jobs: j.join()
	
	return


def mpauthorarchiver(count, location, intermediatedir, workstructure, authors):
	"""
	share the archiving work
	:param authorlist:
	:return:
	"""
	
	dbc = setconnection(config)
	cur = dbc.cursor()
	
	while len(authors) > 0:
		try: a = authors.pop()
		except: a = ('gr0000',)
		q = 'SELECT universalid FROM works WHERE universalid LIKE %s ORDER BY universalid'
		d = (a[0] + '%',)
		cur.execute(q, d)
		works = cur.fetchall()
		if a[0][0:2] == 'gr':
			langdir = location + intermediatedir + 'greekauthors/'
		else:
			langdir = location + intermediatedir + 'latinauthors/'
		
		for w in works:
			count.increment()
			if count.value % 250 == 0:
				print(str(count.value) + ' databases extracted')
			if not os.path.exists(langdir + a[0] + '/'):
				os.makedirs(langdir + a[0] + '/')
			dbloc = langdir + a[0] + '/'
			archivesinglework(w[0], workstructure, dbloc, cur)
			dbc.commit()

	dbc.commit()
	del dbc
	
	return

print('archiving support dbs')
archivesupportdbs(datadir,cursor)

print('archiving individual works')
archiveallworks(datadir, strindividual_work, cursor)