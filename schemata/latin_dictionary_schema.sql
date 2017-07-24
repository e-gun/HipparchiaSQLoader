--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

DROP INDEX public.latin_dictionary_idx;
DROP TABLE public.latin_dictionary;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: latin_dictionary; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE latin_dictionary (
    entry_name character varying(64),
    metrical_entry character varying(64),
    id_number integer,
    entry_type character varying(8),
    entry_key character varying(64),
    entry_options "char",
    translations text,
    entry_body text
);


ALTER TABLE latin_dictionary OWNER TO hippa_wr;

--
-- Name: latin_dictionary_idx; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE INDEX latin_dictionary_idx ON latin_dictionary USING btree (entry_name);


--
-- Name: latin_dictionary; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE latin_dictionary TO hippa_rd;


--
-- PostgreSQL database dump complete
--

