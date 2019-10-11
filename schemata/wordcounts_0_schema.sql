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

DROP INDEX public.wcindex_0;
DROP TABLE public.wordcounts_0;
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: wordcounts_0; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE public.wordcounts_0 (
    entry_name character varying(64),
    total_count integer DEFAULT 0,
    gr_count integer DEFAULT 0,
    lt_count integer DEFAULT 0,
    dp_count integer DEFAULT 0,
    in_count integer DEFAULT 0,
    ch_count integer DEFAULT 0
);


ALTER TABLE public.wordcounts_0 OWNER TO hippa_wr;

--
-- Name: wcindex_0; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE UNIQUE INDEX wcindex_0 ON public.wordcounts_0 USING btree (entry_name);


--
-- Name: TABLE wordcounts_0; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE public.wordcounts_0 TO hippa_rd;


--
-- PostgreSQL database dump complete
--

