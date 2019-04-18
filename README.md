***what***

moves HipparchiaDBs between the SQL system and the filesystem

current dump size for 5 corpora and support data:

    sqldumps/ $ du -h -d1
    774M	./authordbs
    101M	./supportdbs
    875M	.


***importing***

1. you acquire a set of `sqldump` files that can be read by `HipparchiaServer`
1. you install the more general software framework as per the `HipparchiaYOUROSTYPE` instructions/scripts
1. after `config.ini` has been properly edited to point to the `sqldump` files you can run `reloadhipparchiaDBs.py`:

```
    % cd ~/hipparchia_venv/HipparchiaSQLoader/
    % ./reloadhipparchiaDBs.py
    
```

***exporting***

1. you have an installed, configured and running copy of `HipparchiaServer`
1. optionally edit `config.ini` to point to where you want the `sqldump` files to end up. The default is inside `~/hipparchia_venv/HipparchiaData/sqldumps`
1. then you can run `extracthipparchiaDBs.py`:

```
    % cd ~/hipparchia_venv/HipparchiaSQLoader/
    % ./extracthipparchiaDBs.py
    
```

Little or no little editing of `config.ini` is required to load or extract a working set of data. You can get away with zero edits if you position the raw data in the default location
(i.e., in a subfolder named `sqldump` under `../HipparchiaData/`). 

If you do not know where/how to find `../HipparchiaData/` or `~/hipparchia_venv/HipparchiaData/`, you might have problems. You will need to learn the basics of how to read and edit file path names so that you know where to put/find things.
