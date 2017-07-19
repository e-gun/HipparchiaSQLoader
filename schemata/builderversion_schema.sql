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

DROP TABLE public.builderversion;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: builderversion; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE builderversion (
    templateversion integer,
    corpusname character varying(2),
    corpusbuilddate character varying(20)
);


ALTER TABLE builderversion OWNER TO hippa_wr;

--
-- Name: builderversion; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE builderversion TO hippa_rd;


--
-- PostgreSQL database dump complete
--

