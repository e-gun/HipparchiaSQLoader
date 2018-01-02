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

# look out for the following getting split onto TWO lines. It needs to be on one:
#   ALTER TABLE ONLY gr0001 ADD CONSTRAINT gr0001_index_key UNIQUE (index);