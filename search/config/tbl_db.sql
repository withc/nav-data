-- for simply solution
----------------------------------------------------
-- house number
----------------------------------------------------
DROP TABLE IF EXISTS tbl_abbr_word     CASCADE;
DROP TABLE IF EXISTS tbl_search_meta   CASCADE;
DROP TABLE IF EXISTS tbl_genre_info    CASCADE;
DROP TABLE IF EXISTS tbl_city_info     CASCADE;
DROP TABLE IF EXISTS tbl_city_name     CASCADE;
DROP TABLE IF EXISTS tbl_postcode_info CASCADE;
DROP TABLE IF EXISTS tbl_postcode_city CASCADE;

DROP TABLE IF EXISTS tbl_street_info   CASCADE;
DROP TABLE IF EXISTS tbl_street_name   CASCADE;
DROP TABLE IF EXISTS tbl_street_full_name CASCADE;

DROP TABLE IF EXISTS tbl_poi_info      CASCADE;
DROP TABLE IF EXISTS tbl_poi_address   CASCADE;
DROP TABLE IF EXISTS tbl_poi_name      CASCADE;
DROP TABLE IF EXISTS tbl_poi_full_name CASCADE;

DROP TABLE IF EXISTS tbl_bldg_point          CASCADE;
DROP TABLE IF EXISTS tbl_street_hno_range    CASCADE;
DROP TABLE IF EXISTS tbl_street_hno_point    CASCADE;
DROP TABLE IF EXISTS tbl_dealer_data         CASCADE;

DROP TABLE IF EXISTS tmp_place_admin         CASCADE;
DROP TABLE IF EXISTS tmp_place_area          CASCADE;
DROP TABLE IF EXISTS tmp_place_name          CASCADE;
DROP TABLE IF EXISTS tmp_poi                 CASCADE;
DROP TABLE IF EXISTS tmp_poi_duplicate       CASCADE;
DROP TABLE IF EXISTS tmp_postcode            CASCADE;

DROP TABLE IF EXISTS tmp_street              CASCADE;
DROP TABLE IF EXISTS tmp_poi_attr            CASCADE;
DROP TABLE IF EXISTS tmp_poi_geom            CASCADE;
DROP TABLE IF EXISTS tmp_street_geom         CASCADE;
DROP TABLE IF EXISTS tmp_street_hno_id       CASCADE;
DROP TABLE IF EXISTS tmp_feat_lowest_place   CASCADE;

DROP TABLE IF EXISTS tmp_org_to_many_rdb_link CASCADE;

CREATE TABLE tbl_search_meta
(
    base_lon int  NOT NULL,
    base_lat int  NOT NULL,
    min_lon  int  NOT NULL,
    min_lat  int  NOT NULL,
    max_lon  int  NOT NULL,
    max_lat  int  NOT NULL
);

create table tbl_abbr_word
(
    type      char(1)       not null,
    lang      char(3)       not null,
    abbr      varchar(128)  not null,
    full_n    varchar(128)  not null
);

create table tbl_genre_info
(
    u_code     bigint       not null,
    gen1       int          not null,
    gen2       int          not null,
    gen3       int          not null,
    level      smallint     not null,
    imp        smallint     not null,
    name       varchar(128) not null,
    tr_name    varchar(128) not null,
    cnt        int          not null
);

create table tbl_postcode_info
(
    id      int         PRIMARY KEY,
    area0   int         not null,
    pocode  varchar(32) not null,
    lon     int,
    lat     int    
);

create table tbl_postcode_city
(
    id     int          not null,
    area0  int          not null,
    area1  int          not null,
    area2  int          not null,
    area3  int          not null,
    area4  int          not null
);

create table tbl_city_info
(
    level  int          not null,
    area0  int          not null,
    area1  int          not null,
    area2  int          not null,
    area3  int          not null,
    area4  int          not null,
    lon    int          not null,
    lat    int          not null,
    PRIMARY KEY ( area0, area1, area2, area3, area4 ) 
);

create table tbl_city_name
(
    level  int          not null,
    area0  int          not null,
    area1  int          not null,
    area2  int          not null,
    area3  int          not null,
    area4  int          not null,
    type     char(2)      not null,
    lang     char(3)      not null,
    name     varchar(128) not null,
    tr_lang  char(3)      not null,
    tr_name  varchar(128) not null,
    ph_lang  char(3)      not null,
    ph_name  varchar(128) not null
);

CREATE TABLE tbl_street_info
(
  id        int          PRIMARY KEY,
  level     int          not null,
  area0     int          not null,
  area1     int          not null,
  area2     int          not null,
  area3     int          not null,
  area4     int          not null,
  lon       int          not null,
  lat       int          not null
);

create table tbl_street_name
(
    id       int          not null,
    type     char(2)      not null,
    lang     char(3)      not null,
    name     varchar(128) not null,
    tr_lang  char(3)      not null,
    tr_name  varchar(128) not null,
    ph_lang  char(3)      not null,
    ph_name  varchar(128) not null
);

create table tbl_street_full_name
(
    id        int          NOT NULL,
    lang      char(3)      not null,
    name      varchar(128) not null,
    full_name varchar(128) not null
);
--
create table tbl_poi_info
(
  id        int  PRIMARY KEY,
  
  lon       int  NOT NULL,
  lat       int  NOT NULL,
  entry_lon int,
  entry_lat int,
  
  tel       varchar(255),
  fax       varchar(255),
  email     varchar(255),
  internet  varchar(255),
  postcode  varchar(32),
  imp       int not null,
  gen1      int not null,
  gen2      int not null,
  gen3      int not null,
  area0     int not null,
  area1     int not null,
  area2     int not null,
  area3     int not null,
  area4     int not null,
  meshid    int not null
);

create table tbl_poi_address
(
    id         int          NOT NULL,
    lang       char(3)      not null,
    street     varchar(128) not null,
    tr_lang    char(3)      not null,
    tr_street  varchar(128) not null,
    hno        varchar(32)  not null
);

create table tbl_poi_name
(
    id        int          NOT NULL,
    type      char(2)      not null,
    lang      char(3)      not null,
    name      varchar(128) not null,
    tr_lang   char(3)      not null,
    tr_name   varchar(128) not null,
    ph_lang   char(3)      not null,
    ph_name   varchar(128) not null
);

create table tbl_poi_full_name
(
    id        int          NOT NULL,
    lang      char(3)      not null,
    name      varchar(128) not null,
    full_name varchar(128) not null
);

create table tbl_dealer_data
(
    id        int          NOT NULL,
    area0     int          not null,
    meshid    int          not null,
    gen_code  int          not null,
    lang      char(3)      not null,
    name      varchar(128) not null,
    tr_name   varchar(128) not null,
    postcode  varchar(32)  not null,
    address   varchar(255) not null,
    tr_address varchar(255) not null,
    tel       varchar(255) not null,
    lon       int          NOT NULL,
    lat       int          NOT NULL,
    entry_lon int,
    entry_lat int
);
---
create table tbl_street_hno_range
(
    id       bigint        not null,
    link_id  bigint        not null,
	side     smallint      not null,
    scheme   char(1)       not null,
    prefix   varchar(128)  not null,
    suffix   varchar(128)  not null,
    f_hno    varchar(128)  not null,
    l_hno    varchar(128)  not null,
    
    rdb_link_id  bigint    not null,
    s_fraction   int       not null,
    e_fraction   int       not null
);

create table tbl_street_hno_point
(
    id        bigint       not null,
    link_id   bigint       not null,
    side      smallint     not null,
    prefix    varchar(128) not null,
    suffix    varchar(128) not null,
    hno       varchar(128) not null,
    lon       int          not null,
    lat       int          not null,
    entry_lon int          not null,
    entry_lat int          not null,
    
    rdb_link_id  bigint    not null
);

create table tbl_bldg_point
(
     id        bigint not null,
     area0     int    not null,
     area1     int    not null,
     area2     int    not null,
     area3     int    not null,
     area4     int    not null,
     
     link_id      bigint       not null,
     side         smallint     not null,
     hno          varchar(128) not null,
     lon          int          not null,
     lat          int          not null,
     entry_lon    int          not null,
     entry_lat    int          not null,
     rdb_link_id  bigint       not null    
);

create table tmp_street_hno_id
(
    id           int     not null,
    org_link_id  bigint  not null,
    
    mid_id       int     not null
);

create table tmp_place_name
(
    key      bigint       not null,
    type     smallint     not null,
    nametype char(2)      not null,
    lang     char(3)      not null,
    name     varchar(128) not null,
    tr_lang  char(3)      not null,
    tr_name  varchar(128) not null,
    ph_lang  char(3)      not null,
    ph_name  varchar(128) not null
);

create table tmp_place_admin
(
    key    bigint    not null PRIMARY KEY,
    type   smallint  not null,
    level  smallint  not null,
    k0     bigint not null,
    k1     bigint not null,
    k2     bigint not null,
    k3     bigint not null,
    k4     bigint not null
);

create table tmp_place_area
(
    key    bigint    not null PRIMARY KEY,
    type   smallint  not null,
    level  smallint  not null,
    area0  int       not null,
    area1  int       not null,
    area2  int       not null,
    area3  int       not null,
    area4  int       not null
);

create table tmp_postcode
(
    key    bigint    not null,
    type   smallint  not null,
    id     int       not null
);

create table tmp_poi
(
    key    bigint    not null,
    type   smallint  not null,
    pkey   bigint    not null,
    id     int       not null
);

create table tmp_poi_duplicate
( 
    key       bigint  not null,
    save      char(1) not null
);

create table tmp_poi_attr
(
   id        int   not null,
   tel       varchar(255),
   fax       varchar(255),
   email     varchar(255),
   internet  varchar(255)
);

create table tmp_poi_geom
( 
    id        int not null,
    mlon       int not null,
    mlat       int not null,
    entry_mlon int not null,
    entry_mlat int not null
);

create table tmp_street
(
    key    bigint    not null,
    type   smallint  not null,
    pkey   bigint    not null,
    ptype  bigint    not null,
    nameid int       not null,
    id     int       not null
);

create table tmp_street_geom
(
       id    int not null,
       geom  geometry not null
);

create table tmp_org_to_many_rdb_link
(
       org_link_id  bigint           NOT NULL,
       s_org        double precision not null,
       e_org        double precision not null,
       rdb_link_id  bigint           NOT NULL,
       s_rdb        double precision not null,
       e_rdb        double precision not null,
       flag         boolean          not null,
       seq          int              not null
);
--
create table tmp_feat_lowest_place
(
    key    bigint       not null,
    type   smallint     not null,
    pkey   bigint       not null,
    ptype  smallint     not null
);

