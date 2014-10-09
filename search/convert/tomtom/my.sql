
DROP TABLE IF EXISTS temp_road_link     CASCADE;
DROP TABLE IF EXISTS temp_phoneme       CASCADE;

create table temp_road_link
(
    id       serial       PRIMARY KEY,
    linkid   bigint       not null,
    feattyp  smallint     not null,
    langcode char(3)      not null,
    name     varchar(255) not null
);

create table temp_phoneme
(
    featclass   smallint     not null,
    shapeid     bigint       not null,
    nametype    character(2) not null,
    lang        char(3)      not null,
    name        varchar(128) not null,
    normname    varchar(128) not null,
    ptid        int          not null,
    ph_lang     char(3)      not null,
    ph_name     varchar(255) not null
);

