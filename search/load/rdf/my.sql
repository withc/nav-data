
DROP TABLE IF EXISTS temp_road_link     CASCADE;
DROP TABLE IF EXISTS temp_place_point   CASCADE;

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
