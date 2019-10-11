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

DROP INDEX public.greek_morphology_idx;
DROP INDEX public.greek_analysis_trgm_idx;
DROP TABLE public.greek_morphology;
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: greek_morphology; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE public.greek_morphology (
    observed_form character varying(64),
    xrefs character varying(128),
    prefixrefs character varying(128),
    possible_dictionary_forms text
);


ALTER TABLE public.greek_morphology OWNER TO hippa_wr;

--
-- Name: greek_analysis_trgm_idx; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE INDEX greek_analysis_trgm_idx ON public.greek_morphology USING gin (possible_dictionary_forms public.gin_trgm_ops);


--
-- Name: greek_morphology_idx; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE INDEX greek_morphology_idx ON public.greek_morphology USING btree (observed_form);


--
-- Name: TABLE greek_morphology; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE public.greek_morphology TO hippa_rd;


--
-- PostgreSQL database dump complete
--

