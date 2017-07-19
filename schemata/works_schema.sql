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

DROP TABLE public.works;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: works; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE works (
    universalid character(10),
    title character varying(512),
    language character varying(10),
    publication_info text,
    levellabels_00 character varying(64),
    levellabels_01 character varying(64),
    levellabels_02 character varying(64),
    levellabels_03 character varying(64),
    levellabels_04 character varying(64),
    levellabels_05 character varying(64),
    workgenre character varying(32),
    transmission character varying(32),
    worktype character varying(32),
    provenance character varying(64),
    recorded_date character varying(64),
    converted_date integer,
    wordcount integer,
    firstline integer,
    lastline integer,
    authentic boolean
);


ALTER TABLE works OWNER TO hippa_wr;

--
-- Name: works; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE works TO hippa_rd;


--
-- PostgreSQL database dump complete
--

