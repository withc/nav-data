
DROP TABLE IF EXISTS temp_org_category  CASCADE;

create table temp_org_category
(
    org_code  varchar(10)  not null,
    name     varchar(128)  not null,
    imp       smallint     not null
);