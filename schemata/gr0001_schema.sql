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

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: gr0001; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE gr0001 (
    index integer DEFAULT nextval('gr0001'::regclass) NOT NULL,
    wkuniversalid character varying(10),
    level_05_value character varying(64),
    level_04_value character varying(64),
    level_03_value character varying(64),
    level_02_value character varying(64),
    level_01_value character varying(64),
    level_00_value character varying(64),
    marked_up_line text,
    accented_line text,
    stripped_line text,
    hyphenated_words character varying(128),
    annotations character varying(256)
);


ALTER TABLE gr0001 OWNER TO hippa_wr;

--
-- Name: gr0001_mu_trgm_idx; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE INDEX gr0001_mu_trgm_idx ON gr0001 USING gin (accented_line gin_trgm_ops);


--
-- Name: gr0001_st_trgm_idx; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE INDEX gr0001_st_trgm_idx ON gr0001 USING gin (stripped_line gin_trgm_ops);


--
-- Name: gr0001; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE gr0001 TO hippa_rd;


--
-- PostgreSQL database dump complete
--

