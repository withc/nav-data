CREATE OR REPLACE FUNCTION mid_globetech_org1( 
	type smallint,
	prov varchar,
	amp  varchar,
	tam  varchar
)
  RETURNS  bigint 
  LANGUAGE plpgsql VOLATILE
  AS
$BODY$
BEGIN
    RETURN CASE type
	    WHEN 1 THEN prov::integer*10000
        WHEN 2 THEN prov::integer*10000 + amp::integer*100
        WHEN 3 THEN prov::integer*10000 + amp::integer*100 + tam::integer
	ELSE 0
	END;	
END;
$BODY$;
-----------------------------------------------------------
DROP TABLE IF EXISTS temp_admincode      CASCADE;
DROP TABLE IF EXISTS temp_org_category   CASCADE;
create table temp_admincode
(
    type       smallint    not null,
    prov_code  varchar(2)  not null,
    amp_code   varchar(2)  not null,
    tam_code   varchar(2)  not null,
    org_id1    bigint      not null,
    org_id2    bigint      not null
);

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
    name2      varchar(128) not null
);
