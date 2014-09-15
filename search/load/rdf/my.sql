
DROP TABLE IF EXISTS temp_road_link     CASCADE;
DROP TABLE IF EXISTS temp_place_point   CASCADE;
DROP TABLE IF EXISTS temp_ext_poi       CASCADE;

create table temp_road_link
(
    id      serial   PRIMARY KEY,
    linkid  bigint   not null,
    nameid  bigint   not null
);

create table temp_place_point
(
    key      bigint   not null PRIMARY KEY,
    type     smallint not null,
    geom     geometry 
);

create table temp_ext_poi
(
    poi_source  smallint  not null,
    poi_key     int       not null,
    
    cat_id   int          not null,
    lang     char(3)      not null,
    name     varchar(128) not null,
    iso      char(3)      not null,
    pl2      varchar(128),
    pl3      varchar(128),
    pl4      varchar(128),
    pl5      varchar(128),
    postcode varchar(128),
    st       varchar(128),
    hno      varchar(10),
    
    tel      varchar(32),
    lon      int not null,
    lat      int not null,
    CONSTRAINT pk_temp_ext_poi PRIMARY KEY (poi_source, poi_key )
);