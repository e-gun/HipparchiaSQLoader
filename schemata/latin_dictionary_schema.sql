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

DROP INDEX public.latin_dictionary_idx;
DROP TABLE public.latin_dictionary;
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: latin_dictionary; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE public.latin_dictionary (
    entry_name character varying(256),
    metrical_entry character varying(256),
    id_number real,
    entry_key character varying(64),
    pos character varying(64),
    translations text,
    entry_body text
);


ALTER TABLE public.latin_dictionary OWNER TO hippa_wr;

--
-- Name: latin_dictionary_idx; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE INDEX latin_dictionary_idx ON public.latin_dictionary USING btree (entry_name);


--
-- Name: TABLE latin_dictionary; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE public.latin_dictionary TO hippa_rd;


--
-- PostgreSQL database dump complete
--

