# -*- coding: utf-8 -*-
"""
	HipparchiaServer: an interface to a database of Greek and Latin texts
	Copyright: E Gunderson 2016
	License: GNU GENERAL PUBLIC LICENSE 3
		(see LICENSE in the top level directory of the distribution)
"""

import psycopg2
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

sqltemplateversion = 12272016


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
	activecorporalist = []

	dbc = setconnection(config)
	cur = dbc.cursor()

	q = 'SELECT universalid FROM authors'
	cur.execute(q)
	ids = cur.fetchall()

	prefixes = set([id[0:2] for id in ids])

	dbc.commit()

	return activecorporaset

# dictionaries that tell you the SQL structure of the Hipparchia DBs

strauthors = [
	('universalid', 'character(6)'),
	('language', 'character varying(10)'),
	('idxname', 'character varying(128)'),
	('akaname', 'character varying(128)'),
	('shortname', 'character varying(128)'),
	('cleanname', 'character varying(128)'),
	('genres', 'character varying(512)'),
	('recorded_date', 'character varying(64)'),
	('converted_date', 'character varying(8)'),
	('location', 'character varying(128)')
]

strworks = [
	('universalid', 'character(10)'),
	('title', 'character varying(512)'),
	('language', 'character varying(10)'),
	('publication_info', 'text'),
	('levellabels_00', 'character varying(64)'),
	('levellabels_01', 'character varying(64)'),
	('levellabels_02', 'character varying(64)'),
	('levellabels_03', 'character varying(64)'),
	('levellabels_04', 'character varying(64)'),
	('levellabels_05', 'character varying(64)'),
	('workgenre', 'character varying(32)'),
	('transmission', 'character varying(32)'),
	('worktype', 'character varying(32)'),
	('provenance', 'character varying(64)'),
	('recorded_date', 'character varying(64)'),
	('converted_date', 'character varying(8)'),
	('wordcount', 'integer'),
	('firstline', 'integer'),
	('lastline', 'integer'),
	('authentic', 'boolean')
]

strindividual_authorfile = [
	('index', 'integer NOT NULL'),
	('wkuniversalid', 'character varying(10)'),
	('level_05_value', 'character varying(64)'),
	('level_04_value', 'character varying(64)'),
	('level_03_value', 'character varying(64)'),
	('level_02_value', 'character varying(64)'),
	('level_01_value', 'character varying(64)'),
	('level_00_value', 'character varying(64)'),
	('marked_up_line', 'text'),
	('accented_line', 'text'),
	('stripped_line', 'text'),
	('hyphenated_words', 'character varying(128)'),
	('annotations', 'character varying(256)')
]

strindividual_conc = [
	('word', 'character varying(128)'),
	('stripped_word', 'character varying(128)'),
	('loci', 'text')
]

#
# dictionaries, etc
#

strgreek_dictionary = [
	('entry_name', 'character varying(64)'),
	('unaccented_entry', 'character varying(64)'),
	('id_number', 'character varying(8)'),
	('entry_type', 'character varying(8)'),
	('entry_options', '"char"'),
	('entry_body', 'text')
]

strlatin_dictionary = [
	('entry_name', 'character varying(64)'),
	('id_number', 'character varying(8)'),
	('entry_type', 'character varying(8)'),
	('entry_key', 'character varying(64)'),
	('entry_options', '"char"'),
	('entry_body', 'text')
]

strgreek_lemmata = [
	('dictionary_entry', 'character varying(64)'),
	('xref_number', 'integer'),
	('derivative_forms', 'text')
]

strlatin_lemmata = [
	('dictionary_entry', 'character varying(64)'),
	('xref_number', 'integer'),
	('derivative_forms', 'text')
]

strgreek_morphology = [
	('observed_form', 'character varying(64)'),
	('possible_dictionary_forms', 'text')
]

strlatin_morphology = [
	('observed_form', 'character varying(64)'),
	('possible_dictionary_forms', 'text')
]


strbuilderversion = [
	('templateversion', 'integer'),
	('corpusname', 'character varying(2)'),
	('corpusbuilddate', 'character varying(20)')
]


