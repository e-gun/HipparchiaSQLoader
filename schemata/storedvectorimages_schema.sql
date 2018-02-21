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

DROP TABLE public.storedvectorimages;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: storedvectorimages; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE storedvectorimages (
    imagename character varying(12),
    imagedata bytea
);


ALTER TABLE storedvectorimages OWNER TO hippa_wr;

--
-- Name: TABLE storedvectorimages; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE storedvectorimages TO hippa_rd;


--
-- PostgreSQL database dump complete
--

