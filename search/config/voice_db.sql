
DROP TABLE IF EXISTS voice_poi   CASCADE;
DROP TABLE IF EXISTS voice_state   CASCADE;
DROP TABLE IF EXISTS voice_street   CASCADE;
DROP TABLE IF EXISTS voice_street_hno_rang   CASCADE;
DROP TABLE IF EXISTS voice_street_hno_point   CASCADE;
DROP TABLE IF EXISTS voice_tmp_full_place     CASCADE;

create table voice_tmp_full_place
(
  level  smallint,
  area0  int,
  area1  int,
  area2  int,
  area3  int,
  country      varchar(255),
  state        varchar(255),
  city         varchar(255),
  district     varchar(255)
);

create table voice_poi
(
   country_id   int,
   state_id     int,
   poi_id       int,
   gen_code     bigint,
   country      varchar(255),
   state        varchar(255),
   city         varchar(255),
   district     varchar(255),
   poi_name     varchar(255),
   poi_phonetic varchar(255)
);

create table voice_state
(
   country_id   int,
   state_id     int,
   country      varchar(255),
   state        varchar(255)
);

create table voice_street
(
   country_id   int,
   state_id     int,
   country      varchar(255),
   state        varchar(255),
   city         varchar(255),
   district     varchar(255),
   name_type    char(2),
   street_name  varchar(255),
   street_phonetic varchar(255)
);

create table voice_street_hno_rang
(
   country_id   int,
   state_id     int,
   country      varchar(255),
   state        varchar(255),
   city         varchar(255),
   district     varchar(255),
   name_type       char(2),
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
   city         varchar(255),
   district     varchar(255),
   name_type    char(2),
   street_name     varchar(255),
   street_phonetic varchar(255),
   hno             varchar(128)
);