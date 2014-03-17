
DROP TABLE IF EXISTS temp_org_category  CASCADE;
DROP TABLE IF EXISTS temp_poi_category  CASCADE;
DROP TABLE IF EXISTS temp_road_link     CASCADE;

create table temp_org_category
(
    org_code  bigint        not null,
    name      varchar(128)  not null,
    imp       smallint      not null
);

create table temp_poi_category
(
    id        serial       PRIMARY KEY,
    level     smallint     not null,
    org_code  bigint       not null,
    name      varchar(128) not null,
    imp       smallint     not null
);

create table temp_road_link
(
    id      serial   PRIMARY KEY,
    linkid  bigint   not null,
    nameid  bigint   not null
);
