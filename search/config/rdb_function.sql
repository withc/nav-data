CREATE OR REPLACE FUNCTION get_house_number( hn character varying)
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

create or replace function convert_coord( v double precision ) 
returns int
as $$
declare   
begin
    return (v*256*3600)::integer;
end;
$$ language 'plpgsql';

create or replace function base_coord( v double precision ) 
returns int
as $$
declare   
begin
    return (((v*256*3600)::integer>>16)-1)<<16;
end;
$$ language 'plpgsql';

create or replace function lonlat_to_mesh( lon int, lat int ) 
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
