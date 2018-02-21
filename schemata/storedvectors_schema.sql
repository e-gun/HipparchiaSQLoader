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

DROP TABLE public.storedvectors;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: storedvectors; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE storedvectors (
    ts timestamp without time zone,
    versionstamp character varying(6),
    uidlist text[],
    vectortype character varying(10),
    calculatedvectorspace bytea
);


ALTER TABLE storedvectors OWNER TO hippa_wr;

--
-- Name: TABLE storedvectors; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE storedvectors TO hippa_rd;


--
-- PostgreSQL database dump complete
--

