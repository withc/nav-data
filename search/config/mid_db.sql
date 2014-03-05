
DROP TABLE IF EXISTS mid_feat_key         CASCADE;
DROP TABLE IF EXISTS mid_place            CASCADE;
DROP TABLE IF EXISTS mid_place_admin      CASCADE;
DROP TABLE IF EXISTS mid_postcode         CASCADE;

DROP TABLE IF EXISTS mid_poi             CASCADE;
DROP TABLE IF EXISTS mid_poi_attr_value  CASCADE;
DROP TABLE IF EXISTS mid_poi_category    CASCADE;
DROP TABLE IF EXISTS mid_poi_children    CASCADE;

DROP TABLE IF EXISTS mid_link            CASCADE;

DROP TABLE IF EXISTS mid_name                 CASCADE;
DROP TABLE IF EXISTS mid_geometry             CASCADE;
DROP TABLE IF EXISTS mid_geometry_xyz         CASCADE;
DROP TABLE IF EXISTS mid_feature_to_name      CASCADE;
DROP TABLE IF EXISTS mid_feature_to_geometry  CASCADE;
DROP TABLE IF EXISTS mid_feature_to_feature   CASCADE;


DROP TABLE IF EXISTS temp_feat_name            CASCADE;
DROP TABLE IF EXISTS temp_feat_name_gen_id     CASCADE;
DROP TABLE IF EXISTS temp_feat_geom            CASCADE;
DROP TABLE IF EXISTS temp_feat_geom_gen_id     CASCADE;
DROP TABLE IF EXISTS temp_feat_class           CASCADE;
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
create table mid_place
(
    key   bigint   not null,
    type  smallint not null
);

create table mid_place_admin
(
    key    bigint not null,
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
    key    bigint      not null,
    type   smallint    not null,
    sub    smallint    not null,
    pocode varchar(16) not null
);

-- category
create table mid_poi_category
(
    cat_id        int not null,
    parent_cat_id int not null,
    level         smallint not null,
    imp           smallint,
    cat_name      varchar(128) not null
);

-- poi
create table mid_poi
(
    key     bigint   not null,
    type    smallint not null,
    cat_id  int      not null,
    imp     smallint not null
);

create table mid_poi_attr_value
(
    key         bigint       not null,
    type        smallint     not null,
    attr_type   char(2)      not null,
    attr_value  varchar(128) not null
);

create table mid_poi_children
(
    c_k      bigint   not null,
    f_k      bigint   not null
);

-- street
create table mid_link
(
    key   bigint   not null,
    type  smallint not null,
    
);

-- name
create table mid_name
(
    id       bigint       not null,
    langcode char(4)      not null,
    name     varchar(256) not null
);

-- geometry
create table mid_geometry
(
    id    bigint   not null,
    type  char     not null,
    geom  geometry not null
);

create table mid_geometry_xyz
(
    id   bigint   not null,
    seq  smallint not null,
    x    INT      NOT NULL,
    y    INT      NOT NULL,
    z    INT      NOT NULL
);

-- releationship

create table mid_feature_to_feature
(
    fkey       bigint   not null,
    ftype      smallint not null,
    code      smallint not null,
    tkey      bigint   not null,
    ttype     smallint not null
);

create table mid_feature_to_name
(
    key       bigint   not null,
    type      smallint not null,
    nametype  char(2)  not null,
    nameid    bigint   not null
);

create table mid_feature_to_geometry
(
    key       bigint   not null,
    type      smallint not null,
    code      smallint not null,
    geomid    bigint   not null
);

-- temp table
create table temp_feat_name
(
    key       bigint   not null,
    type      smallint not null,
    nametype  char(2)  not null,
    langcode  char(4)  not null,
    name      varchar(256)
);

create table temp_feat_name_gen_id
(
    key       bigint   not null,
    type      smallint not null,
    nametype  char(2)  not null,
    langcode  char(4)  not null,
    name      varchar(256),
    nameid    int      not null
);

create table temp_feat_geom
(
    key      bigint   not null,
    type     smallint not null,
    code     smallint not null,
    geotype  char     not null,
    geom     geometry not null
);

create table temp_feat_geom_gen_id
(
    key      bigint   not null,
    type     smallint not null,
    code     smallint not null,
    geotype  char     not null,
    geom     geometry not null,
    geomid   int      not null
);

create table temp_feat_class
(
    c1       int not null,
    c2       int not null,
    c3       int not null,
    level    smallint     not null,
    imp      smallint     not null,
    name     varchar(128) not null
);


