--
-- PostgreSQL database dump
--

-- Dumped from database version 10.1
-- Dumped by pg_dump version 10.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

DROP TABLE public.wordcounts_0;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: wordcounts_0; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE wordcounts_0 (
    entry_name character varying(64),
    total_count integer,
    gr_count integer,
    lt_count integer,
    dp_count integer,
    in_count integer,
    ch_count integer
);


ALTER TABLE wordcounts_0 OWNER TO hippa_wr;

--
-- Name: wordcounts_0; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE wordcounts_0 TO hippa_rd;


--
-- PostgreSQL database dump complete
--

