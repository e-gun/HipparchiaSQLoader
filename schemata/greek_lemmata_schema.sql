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

DROP INDEX public.greek_lemmata_idx;
DROP TABLE public.greek_lemmata;
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: greek_lemmata; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE public.greek_lemmata (
    dictionary_entry character varying(64),
    xref_number integer,
    derivative_forms text[]
);


ALTER TABLE public.greek_lemmata OWNER TO hippa_wr;

--
-- Name: greek_lemmata_idx; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE INDEX greek_lemmata_idx ON public.greek_lemmata USING btree (dictionary_entry);


--
-- Name: TABLE greek_lemmata; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE public.greek_lemmata TO hippa_rd;


--
-- PostgreSQL database dump complete
--

