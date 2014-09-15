create or replace function mid_gaode_coord( v float8 ) 
returns float8
as $$
declare   
begin
    return v/3600 ;
end;
$$ language 'plpgsql';