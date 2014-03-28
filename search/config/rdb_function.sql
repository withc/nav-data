CREATE OR REPLACE FUNCTION srch_hno_num( hn character varying)
  RETURNS integer 
  LANGUAGE plpgsql 
  AS $$
DECLARE
   s   integer;
   e   integer;
   len integer = length(hn);
   ch  char;
BEGIN
    s = 1;
    e = len+1;
    for i in reverse len .. 1 loop
	    ch = substring( hn, i, 1);
	    if '0' <= ch and ch <= '9' then
	         e = i;
	         EXIT;
	    end if;	    
    end loop;
    
    if e > len then
        return 0;
    end if;
    
	for i in reverse e .. 1 loop
	    ch = substring( hn, i, 1);
	    if ch < '0'  or  '9' < ch then
	       s = i+1;
	       EXIT;
	    end if;	    
	end loop;

	return substring( hn, s, e-s+1 )::integer;
END;
$$;

CREATE OR REPLACE FUNCTION srch_hno_suffix( hn character varying)
  RETURNS  character varying 
  LANGUAGE plpgsql 
  AS $$
DECLARE
   s   integer;
   e   integer;
   len integer = length(hn);
   ch  char;
BEGIN
    s = 1;
    e = len+1;
    for i in reverse len .. 1 loop
	    ch = substring( hn, i, 1);
	    if '0' <= ch and ch <= '9' then
	         e = i;
	         EXIT;
	    end if;	    
    end loop;
    
    if e > len then
        return '';
    end if;

	return substring( hn, e+1 );
END;
$$;

CREATE OR REPLACE FUNCTION srch_hno_prefix( hn character varying)
  RETURNS  character varying 
  LANGUAGE plpgsql 
  AS $$
DECLARE
   s   integer;
   e   integer;
   len integer = length(hn);
   ch  char;
BEGIN
    s = 1;
    e = len+1;
    for i in reverse len .. 1 loop
	    ch = substring( hn, i, 1);
	    if '0' <= ch and ch <= '9' then
	         e = i;
	         EXIT;
	    end if;	    
    end loop;
    
    if e > len then
        return '';
    end if;
    
	for i in reverse e .. 1 loop
	    ch = substring( hn, i, 1);
	    if ch < '0'  or  '9' < ch then
	       s = i+1;
	       EXIT;
	    end if;	    
	end loop;

	return substring( hn, 0, s );
END;
$$;

create or replace function srch_coord( v integer ) 
returns int
as $$
declare   
begin
    return (v/100000.0*256*3600)::integer;
end;
$$ language 'plpgsql';

create or replace function srch_base_coord( v integer ) 
returns int
as $$
declare   
begin
    return (((v/100000.0*256*3600)::integer>>16)-1)<<16;
end;
$$ language 'plpgsql';

create or replace function srch_mesh( lon int, lat int ) 
returns int
as $$
declare  
    code int;
    x    int;
    y    int;  
begin
    lon = lon - ( select min(base_lon) from tbl_search_meta );
    lat = lat - ( select min(base_lat) from tbl_search_meta );

    code = 0;

    for  icnt in 1 .. 19 loop
	 x = ((lon>>(32-icnt))&1)<<1;
	 y = (lat>>(32-icnt))&1;
	 code = (code << 2) + (x+y);
    end loop;
    return code;
end;
$$ language 'plpgsql';

CREATE OR REPLACE FUNCTION getphone( ph character varying  )
  RETURNS character varying  AS
$BODY$
declare
    len    integer = length(ph);
    ch     char;
    numstr character varying = '';
begin
    
    for i in 1 .. len loop
	    ch = substring( ph, i, 1);
	    if '0' <= ch and ch <= '9' then
	         numstr := numstr || ch;
	    end if;	    
    end loop;
    return numstr;    
end;
$BODY$ language 'plpgsql';
