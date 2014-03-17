CREATE OR REPLACE FUNCTION get_house_number( hn character varying)
  RETURNS integer 
  LANGUAGE plpgsql 
  AS $$
DECLARE
   s  integer;
   e  integer;
   ch char;
BEGIN
    s = 1;
    e = length(hn);
    for i in reverse length(hn) .. 1 loop
	    ch = substring( hn, i, 1);
	    if '0' <= ch and ch <= '9' then
	         e = i;
	         EXIT;
	    end if;	    
    end loop;

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