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

DROP INDEX public.gr0001_st_trgm_idx;
DROP INDEX public.gr0001_mu_trgm_idx;
ALTER TABLE ONLY public.gr0001 DROP CONSTRAINT gr0001_index_key;
DROP TABLE public.gr0001;
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: gr0001; Type: TABLE; Schema: public; Owner: hippa_wr
--

CREATE TABLE public.gr0001 (
    index integer DEFAULT nextval('public.gr0001'::regclass) NOT NULL,
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


ALTER TABLE public.gr0001 OWNER TO hippa_wr;

--
-- Name: gr0001 gr0001_index_key; Type: CONSTRAINT; Schema: public; Owner: hippa_wr
--

ALTER TABLE ONLY public.gr0001 ADD CONSTRAINT gr0001_index_key UNIQUE (index);


--
-- Name: gr0001_mu_trgm_idx; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE INDEX gr0001_mu_trgm_idx ON public.gr0001 USING gin (accented_line public.gin_trgm_ops);


--
-- Name: gr0001_st_trgm_idx; Type: INDEX; Schema: public; Owner: hippa_wr
--

CREATE INDEX gr0001_st_trgm_idx ON public.gr0001 USING gin (stripped_line public.gin_trgm_ops);


--
-- Name: TABLE gr0001; Type: ACL; Schema: public; Owner: hippa_wr
--

GRANT SELECT ON TABLE public.gr0001 TO hippa_rd;


--
-- PostgreSQL database dump complete
--

