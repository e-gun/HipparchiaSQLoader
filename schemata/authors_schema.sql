--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP TABLE public.authors;
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: authors; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE public.authors (
    universalid character(6),
    language character varying(10),
    idxname character varying(128),
    akaname character varying(128),
    shortname character varying(128),
    cleanname character varying(128),
    genres character varying(512),
    recorded_date character varying(64),
    converted_date integer,
    location character varying(128)
);


ALTER TABLE public.authors OWNER TO hippa_wr;

--
-- Name: TABLE authors; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE public.authors TO hippa_rd;


--
-- PostgreSQL database dump complete
--

