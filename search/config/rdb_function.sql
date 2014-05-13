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
   pre character varying;
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

	pre = substring( hn, 0, s );
	
	-- for lead zero
	if pre = '' then
	   for i in 1 .. len loop
	      ch = substring( hn, i, 1);
	      if ch = '0' then
	         pre = pre||'0';
	      else 
	         exit;
	      end if;	    
	   end loop;
	end if;
	
	return pre;
END;
$$;

create or replace function srch_geomx( g geometry ) 
returns int
as $$
declare   
begin
    return (st_x(g)*100000)::int;
end;
$$ language 'plpgsql';

create or replace function srch_geomy( g geometry ) 
returns int
as $$
declare   
begin
    return (st_y(g)*100000)::int;
end;
$$ language 'plpgsql';

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

CREATE OR REPLACE FUNCTION srch_getphone( ph character varying  )
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

CREATE OR REPLACE FUNCTION srch_s_e_num( scheme char, s_num double precision, e_num double precision, is_s bool )
  RETURNS  integer 
  LANGUAGE plpgsql 
  AS $$
DECLARE
   s   integer;
   e   integer;

BEGIN
    
    if s_num < e_num then
        s = ceil(s_num);
        e = floor(e_num);
        if scheme = 'O' then
           if s%2 = 0 then
              s = s+1;
           end if;
           if e%2 = 0 then
              e = e-1;
           end if;
        elsif scheme = 'E' then
           if s%2 = 1 then
              s = s+1;
           end if;
           if e%2 = 1 then
              e = e-1;
           end if;
        end if; 
        if s > e then
           s = -1;
           e = -1;
        end if;
    else
        s = floor(s_num);
        e = ceil(e_num);
        if scheme = 'O' then
           if s%2 = 0 then
              s = s-1;
           end if;
           if e%2 = 0 then
              e = e+1;
           end if;
        elsif scheme = 'E' then
           if s%2 = 1 then
              s = s-1;
           end if;
           if e%2 = 1 then
              e = e+1;
           end if;
        end if ;
        if s < e then
           s = -1;
           e = -1;
        end if;
    end if;
    
    if is_s then
        return s;
    else 
        return e;
    end if;
END;
$$;

create or replace function srch_punctuation(  str character varying ) 
returns bool
LANGUAGE plpgsql 
as $$
declare
   d int = ascii(str);
BEGIN
   return case d
      when 32 then true
      when 34 then true
      when 39 then true
      when 40 then true
      when 41 then true
      when 44 then true
      when 59 then true
      when 60 then true
      when 61 then true
      when 91 then true
      when 93 then true
      when 123 then true
      when 125 then true
      else false
    end;
    
END;
$$;

create or replace function srch_full_name( in_type char,  in_lang character varying, in_name character varying ) 
returns character varying
as $$
declare  
    curs refcursor; 
    abbr_w    character varying;
    full_w    character varying;
    full_name character varying = '';
    pos       int;
begin
    OPEN curs FOR SELECT abbr, full_n
			        FROM mid_abbr_word
			       where type = in_type and lang = in_lang;

	-- Get the first record        
	FETCH curs INTO abbr_w, full_w;
	while abbr_w is not null LOOP
		pos = strpos( in_name, abbr_w );
		--RAISE NOTICE 'POS = %', pos;
		
		if pos <> 0 and ( pos = 1 or srch_punctuation( substr(in_name, pos-1, 1) ) ) then
		   pos = pos+length(abbr_w);
		   if pos = length(in_name)+1  or srch_punctuation( substr(in_name, pos, 1) ) then
		       full_name = replace( in_name, abbr_w, full_w );
		       --RAISE NOTICE 'FULL = %', full_name;
		       exit;
		   end if;
		end if;
		
		-- Get the next record
		FETCH curs INTO abbr_w, full_w;
	END LOOP;
	close curs;
    
    return full_name;
end;
$$ language 'plpgsql';

create or replace function srch_get_admin(  ary bigint[], idx int ) 
returns bigint
LANGUAGE plpgsql 
as $$
declare
BEGIN
     FOR i IN 1..array_length(ary,1)
     LOOP
         if ary[i] <> 0 then
            idx=idx-1;
            if idx = 0 then
               return ary[i];
            end if;
         end if;
     END LOOP; 
     return 0;
END;
$$;

create or replace function srch_adjust_name(  in_name varchar ) 
returns  character varying
LANGUAGE plpgsql 
as $$
declare
   pre   varchar = '';
   suf   varchar = '';
   len   integer;
   ch    varchar;
   ispre bool = true;
BEGIN
     if '(' <> substr(in_name, 1, 1) then
         return in_name;
     end if;
     
     len  = length(in_name);
     
     FOR i IN 1..len
     LOOP
         ch = substr( in_name, i, 1);
	     if ispre then
	        pre = pre || ch;
	     else
	        suf = suf || ch;
	     end if;
	     
     
	     if ')' = ch  and ispre = true then
	        ispre = false;
	     end if;	    
     END LOOP;

     if suf = '' then
        return suf;
     else
       return btrim(suf) || ' ' || btrim(pre) ;
     end if;
END;
$$;

create or replace function srch_compare_name(  name1 varchar, name2 varchar  ) 
returns bool
LANGUAGE plpgsql 
as $$
declare
  pos int = strpos( name1, ' ');
BEGIN

     if name1 = name2 or name1||'.' = name2  then 
         return true;
     end if; 
     
     if pos > 0 and name2 = substring(name1, pos+1 ) || ' ' || substring( name1,1, pos-1 ) then
        return true;
     end if;
     
     return false;
END;
$$;

