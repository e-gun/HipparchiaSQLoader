--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5
-- Dumped by pg_dump version 11.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
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
    total_count integer DEFAULT 0,
    gr_count integer DEFAULT 0,
    lt_count integer DEFAULT 0,
    dp_count integer DEFAULT 0,
    in_count integer DEFAULT 0,
    ch_count integer DEFAULT 0,
    frequency_classification character varying(64),
    early_occurrences integer DEFAULT 0,
    middle_occurrences integer DEFAULT 0,
    late_occurrences integer DEFAULT 0,
    acta integer DEFAULT 0,
    agric integer DEFAULT 0,
    alchem integer DEFAULT 0,
    anthol integer DEFAULT 0,
    apocalyp integer DEFAULT 0,
    apocryph integer DEFAULT 0,
    apol integer DEFAULT 0,
    astrol integer DEFAULT 0,
    astron integer DEFAULT 0,
    biogr integer DEFAULT 0,
    bucol integer DEFAULT 0,
    caten integer DEFAULT 0,
    chronogr integer DEFAULT 0,
    comic integer DEFAULT 0,
    comm integer DEFAULT 0,
    concil integer DEFAULT 0,
    coq integer DEFAULT 0,
    dialog integer DEFAULT 0,
    docu integer DEFAULT 0,
    doxogr integer DEFAULT 0,
    eccl integer DEFAULT 0,
    eleg integer DEFAULT 0,
    encom integer DEFAULT 0,
    epic integer DEFAULT 0,
    epigr integer DEFAULT 0,
    epist integer DEFAULT 0,
    evangel integer DEFAULT 0,
    exeget integer DEFAULT 0,
    fab integer DEFAULT 0,
    geogr integer DEFAULT 0,
    gnom integer DEFAULT 0,
    gramm integer DEFAULT 0,
    hagiogr integer DEFAULT 0,
    hexametr integer DEFAULT 0,
    hist integer DEFAULT 0,
    homilet integer DEFAULT 0,
    hymn integer DEFAULT 0,
    hypoth integer DEFAULT 0,
    iamb integer DEFAULT 0,
    ignotum integer DEFAULT 0,
    invectiv integer DEFAULT 0,
    inscr integer DEFAULT 0,
    jurisprud integer DEFAULT 0,
    lexicogr integer DEFAULT 0,
    liturg integer DEFAULT 0,
    lyr integer DEFAULT 0,
    magica integer DEFAULT 0,
    math integer DEFAULT 0,
    mech integer DEFAULT 0,
    med integer DEFAULT 0,
    metrolog integer DEFAULT 0,
    mim integer DEFAULT 0,
    mus integer DEFAULT 0,
    myth integer DEFAULT 0,
    narrfict integer DEFAULT 0,
    nathist integer DEFAULT 0,
    onir integer DEFAULT 0,
    orac integer DEFAULT 0,
    orat integer DEFAULT 0,
    paradox integer DEFAULT 0,
    parod integer DEFAULT 0,
    paroem integer DEFAULT 0,
    perieg integer DEFAULT 0,
    phil integer DEFAULT 0,
    physiognom integer DEFAULT 0,
    poem integer DEFAULT 0,
    polyhist integer DEFAULT 0,
    prophet integer DEFAULT 0,
    pseudepigr integer DEFAULT 0,
    rhet integer DEFAULT 0,
    satura integer DEFAULT 0,
    satyr integer DEFAULT 0,
    schol integer DEFAULT 0,
    tact integer DEFAULT 0,
    test integer DEFAULT 0,
    theol integer DEFAULT 0,
    trag integer DEFAULT 0
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

