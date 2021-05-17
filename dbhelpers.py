# -*- coding: utf-8 -*-
"""
	HipparchiaSQLoader: archive and restore a database of Greek and Latin texts
	Copyright: E Gunderson 2016-18
	License: GNU GENERAL PUBLIC LICENSE 3
		(see LICENSE in the top level directory of the distribution)
"""

import configparser
import re
from collections import deque
from multiprocessing import Value, Process
from os import name as osname

from connection import setconnection, ConnectionObject

config = configparser.ConfigParser()
config.read('config.ini')

sqltemplateversion = 10082019


def icanpickleconnections():
	result = True
	c = (ConnectionObject(),)
	j = Process(target=type, args=c)

	try:
		j.start()
		j.join()
	except TypeError:
		# can't pickle psycopg2.extensions.connection objects
		print('to avoid seeing "EOFError: Ran out of input" messages edit "settings/networksettings.py" to read:')
		print("\tICANPICKLECONNECTIONS = 'n'\n")
		result = False
	c[0].connectioncleanup()

	return result


def templatetest():
	"""

	make sure that HipparchiaSQLoader knows how to deal with the databases that are coming its way

	:return:
	"""

	dbc = setconnection()
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

	dbc.connectioncleanup()

	return testresults


def knowncorpora():
	"""

	test for what is available

	return list of available dbs

	:return:
	"""

	dbc = setconnection()
	cur = dbc.cursor()

	q = 'SELECT universalid FROM authors'
	cur.execute(q)
	ids = cur.fetchall()
	ids = [x[0] for x in ids]
	prefixes = set([id[0:2] for id in ids])

	dbc.connectioncleanup()

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


class MPCounter(object):
	def __init__(self):
		self.val = Value('i', 0)

	def increment(self, n=1):
		with self.val.get_lock():
			self.val.value += n

	@property
	def value(self):
		return self.val.value