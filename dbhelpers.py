# -*- coding: utf-8 -*-
"""
	HipparchiaSQLoader: archive and restore a database of Greek and Latin texts
	Copyright: E Gunderson 2016-17
	License: GNU GENERAL PUBLIC LICENSE 3
		(see LICENSE in the top level directory of the distribution)
"""

import re
import psycopg2
import configparser
from collections import deque

config = configparser.ConfigParser()
config.read('config.ini')

sqltemplateversion = 7242017


def setconnection(config):
	dbconnection = psycopg2.connect(user=config['db']['DBUSER'], host=config['db']['DBHOST'],
	                                port=config['db']['DBPORT'], database=config['db']['DBNAME'],
	                                password=config['db']['DBPASS'])
	# dbconnection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
	
	return dbconnection


def templatetest():
	"""

	make sure that HipparchiaSQLoader knows how to deal with the databases that are coming its way

	:return:
	"""

	dbc = setconnection(config)
	cur = dbc.cursor()

	q = 'SELECT templateversion FROM builderversion'
	cur.execute(q)
	versions = cur.fetchall()

	versions = set([x[0] for x in versions])

	compatible = 1
	version = sqltemplateversion

	for v in versions:
		if v != sqltemplateversion:
			version = v
			compatible = 0

	testresults = {compatible: version}

	return testresults


def knowncorpora():
	"""

	test for what is available

	return list of available dbs

	:return:
	"""

	dbc = setconnection(config)
	cur = dbc.cursor()

	q = 'SELECT universalid FROM authors'
	cur.execute(q)
	ids = cur.fetchall()
	ids = [x[0] for x in ids]
	prefixes = set([id[0:2] for id in ids])

	dbc.commit()

	return prefixes


def loadschemafromfile(tablename, templatetablename, filename):
	"""

	:param schemaname:
	:param filename:
	:return:
	"""

	with open(filename, 'rt') as s:
		fullschema = s.readlines()

	# do not name every work table 'gr0001' or every wordcount table 'wordcounts_0'
	fullschema = [re.sub(templatetablename, tablename, x) for x in fullschema]
	fullschema = [s.strip() for s in fullschema]

	return fullschema


def loadcolumnsfromfile(filename):
	"""
	find the core column structure from a set of schema lines

	return a set of tuples that associate the name of the column with its structure:
		... ('accented_line', 'text'), ('stripped_line', 'text'), ...

	:param schemalines:
	:return:
	"""

	with open(filename) as s:
		schemalines = s.readlines()
	schemalines = deque([s.strip() for s in schemalines])

	columnfinder = re.compile(r'CREATE TABLE', re.MULTILINE)

	# prune away the stuff that is on either side of 'CREATE TABLE ... ( ... );
	thisline = ''
	while re.search(columnfinder, thisline) is None:
		thisline = schemalines.popleft()

	columns = list()
	while re.search(r'^\);', thisline) is None:
		thisline = schemalines.popleft()
		columns.append(thisline)

	columns = columns[:-1]
	# now you have the core a list of items like 'wkuniversalid character varying(10),'
	columns = [re.sub(r',$', '', c) for c in columns]
	columns = [(c.split(' ')[0], ' '.join(c.split(' ')[1:])) for c in columns]

	return columns
