DROP TABLE IF EXISTS temp_admincode     CASCADE;
DROP TABLE IF EXISTS temp_poi_uid       CASCADE;

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
    uid        varchar(20) not null PRIMARY KEY,
    org_id1    bigint      not null,
    org_id2    bigint      not null
);

