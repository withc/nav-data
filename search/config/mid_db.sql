
DROP TABLE IF EXISTS mid_feat_key         CASCADE;
DROP TABLE IF EXISTS mid_country_profile  CASCADE;
DROP TABLE IF EXISTS mid_full_area        CASCADE;
DROP TABLE IF EXISTS mid_place            CASCADE;
DROP TABLE IF EXISTS mid_place_admin      CASCADE;
DROP TABLE IF EXISTS mid_postcode         CASCADE;

DROP TABLE IF EXISTS temp_org_category   CASCADE;
DROP TABLE IF EXISTS mid_poi             CASCADE;
DROP TABLE IF EXISTS mid_poi_attr_value  CASCADE;
DROP TABLE IF EXISTS mid_poi_address     CASCADE;
DROP TABLE IF EXISTS mid_poi_category    CASCADE;
DROP TABLE IF EXISTS mid_poi_children    CASCADE;

DROP TABLE IF EXISTS mid_link               CASCADE;

DROP TABLE IF EXISTS mid_link_road          CASCADE;
DROP TABLE IF EXISTS mid_place_road         CASCADE;
DROP TABLE IF EXISTS mid_address_range      CASCADE;
DROP TABLE IF EXISTS mid_address_point      CASCADE;
DROP TABLE IF EXISTS mid_bldg_point         CASCADE;

DROP TABLE IF EXISTS mid_feature_to_feature   CASCADE;
DROP TABLE IF EXISTS temp_postcode            CASCADE;

-- for street's name/geom
DROP TABLE IF EXISTS mid_street_name           CASCADE;
DROP TABLE IF EXISTS mid_street_geometry       CASCADE;
DROP TABLE IF EXISTS mid_street_to_name        CASCADE;
DROP TABLE IF EXISTS mid_street_to_geometry    CASCADE;
DROP TABLE IF EXISTS temp_street_name          CASCADE;
DROP TABLE IF EXISTS temp_street_name_gen_id   CASCADE;
DROP TABLE IF EXISTS temp_street_geom          CASCADE;
DROP TABLE IF EXISTS temp_street_geom_gen_id   CASCADE;

-- for poi's name/geom
DROP TABLE IF EXISTS mid_poi_name             CASCADE;
DROP TABLE IF EXISTS mid_poi_geometry         CASCADE;
DROP TABLE IF EXISTS mid_poi_to_name          CASCADE;
DROP TABLE IF EXISTS mid_poi_to_geometry      CASCADE;
DROP TABLE IF EXISTS temp_poi_name            CASCADE;
DROP TABLE IF EXISTS temp_poi_name_gen_id     CASCADE;
DROP TABLE IF EXISTS temp_poi_geom            CASCADE;
DROP TABLE IF EXISTS temp_poi_geom_gen_id     CASCADE;

--------------------------------------------------------------
create table mid_feat_key
(
    feat_key    serial PRIMARY KEY,
    feat_type   smallint not null,
    org_id1     bigint   not null,
    org_id2     bigint   not null,
    CONSTRAINT  un_item UNIQUE(org_id1,org_id2)  
);

-- place
create table mid_country_profile
(
    iso       char(3)  not null,
    off_lang  char(3)  not null,
    key       bigint   not null,
    type      smallint not null
);

CREATE TABLE mid_full_area
(
    min_lon  int  not null,
    min_lat  int  not null,
    max_lon  int  not null,
    max_lat  int  not null
);

create table mid_place
(
    key   bigint   not null PRIMARY KEY,
    type  smallint not null
);

create table mid_place_admin
(
    key    bigint not null PRIMARY KEY,
    type   smallint not null,
    a0     bigint not null,
    a1     bigint not null,
    a2     bigint not null,
    a7     bigint not null,
    a8     bigint not null,
    a9     bigint not null
);

-- postcode
create table mid_postcode
(
    key    bigint      not null PRIMARY KEY,
    type   smallint    not null,
    sub    smallint    not null,
    pocode varchar(16) not null
);

-- category
create table mid_poi_category
(
    per_code   bigint       not null PRIMARY KEY,
    gen1       int          not null,
    gen2       int          not null,
    gen3       int          not null,
    level      smallint     not null,
    imp        smallint     not null,
    name       varchar(128) not null,
    tr_name    varchar(128) not null default ''
);

-- poi
create table mid_poi
(
    key       bigint   not null PRIMARY KEY,
    type      smallint not null,
    gen_code  bigint   not null,
    imp       smallint not null
);

create table mid_poi_attr_value
(
    key         bigint       not null,
    type        smallint     not null,
    attr_type   char(2)      not null,
    attr_value  varchar(255) not null
);

create table mid_poi_address
(
    key         bigint       not null,
    type        smallint     not null,
    lang        char(3)      not null,
    name        varchar(128) not null,
    tr_lang     char(3)      not null,
    tr_name     varchar(128) not null,
    hno         varchar(32)  not null     
);

create table mid_poi_children
(
    c_k      bigint   not null,
    f_k      bigint   not null
);

-- street
create table mid_link
(
    key   bigint   not null PRIMARY KEY,
    type  smallint not null
);

-- house number
create table mid_link_road
(
    id         bigint       not null,
    key        bigint       not null,
    type       smallint     not null,
    langcode   char(4)      not null,
    name       varchar(255) not null
);

create table mid_place_road
(
    id          bigint       not null,
    pkey        bigint       not null,
    ptype       smallint     not null,
    lang        char(3)      not null,
    name        varchar(255) not null
);

create table mid_address_range
(
     id       bigint       not null,
     side     smallint     not null CONSTRAINT valid_sol    CHECK (side IN (1,2)),
     scheme   char(1)      not null CONSTRAINT valid_scheme CHECK (scheme IN ('M', 'O', 'E')),
     first    varchar(128) not null,
     last     varchar(128) not null
);

create table mid_address_point
(
     id       bigint       not null,
     side     smallint     not null CONSTRAINT valid_sol CHECK (side IN (1,2)),
     num      varchar(128) not null,
     x        int          not null,
     y        int          not null,
     dis_x    int          not null,
     dis_y    int          not null    
);

create table mid_bldg_point
(
     id       bigint       not null,
     pkey     bigint       not null,
     ptype    smallint     not null,
     
     lkey     bigint       not null,
     ltype    smallint     not null,
     side     smallint     not null CONSTRAINT valid_sol CHECK (side IN (1,2)),
     
     num      varchar(128) not null,
     x        int          not null,
     y        int          not null,
     entry_x  int          not null,
     entry_y  int          not null    
);
-- name
create table mid_street_name
(
    id        bigint       not null PRIMARY KEY,
    langcode  char(3)      not null,
    name      varchar(128) not null,
    tr_lang   char(3)      not null,
    tr_name   varchar(128) not null,
    ph_lang   char(3)      not null,
    ph_name   varchar(128) not null
);

create table mid_poi_name
(
    id        bigint       not null PRIMARY KEY,
    langcode  char(3)      not null,
    name      varchar(128) not null,
    tr_lang   char(3)      not null,
    tr_name   varchar(128) not null,
    ph_lang   char(3)      not null,
    ph_name   varchar(128) not null  
);

-- geometry
create table mid_street_geometry
(
    id    bigint   not null PRIMARY KEY,
    type  char     not null,
    geom  geometry not null
);

create table mid_poi_geometry
(
    id    bigint   not null PRIMARY KEY,
    type  char     not null,
    geom  geometry not null
);

-- releationship

create table mid_feature_to_feature
(
    fkey      bigint   not null,
    ftype     smallint not null,
    code      smallint not null,
    tkey      bigint   not null,
    ttype     smallint not null
);

create table mid_street_to_name
(
    key       bigint   not null,
    type      smallint not null,
    nametype  char(2)  not null,
    nameid    bigint   not null
);

create table mid_street_to_geometry
(
    key       bigint   not null,
    type      smallint not null,
    code      smallint not null,
    geomid    bigint   not null
);
--
create table mid_poi_to_name
(
    key       bigint   not null,
    type      smallint not null,
    nametype  char(2)  not null,
    nameid    bigint   not null
);

create table mid_poi_to_geometry
(
    key       bigint   not null,
    type      smallint not null,
    code      smallint not null,
    geomid    bigint   not null
);

-- temp table
create table temp_street_name
(
    gid       serial   PRIMARY KEY,
    key       bigint   not null,
    type      smallint not null,
    nametype  char(2)  not null,
    
    langcode  char(3)      not null,
    name      varchar(128) not null,
    tr_lang   char(3)      not null default '',
    tr_name   varchar(128) not null default '',
    ph_lang   char(3)      not null default '',
    ph_name   varchar(128) not null default ''
);

create table temp_street_name_gen_id
(
    gid       int      not null,
    nameid    int      not null
);

create table temp_street_geom
(
    gid      serial   PRIMARY KEY,
    key      bigint   not null,
    type     smallint not null,
    code     smallint not null,
    geotype  char     not null,
    geom     geometry not null
);

create table temp_street_geom_gen_id
(
    gid      int      not null,
    geomid   int      not null
);
-- for poi
create table temp_poi_name
(
    gid       serial   PRIMARY KEY,
    key       bigint   not null,
    type      smallint not null,
    nametype  char(2)  not null,
    
    langcode  char(3)      not null,
    name      varchar(128) not null,
    tr_lang   char(3)      not null default '',
    tr_name   varchar(128) not null default '',
    ph_lang   char(3)      not null default '',
    ph_name   varchar(128) not null default ''
);

create table temp_poi_name_gen_id
(
    gid       int      not null,
    nameid    int      not null
);

create table temp_poi_geom
(
    gid      serial   PRIMARY KEY,
    key      bigint   not null,
    type     smallint not null,
    code     smallint not null,
    geotype  char     not null,
    geom     geometry not null
);

create table temp_poi_geom_gen_id
(
    gid      int      not null,
    geomid   int      not null
);

create table temp_org_category
(
    per_code   bigint       not null,
    gen1       int          not null,
    gen2       int          not null,
    gen3       int          not null,
    level      smallint     not null,
    name       varchar(128) not null,
    imp        smallint     not null,
    org_code   bigint       not null,
    tr_name    varchar(128) not null default ''
);

--
create table temp_postcode
(
    id       int         not null,
    sub      smallint    not null,
    org_code varchar(16) not null
);


