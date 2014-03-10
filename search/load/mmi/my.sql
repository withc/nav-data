DROP TABLE IF EXISTS temp_admincode     CASCADE;
DROP TABLE IF EXISTS temp_poi_uid       CASCADE;
DROP TABLE IF EXISTS temp_org_category  CASCADE;
DROP TABLE IF EXISTS temp_poi_category  CASCADE;

create table temp_admincode
(
    kind       smallint     not null,
    id         varchar(20)  not null,
    parent_id  varchar(20)  not null,
    org_id1    bigint       not null,
    org_id2    bigint       not null
);

create table temp_poi_uid
(
    uid        varchar(20) not null,
    org_id1    bigint      not null,
    org_id2    bigint      not null
);

create table temp_org_category
(
    org_id    varchar(10)  not null,
    name1     varchar(128) not null,
    name2     varchar(128) not null,
    org_code  varchar(10)  not null,
    imp       smallint     not null
);

create table temp_poi_category
(
    id        serial    PRIMARY KEY,
    level     smallint     not null,
    org_code  varchar(10)  not null,
    name      varchar(128) not null,
    imp       smallint     not null
);

