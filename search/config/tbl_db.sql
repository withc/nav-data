-- for simply solution
----------------------------------------------------
-- house number
----------------------------------------------------
DROP TABLE IF EXISTS tbl_search_meta   CASCADE;
DROP TABLE IF EXISTS tbl_genre_info    CASCADE;
DROP TABLE IF EXISTS tbl_city_info     CASCADE;
DROP TABLE IF EXISTS tbl_street_info   CASCADE;
DROP TABLE IF EXISTS tbl_poi_info      CASCADE;

DROP TABLE IF EXISTS tbl_hno_range           CASCADE;
DROP TABLE IF EXISTS tbl_hno_point           CASCADE;
DROP TABLE IF EXISTS tbl_place               CASCADE;
DROP TABLE IF EXISTS tmp_place_name          CASCADE;
DROP TABLE IF EXISTS tmp_link_place_name     CASCADE;
DROP TABLE IF EXISTS tmp_feat_lowest_place   CASCADE;

CREATE TABLE tbl_search_meta
(
    base_lon int  NOT NULL,
    base_lat int  NOT NULL,
    min_lon  int  NOT NULL,
    min_lat  int  NOT NULL,
    max_lon  int  NOT NULL,
    max_lat  int  NOT NULL
)

create table tbl_genre_info
(
    per_code   bigint       not null,
    gen1       int          not null,
    gen2       int          not null,
    gen3       int          not null,
    level      smallint     not null,
    imp        smallint     not null,
    name       varchar(128) not null
);

create table tbl_city_info
(
    level  int          not null,
    area1  int          not null,
    area2  int          not null,
    area3  int          not null,
    lon    int          not null,
    lat    int          not null,
    type   char(2)      not null,
    lang   char(3)      not null,
    name   varchar(255) not null
);

CREATE TABLE tbl_street_info
(
  id        int not null,
  area1     int not null,
  area2     int not null,
  area3     int not null,
  lon       int not null,
  lat       int not null,
  type      char(2)      not null,
  lang      char(3)      not null,
  name      varchar(255) not null
)

create table tbl_poi_info
(
  id  int  NOT NULL,
  lon int  NOT NULL,
  lat int  NOT NULL,
  int_entry_point_lon int,
  int_entry_point_lat int,
  
  type      char(2)      not null,
  lang      char(3)      not null,
  name      varchar(255) not null
  
  text_poi_name     varchar(255),
  text_phone_number varchar(255),
  text_address_text varchar(255),
  
  imp       int not null,
  gen1      int not null,
  gen2      int not null,
  gen3      int not null,
  area1     int not null,
  area2     int not null,
  area3     int not null,
  meshid    int not null
);

create table tbl_hno_range
(
    id       bigint        not null,
    country  varchar(128)  not null,
    state    varchar(128)  not null,
    city     varchar(128)  not null,
    district varchar(128)  not null,
    street   varchar(128)  not null,
    scheme   char(1)       not null,
    first    varchar(128)  not null,
    last     varchar(128)  not null
);

create table tbl_hno_point
(
    id       bigint       not null,
    country  varchar(128) not null,
    state    varchar(128) not null,
    city     varchar(128) not null,
    district varchar(128) not null,
    street   varchar(128) not null,
    num      varchar(128) not null
);

create table tbl_place
(
    key      bigint       not null,
    type     smallint     not null,
    country  varchar(128) not null,
    state    varchar(128) not null,
    city     varchar(128) not null,
    district varchar(128) not null
);
--
create table tmp_feat_lowest_place
(
    key   bigint       not null,
    type  smallint     not null,
    pkey   bigint       not null,
    ptype  smallint     not null
);

create table tmp_place_name
(
    key   bigint       not null,
    type  smallint     not null,
    lang  char(3)      not null,
    name  varchar(255) not null
);
---
create table tmp_link_place_name
(
    key   bigint   not null,
    type  smallint not null
);
