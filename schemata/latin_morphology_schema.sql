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

DROP INDEX public.latin_morphology_idx;
DROP INDEX public.latin_analysis_trgm_idx;
DROP TABLE public.latin_morphology;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: latin_morphology; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE latin_morphology (
    observed_form character varying(64),
    xrefs character varying(128),
    prefixrefs character varying(128),
    possible_dictionary_forms text
);


ALTER TABLE latin_morphology OWNER TO hippa_wr;

--
-- Name: latin_analysis_trgm_idx; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE INDEX latin_analysis_trgm_idx ON latin_morphology USING gin (possible_dictionary_forms gin_trgm_ops);


--
-- Name: latin_morphology_idx; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE INDEX latin_morphology_idx ON latin_morphology USING btree (observed_form);


--
-- Name: latin_morphology; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE latin_morphology TO hippa_rd;


--
-- PostgreSQL database dump complete
--

