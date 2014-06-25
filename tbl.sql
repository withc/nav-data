CREATE TABLE tbl_genre_info
(
  u_code bigint NOT NULL,
  gen1 integer NOT NULL,
  gen2 integer NOT NULL,
  gen3 integer NOT NULL,
  level smallint NOT NULL,
  imp smallint NOT NULL,
  name character varying(128) NOT NULL
);
--
CREATE TABLE xtbl_city_info
(
  int_area_id1 integer NOT NULL,
  int_area_id2 integer NOT NULL,
  int_area_id3 integer NOT NULL,
  var_name     character varying(256),
  int_area_lon integer NOT NULL,
  int_area_lat integer NOT NULL,
  full_name    text
);

insert into xtbl_city_info( int_area_id1, int_area_id2, int_area_id3, var_name, int_area_lon, int_area_lat, full_name )
select  c.area1, c.area2, c.area3, n.name, c.lon, c.lat, ''
from tbl_city_info  as c
join tbl_city_name  as n
  on c.area0 = n.area0 and 
     c.area1 = n.area1 and 
	 c.area2 = n.area2 and 
	 c.area3 = n.area3 and
	 n.lang = 'ENG'
	 
--
CREATE TABLE xtbl_street_info
(
  int_street_id integer NOT NULL,
  
  int_area_id1 integer NOT NULL,
  int_area_id2 integer NOT NULL,
  int_area_id3 integer NOT NULL,
  var_name character varying(256),
  
  int_street_lon integer NOT NULL,
  int_street_lat integer NOT NULL
);

insert into xtbl_street_info( int_street_id, int_area_id1, int_area_id2, int_area_id3, var_name, int_street_lon, int_street_lat )
select s.id, s.area1,  s.area2, s.area3, n.name, s.lon, s.lat
from tbl_street_info  as s
join tbl_street_name  as n
  on s.id = n.id and 
	 n.lang = 'ENG'
--
CREATE TABLE xtbl_poi_info
(
  int_poi_id integer NOT NULL,
  int_poi_lon integer NOT NULL,
  int_poi_lat integer NOT NULL,
  int_entry_point_lon integer,
  int_entry_point_lat integer,
  
  text_poi_name     text,
  text_phone_number text,
  text_address      text,
  text_postcode     text,
  
  int_genre_code  integer,
  int_important   integer,

  int_area_id1 integer NOT NULL,
  int_area_id2 integer NOT NULL,
  int_area_id3 integer NOT NULL,
  
  int_mesh_id integer
);

insert into xtbl_poi_info( int_poi_id, int_poi_lon, int_poi_lat, int_entry_point_lon, int_entry_point_lat,
                           text_poi_name, text_phone_number, text_address, text_postcode,
						   int_genre_code, int_important, 
                           int_area_id1, int_area_id2, int_area_id3, int_mesh_id )
select p.id, p.lon, p.lat, p.entry_lon, p.entry_lat, n.name, getphone(p.tel), 
       case
          when a.hno <> '' then a.hno || ',' || a.street
		  else a.street
	    end, p.postcode, (p.gen1<<24)+(p.gen2<<16)+p.gen3, p.imp,
		p.area1, p.area2, p.area3, p.meshid
from tbl_poi_info  as p
left join tbl_poi_address as a
  on p.id = a.id
left join tbl_poi_name as n
  on p.id = n.id and n.type = 'ON'
  order by n.name
