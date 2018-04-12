--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP INDEX public.wcindexts;
DROP TABLE public.dictionary_headword_wordcounts;
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: dictionary_headword_wordcounts; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE public.dictionary_headword_wordcounts (
    entry_name character varying(64),
    total_count integer,
    gr_count integer,
    lt_count integer,
    dp_count integer,
    in_count integer,
    ch_count integer,
    frequency_classification character varying(64),
    early_occurrences integer,
    middle_occurrences integer,
    late_occurrences integer,
    acta integer,
    agric integer,
    alchem integer,
    anthol integer,
    apocalyp integer,
    apocryph integer,
    apol integer,
    astrol integer,
    astron integer,
    biogr integer,
    bucol integer,
    caten integer,
    chronogr integer,
    comic integer,
    comm integer,
    concil integer,
    coq integer,
    dialog integer,
    docu integer,
    doxogr integer,
    eccl integer,
    eleg integer,
    encom integer,
    epic integer,
    epigr integer,
    epist integer,
    evangel integer,
    exeget integer,
    fab integer,
    geogr integer,
    gnom integer,
    gramm integer,
    hagiogr integer,
    hexametr integer,
    hist integer,
    homilet integer,
    hymn integer,
    hypoth integer,
    iamb integer,
    ignotum integer,
    invectiv integer,
    inscr integer,
    jurisprud integer,
    lexicogr integer,
    liturg integer,
    lyr integer,
    magica integer,
    math integer,
    mech integer,
    med integer,
    metrolog integer,
    mim integer,
    mus integer,
    myth integer,
    narrfict integer,
    nathist integer,
    onir integer,
    orac integer,
    orat integer,
    paradox integer,
    parod integer,
    paroem integer,
    perieg integer,
    phil integer,
    physiognom integer,
    poem integer,
    polyhist integer,
    prophet integer,
    pseudepigr integer,
    rhet integer,
    satura integer,
    satyr integer,
    schol integer,
    tact integer,
    test integer,
    theol integer,
    trag integer
);


ALTER TABLE public.dictionary_headword_wordcounts OWNER TO hippa_wr;

--
-- Name: wcindexts; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE UNIQUE INDEX wcindexts ON public.dictionary_headword_wordcounts USING btree (entry_name);


--
-- Name: TABLE dictionary_headword_wordcounts; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE public.dictionary_headword_wordcounts TO hippa_rd;


--
-- PostgreSQL database dump complete
--

