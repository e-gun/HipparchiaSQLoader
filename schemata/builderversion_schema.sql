--
-- PostgreSQL database dump
--

-- Dumped from database version 11.3
-- Dumped by pg_dump version 11.3

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

DROP TABLE public.builderversion;
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: builderversion; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE public.builderversion (
    templateversion integer,
    corpusname character varying(2),
    corpusbuilddate character varying(64),
    buildoptions character varying(512)
);


ALTER TABLE public.builderversion OWNER TO hippa_wr;

--
-- Name: TABLE builderversion; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE public.builderversion TO hippa_rd;


--
-- PostgreSQL database dump complete
--

