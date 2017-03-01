#!/bin/bash

DB="hipparchiaDB"
PGDUMP="/usr/local/bin/pg_dump"
OUTDIR="./schemata/"

if [ ! -d $OUTDIR ]; then
	/bin/mkdir $OUTDIR
fi

for table in authors gr0001 builderversion dictionary_headword_wordcounts greek_dictionary greek_lemmata greek_morphology latin_dictionary latin_lemmata latin_morphology wordcounts_0 works
do 
	$PGDUMP -c -s -t $table $DB > $OUTDIR/${table}_schema.sql
done