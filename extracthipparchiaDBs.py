# -*- coding: utf-8 -*-
#!../bin/python
import psycopg2
import configparser
import pickle
import gzip
import os
from dbstructures import *

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
	
	q = 'SELECT universalid FROM authors ORDER BY universalid'
	cursor.execute(q)
	authors = cursor.fetchall()
	
	count = 0
	
	for a in authors:
		# a more interesting query could output things like 5th c prose
		q = 'SELECT universalid FROM works WHERE universalid LIKE %s ORDER BY universalid'
		d = (a[0]+'%',)
		cursor.execute(q,d)
		works = cursor.fetchall()
		if a[0][0:2] == 'gr':
			langdir = location + intermediatedir + 'greekauthors/'
		else:
			langdir = location + intermediatedir + 'latinauthors/'
	
		for w in works:
			count += 2
			if count % 250 == 0:
				print(str(count)+' databases extracted')
			if not os.path.exists(langdir+a[0]+'/'):
				os.makedirs(langdir+a[0]+'/')
			dbloc = langdir+a[0]+'/'
			archivesinglework(w[0], workstructure, dbloc, cursor)
			dbconnection.commit()

	return

archivesupportdbs(datadir,cursor)
archiveallworks(datadir, strindividual_work, cursor)