#!../bin/python
"""
	HipparchiaSQLoader: archive and restore a database of Greek and Latin texts
	Copyright: E Gunderson 2016-18
	License: GNU GENERAL PUBLIC LICENSE 3
		(see LICENSE in the top level directory of the distribution)
"""

import gzip
import io
import os
import pickle
from multiprocessing import Manager, Process

import psycopg2

from dbhelpers import *
from dbhelpers import MPCounter

config = configparser.ConfigParser()
config.read('config.ini')

datadir = config['io']['datadir'] + 'sqldumps/'
schemadir = config['io']['schemadir']
vectors = config['options']['archivevectors']


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


def resetdb(tablename, templatetablename, templatefilename, cursor):
	"""
	empty out a db and get it ready for reloaded data

	build the set of queries from the output of 'pgdump -c -s -t'

	:param dbname:
	:param cursor:
	:return:
	"""

	querylines = loadschemafromfile(tablename, templatetablename, templatefilename)
	querylines = [q for q in querylines if q and re.search(r'^--',q) is None]
	querylines = [re.sub(r'(ALTER|DROP) (TABLE|INDEX) ', r'\1 \2 IF EXISTS ', q) for q in querylines]

	corequery = [q for q in querylines
	             if re.search(r',$', q)
	             or re.search(r'CREATE TABLE', q)
	             or re.search(r'[^;]$', q)
	             or q == ');']

	othersql = list()
	for q in querylines:
		if re.search(r';$', q) and q not in corequery:
			othersql.append(q)
		else:
			othersql.append('padding')

	corequery = ' '.join(corequery)

	tablecreated = False

	for q in othersql:
		if q != 'padding':
			cursor.execute(q)

		elif tablecreated is False:
			cursor.execute(corequery)
			tablecreated = True
		else:
			pass

	return


def reloadwhoeldb(dbcontents, dbconnection):
	"""
	the pickle package itself should tell you all you need to know to call reloadoneline() repeatedly
	note that the dbname is stored in the file and need not be derived from the filename itself

	example:

	struct [('index', "integer DEFAULT nextval('public.gr0001'::regclass) NOT NULL"), ('wkuniversalid', 'character varying(10)'), ('level_05_value', 'character varying(64)'), ('level_04_value', 'character varying(64)'), ('level_03_value', 'character varying(64)'), ('level_02_value', 'character varying(64)'), ('level_01_value', 'character varying(64)'), ('level_00_value', 'character varying(64)'), ('marked_up_line', 'text'), ('accented_line', 'text'), ('stripped_line', 'text'), ('hyphenated_words', 'character varying(128)'), ('annotations', 'character varying(256)')]

	data[:4] [(1, 'lt9505w001', '-1', '-1', '-1', '-1', '-1', 't', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="hmu_title">INCERTI NOMINIS RELIQVIAE</span>', 'incerti nominis reliqviae', 'incerti nominis reliquiae', '', ''), (2, 'lt9505w001', '-1', '-1', '-1', '-1', '-1', '1', '<hmu_metadata_notes value="Serv. Dan. &3A.& 11.160" />uictrices', 'uictrices', 'uictrices', '', ''), (3, 'lt9505w001', '-1', '-1', '-1', '-1', '-1', '2', '<hmu_metadata_notes value="Quint. &3Inst.& 5.11.24" />Quis⟨nam⟩ íste torquens fáciem planipedís senis? <hmu_standalone_endofpage />', 'quisnam íste torquens fáciem planipedís senis ', 'quisnam iste torquens faciem planipedis senis ', '', ''), (4, 'lt9505w002', '-1', '-1', '-1', '-1', '-1', 't', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="hmu_title">INCERTI NOMINIS RELIQVIAE</span>', 'incerti nominis reliqviae', 'incerti nominis reliquiae', '', '')]

	:param dbcontents:
	:return:
	"""

	dbcursor = dbconnection.cursor()

	# there are tabs in the greek dictionary: you can't use '\t' as the separator
	# similarly you can't use a high-value junk separator because you are not allowed to use that many bits...
	separator = chr(7)

	table = dbcontents['dbname']
	structure = dbcontents['structure']
	data = dbcontents['data']

	# the problems
	# [a] *_lemmata
	#   psycopg2.DataError: malformed array literal: "['ζῳοτύπον', 'ζωιοτύποϲ']"
	#   DETAIL:  "[" must introduce explicitly-specified array dimensions.
	# [b] *_morphology
	#   [1] psycopg2.DataError: missing data for column "xrefs"
	#   [2] psycopg2.DataError: value too long for type character varying(64)
	# [c] authors and works
	#   psycopg2.DataError: invalid input syntax for integer: "None"
	#   CONTEXT:  COPY works, line 1, column converted_date: "None"
	# [d] unclear why ATM, but latin_dictionary will turn up empty...

	tests = ['lemmata', 'morphology', 'authors', 'works', 'latin_dictionary']
	avoidcopyfrom = [t for t in tests if t in table]

	if not avoidcopyfrom:
		columns = [s[0] for s in structure]
		stream = generatecopystream(data, separator=separator)
		dbcursor.copy_from(stream, table, sep=separator, columns=columns)
	else:
		dbconnection.setdefaultisolation()
		count = 1
		for line in data:
			count += 1
			# 32k is the limit?
			if count % 5000 == 0:
				dbconnection.commit()
			if count % 200000 == 0:
				print('\t\tlongdb: {t} [ @ line {c}]'.format(t=table, c=count))
			reloadoneline(line, table, structure, dbcursor)
		dbconnection.commit()
	return


def generatecopystream(queryvaluetuples, separator='\t'):
	"""
	postgres inserts much faster via "COPY FROM"
	prepare data to match the psychopg2.copy_from() interface
	copy_from(file, table, sep='\t', null='\\N', size=8192, columns=None)
		Read data from the file-like object file appending them to the table named table.
	see the example at http://initd.org/psycopg/docs/cursor.html:
		f = StringIO("42\tfoo\n74\tbar\n")
		cur.copy_from(f, 'test', columns=('num', 'data'))
	:param queryvaluetuples:
	:return:
	"""

	copystream = io.StringIO()

	for t in queryvaluetuples:
		copystream.write(separator.join([str(x) for x in t]) + '\n')

	copystream.seek(0)

	return copystream


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

	q = 'INSERT INTO {t} {i} VALUES {v}'.format(t=dbname, i=insertstring, v=insertvals)
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

	entries = list()
	pickles = re.compile(r'\.pickle\.gz$')
	for m in memory:
		if re.search(pickles, m.path):
			entries.append(m)

	paths = list()
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

	support = {'authors', 'works', 'greek_dictionary', 'latin_dictionary', 'greek_lemmata', 'latin_lemmata',
	             'greek_morphology', 'latin_morphology', 'builderversion', 'dictionary_headword_wordcounts',
	           'storedvectors', 'storedvectorimages'}

	if vectors != 'yes':
		support = support - {'storedvectors', 'storedvectorimages'}

	structures = dict()
	for item in support:
		structures[item] = loadcolumnsfromfile(schemadir+item+'_schema.sql')

	strwordcount = loadcolumnsfromfile(schemadir+'wordcounts_0_schema.sql')

	letters = '0abcdefghijklmnopqrstuvwxyzαβψδεφγηιξκλμνοπρϲτυωχθζ'

	for l in letters:
		structures['wordcounts_'+l] = strwordcount

	print('scanning the filesystem')
	dbpaths = buildfilesearchlist(datadir, [])
	totaldbs = len(dbpaths)

	print('dropping any old tables and creating new ones')

	authorfinder = re.compile(r'(gr|lt|in|dp|ch)\w\w\w\w$')

	count = 0
	for db in dbpaths:
		count += 1
		dbcontents = retrievedb(db)
		nm = dbcontents['dbname']
		if nm in structures and 'wordcounts_' not in nm:
			resetdb(nm, nm, schemadir+nm+'_schema.sql', cur)
		elif nm in structures and 'wordcounts_' in nm:
			resetdb(nm, 'wordcounts_0', schemadir+'wordcounts_0_schema.sql', cur)
		elif re.search(authorfinder, nm):
			resetdb(nm, 'gr0001', schemadir+'gr0001_schema.sql', cur)
		if count % 500 == 0:
			print('\t{c} tables reset'.format(c=count))
			dbc.commit()
	dbc.commit()

	print('beginning to reload the tables: {d} found'.format(d=totaldbs))
	print('[NB: the lengths vary considerably; not every 10% chunk will load as swiftly/slowly as did its peers...]')
	manager = Manager()
	count = MPCounter()
	dbs = manager.list(dbpaths)
	workers = int(config['io']['workers'])

	connections = {i: setconnection(autocommit=True) for i in range(workers)}

	jobs = [Process(target=mpreloader, args=(dbs, count, totaldbs, connections[i])) for i in range(workers)]

	for j in jobs:
		j.start()
	for j in jobs:
		j.join()

	for c in connections:
		connections[c].connectioncleanup()

	return


def mpreloader(dbs, count, totaldbs, dbconnection):
	"""
	mp reader reloader
	:return:
	"""

	progresschunks = int(totaldbs / 10)

	while len(dbs) > 0:
		try:
			db = dbs.pop()
			dbcontents = retrievedb(db)
		except IndexError:
			dbcontents = dict()
			dbcontents['dbname'] = ''

		count.increment()
		if count.value % progresschunks == 0:
			percent = round((count.value / totaldbs) * 100, 1)
			print('\t {p}% of the tables have been restored ({a}/{b})'.format(p=percent, a=count.value, b=totaldbs))

		if dbcontents['dbname'] != '':
			reloadwhoeldb(dbcontents, dbconnection)
			# unnestreloader(dbcontents)

	return


print('\n *** WARNING ***\n')
print('You are about to completely erase any currently installed data\n')
print('If "{d}" does not contain a full set of datafiles, HipparchiaServer will be sad and refuse to work properly, if at all.\n'.format(d=datadir))
areyousure = input('Type "YES" if you are sure you want to do this: ')

# everything

if areyousure == 'YES':
	# print('nuking')
	recursivereload(datadir)
else:
	print()
	print('"{x}" is not "YES"'.format(x=areyousure))
	print('Aborting. Current installation unmodified')

# support only
# recursivereload(datadir+'/supportdbs/')

# gk only
# recursivereload(datadir+'/workdbs/greekauthors/')

# lt only
# recursivereload(datadir+'/workdbs/latinauthors/')