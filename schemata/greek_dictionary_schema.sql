--
-- PostgreSQL database dump
--

-- Dumped from database version 10.2
-- Dumped by pg_dump version 10.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

DROP INDEX public.greek_dictionary_idx;
DROP TABLE public.greek_dictionary;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: greek_dictionary; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE greek_dictionary (
    entry_name character varying(64),
    metrical_entry character varying(64),
    unaccented_entry character varying(64),
    id_number integer,
    pos character varying(64),
    translations text,
    entry_body text
);


ALTER TABLE greek_dictionary OWNER TO hippa_wr;

--
-- Name: greek_dictionary_idx; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE INDEX greek_dictionary_idx ON greek_dictionary USING btree (entry_name);


--
-- Name: TABLE greek_dictionary; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE greek_dictionary TO hippa_rd;


--
-- PostgreSQL database dump complete
--

