
DROP TABLE IF EXISTS temp_org_category  CASCADE;
DROP TABLE IF EXISTS temp_road_link     CASCADE;
DROP TABLE IF EXISTS temp_place_point   CASCADE;

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
