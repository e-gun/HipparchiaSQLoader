--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

DROP INDEX public.wcindexts;
DROP TABLE public.dictionary_headword_wordcounts;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: dictionary_headword_wordcounts; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE dictionary_headword_wordcounts (
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
    late_occurrences integer
);


ALTER TABLE dictionary_headword_wordcounts OWNER TO hippa_wr;

--
-- Name: wcindexts; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE UNIQUE INDEX wcindexts ON dictionary_headword_wordcounts USING btree (entry_name);


--
-- Name: dictionary_headword_wordcounts; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE dictionary_headword_wordcounts TO hippa_rd;


--
-- PostgreSQL database dump complete
--

