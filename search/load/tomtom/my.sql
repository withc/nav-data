DROP TABLE IF EXISTS temp_road_link     CASCADE;

create table temp_road_link
(
    id       serial       PRIMARY KEY,
    linkid   bigint       not null,
    feattyp  smallint     not null,
    langcode char(3)      not null,
    name     varchar(255) not null
);