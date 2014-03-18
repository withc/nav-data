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