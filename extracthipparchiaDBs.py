#!../bin/python
"""
	HipparchiaSQLoader: archive and restore a database of Greek and Latin texts
	Copyright: E Gunderson 2016-18
	License: GNU GENERAL PUBLIC LICENSE 3
		(see LICENSE in the top level directory of the distribution)
"""

import gzip
import os
import pickle
import psycopg2
from multiprocessing import Manager, Process, freeze_support

from dbhelpers import *
from dbhelpers import MPCounter
from workers import setworkercount

config = configparser.ConfigParser()
config.read('config.ini')

datadir = config['io']['datadir']+'sqldumps/'
schemadir = config['io']['schemadir']
vectors = config['options']['archivevectors']


def fetchit(dbname, dbstructurelist, cursor):
	"""

	pull everything from a db

	:param dbname:
	:param dbstructurelist:
	:param cursor:
	:return:
	"""

	selectlist = [label[0] for label in dbstructurelist]
	selectstring = ','.join(selectlist)
	
	q = 'SELECT {s} FROM {d}'.format(s=selectstring, d=dbname)
	try:
		cursor.execute(q)
		results = cursor.fetchall()
	except psycopg2.ProgrammingError:
		results = None

	return results


def pickleprep(dbname, dbstructurelist, dbcontents):
	"""
	take the fetchaller results and pickle them
	:param dbname:
	:param dbstructurelist:
	:param dbcontents:
	:return:
	"""

	pickleddb = dict()
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
	
	f = gzip.open(location, 'wb')
	pickle.dump(pickleddb, f, pickle.HIGHEST_PROTOCOL)
	f.close()
	
	return


def archivesupportdbs(location):
	"""
	take all of the non-work dbs and store them
	
	:return:
	"""

	dbconnection = setconnection()
	dbcursor = dbconnection.cursor()

	intermediatedir = 'supportdbs/'
	if not os.path.exists(location + intermediatedir):
		os.makedirs(location+intermediatedir)
		
	suffix = '.pickle.gz'

	support = {'authors', 'works', 'greek_dictionary', 'latin_dictionary', 'greek_lemmata', 'latin_lemmata',
	             'greek_morphology', 'latin_morphology', 'builderversion', 'dictionary_headword_wordcounts',
	           'storedvectors', 'storedvectorimages'}

	if vectors != 'yes':
		support = support - {'storedvectors', 'storedvectorimages'}

	dbs = dict()
	for item in support:
		dbs[item] = loadcolumnsfromfile(schemadir+item+'_schema.sql')

	strwordcount = loadcolumnsfromfile(schemadir+'wordcounts_0_schema.sql')

	letters = '0abcdefghijklmnopqrstuvwxyzαβψδεφγηιξκλμνοπρϲτυωχθζ'

	for l in letters:
		dbs['wordcounts_'+l] = strwordcount

	for db in dbs:
		dbcontents = fetchit(db, dbs[db], dbcursor)
		dbconnection.commit()
		if dbcontents:
			pickleddb = pickleprep(db, dbs[db], dbcontents)
			storeit(location+intermediatedir+db+suffix, pickleddb)

	dbconnection.connectioncleanup()
	
	return


def archivesingleauthor(db, structure, location, cursor):
	"""

	pickle and save a single work

	:param db:
	:param structure:
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


def archiveallauthors(location, authordbstructure):
	"""
	search for the lot of them and then do it
	:param location:
	:param cursor:
	:return:
	"""

	dbconnection = setconnection(config)
	dbcursor = dbconnection.cursor()

	intermediatedir = 'authordbs/'
	if not os.path.exists(location + intermediatedir):
		os.makedirs(location+intermediatedir)

	coprora = knowncorpora()

	for c in coprora:
		if not os.path.exists(location + intermediatedir + c):
			os.makedirs(location + intermediatedir + c)

	# a more interesting set of queries could output things like 5th c prose
	q = 'SELECT universalid FROM authors ORDER BY universalid'
	dbcursor.execute(q)
	authorids = dbcursor.fetchall()
	authorids = [a[0] for a in authorids]
	dbconnection.commit()

	manager = Manager()
	count = MPCounter()
	authors = manager.list(authorids)
	workers = setworkercount()

	connections = {i: setconnection() for i in range(workers)}

	print(len(authorids), 'author databases to extract')

	jobs = [Process(target=mpauthorarchiver, args=(count, location, intermediatedir, authordbstructure, authors, connections[i])) for i in
	        range(workers)]
	
	for j in jobs:
		j.start()
	for j in jobs:
		j.join()

	for c in connections:
		connections[c].connectioncleanup()

	return


def mpauthorarchiver(count, location, intermediatedir, authordbstructure, authors, dbconnection):
	"""
	share the archiving work

	:param count:
	:param location:
	:param intermediatedir:
	:param authordbstructure:
	:param authors:
	:return:
	"""

	dbcursor = dbconnection.cursor()
	
	while len(authors) > 0:
		try:
			au = authors.pop()
		except IndexError:
			au = 'gr0000'

		langdir = location + intermediatedir
		if not os.path.exists(langdir + au[0:2] + '/' + au[0:4] + '/'):
			try:
				os.makedirs(langdir + au[0:2] + '/' + au[0:4] + '/')
			except FileExistsError:
				# FileExistsError: [Errno 17] File exists:
				# MP means a race to create
				pass
		dbloc = langdir + au[0:2] + '/' + au[0:4] + '/'

		if au != 'gr0000':
			archivesingleauthor(au, authordbstructure, dbloc, dbcursor)

		dbconnection.commit()

		count.increment()
		if count.value % 250 == 0:
			print('\t', str(count.value) + ' databases extracted')

	dbconnection.commit()

	return


if __name__ == '__main__':
	freeze_support()
	testresults = templatetest()
	if 0 in testresults:
		print('aborting:', testresults[0], 'is not a DB version I can extract')
	else:
		print('archiving support dbs')
		archivesupportdbs(datadir)

		print('archiving individual authorfiles')
		strindividual_authorfile = loadcolumnsfromfile(schemadir+'gr0001_schema.sql')
		archiveallauthors(datadir, strindividual_authorfile)
