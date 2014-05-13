
DROP TABLE IF EXISTS voice_poi                CASCADE;
DROP TABLE IF EXISTS voice_state              CASCADE;
DROP TABLE IF EXISTS voice_street             CASCADE;
DROP TABLE IF EXISTS voice_street_hno_range   CASCADE;
DROP TABLE IF EXISTS voice_street_hno_point   CASCADE;
DROP TABLE IF EXISTS voice_bldg_point         CASCADE;
DROP TABLE IF EXISTS voice_tmp_full_place     CASCADE;

create table voice_tmp_full_place
(
  level  smallint,
  area0  int,
  area1  int,
  area2  int,
  area3  int,
  area4  int,
  langcode     char(3),
  country      varchar(255),
  state        varchar(255),
  city1        varchar(255),
  city2        varchar(255),
  city3        varchar(255)
);

create table voice_poi
(
   country_id   int,
   state_id     int,
   poi_id       int,
   gen_code     bigint,
   country      varchar(255),
   state        varchar(255),
   city1        varchar(255),
   city2        varchar(255),
   city3        varchar(255),
   poi_lang     char(3),
   poi_name     varchar(255),
   poi_phonetic varchar(255)
);

create table voice_state
(
   country_id   int          not null,
   state_id     int          not null,
   langcode     char(3)      not null,
   country      varchar(255) not null,
   state        varchar(255) not null
);

create table voice_street
(
   country_id   int,
   state_id     int,
   country      varchar(255),
   state        varchar(255),
   city1        varchar(255),
   city2        varchar(255),
   city3        varchar(255),
   name_type       char(2),
   street_lang     char(3),
   street_name     varchar(255),
   street_phonetic varchar(255)
);

create table voice_street_hno_range
(
   country_id   int,
   state_id     int,
   country      varchar(255),
   state        varchar(255),
   city1        varchar(255),
   city2        varchar(255),
   city3        varchar(255),
   name_type       char(2),
   street_lang     char(3),
   street_name     varchar(255),
   street_phonetic varchar(255),
   
   scheme          char(1),
   f_hno           varchar(128),
   l_hno           varchar(128) 
);

create table voice_street_hno_point
(
   country_id   int,
   state_id     int,
   country      varchar(255),
   state        varchar(255),
   city1        varchar(255),
   city2        varchar(255),
   city3        varchar(255),
   name_type       char(2),
   street_lang     char(3),
   street_name     varchar(255),
   street_phonetic varchar(255),
   hno             varchar(128)
);

create table voice_bldg_point
(
     country_id   int,
     state_id     int,
     langcode     char(3),
     country      varchar(255),
     state        varchar(255),
     city1        varchar(255),
     city2        varchar(255),
     city3        varchar(255),
     hno          varchar(128) not null
);
