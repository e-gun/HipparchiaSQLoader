# dictionaries that tell you the SQL structure of the Hipparchia DBs
# in SQL dump:
#   find: [note 2 leading whitespaces]
#         (.*?)\s(.*?)(,|$)
#   replace:
#       \t('\1', '\2')\3

strauthors = [
	('universalid', 'character(6)'),
	('language', 'character varying(10)'),
	('idxname', 'character varying(128)'),
	('akaname', 'character varying(128)'),
	('shortname', 'character varying(128)'),
	('cleanname', 'character varying(128)'),
	('genres', 'character varying(512)'),
	('floruit', 'character varying(8)'),
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
	('wordcount', 'integer'),
	('authentic', 'boolean')
]

strindividual_work = [
	('index', 'integer NOT NULL'),
	('level_05_value', 'character varying(64)'),
	('level_04_value', 'character varying(64)'),
	('level_03_value', 'character varying(64)'),
	('level_02_value', 'character varying(64)'),
	('level_01_value', 'character varying(64)'),
	('level_00_value', 'character varying(64)'),
	('marked_up_line', 'text'),
	('stripped_line', 'text'),
	('hyphenated_words', 'character varying(128)'),
	('annotations', 'character varying(256)')
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



