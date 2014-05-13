
DROP TABLE IF EXISTS xtbl_city_info       CASCADE;
DROP TABLE IF EXISTS xtbl_street_info     CASCADE;
DROP TABLE IF EXISTS xtbl_poi_info        CASCADE;
DROP TABLE IF EXISTS xtbl_dealer_data     CASCADE;

CREATE TABLE xtbl_city_info
(
  int_area_id0 integer NOT NULL,
  int_area_id1 integer NOT NULL,
  int_area_id2 integer NOT NULL,
  int_area_id3 integer NOT NULL,
  int_area_id4 integer NOT NULL,
  name_type            char(2) not null,
  var_name        varchar(255) not null,
  var_name_trans  varchar(255) not null,
  
  int_area_lon integer NOT NULL,
  int_area_lat integer NOT NULL
);

CREATE TABLE xtbl_street_info
(
  int_street_id   integer NOT NULL,
  int_area_id0    integer NOT NULL,
  int_area_id1    integer NOT NULL,
  int_area_id2    integer NOT NULL,
  int_area_id3    integer NOT NULL,
  int_area_id4    integer NOT NULL,
  name_type            char(2) not null,
  var_name        varchar(255) not null,
  var_name_trans  varchar(255) not null,
  
  int_street_lon integer NOT NULL,
  int_street_lat integer NOT NULL
);

CREATE TABLE xtbl_poi_info
(
  int_poi_id          integer NOT NULL,
  int_poi_lon         integer NOT NULL,
  int_poi_lat         integer NOT NULL,
  int_entry_point_lon integer,
  int_entry_point_lat integer,
  name_type           char(2) not null,
  text_poi_name     text,
  text_phone_number text,
  text_address      text,
  text_postcode     text,
  
  int_important   integer,
  int_genre_code  integer,
  int_mesh_id     integer,
  
  
  int_area_id0    integer NOT NULL,
  int_area_id1    integer NOT NULL,
  int_area_id2    integer NOT NULL,
  int_area_id3    integer NOT NULL,
  int_area_id4    integer NOT NULL,
  text_poi_name_trans  text,
  text_address_trans   text
);

CREATE TABLE xtbl_dealer_data
(
  int_poi_id          integer NOT NULL,
  int_area_id0        integer not null,
  int_poi_lon         integer NOT NULL,
  int_poi_lat         integer NOT NULL,
  int_entry_point_lon integer,
  int_entry_point_lat integer,
  text_poi_name       text,
  text_address        text,
  text_phone_number   text,
  text_postcode       text,
  
  int_important       integer,
  int_genre_code      integer,
  int_mesh_id         integer,
  
  text_poi_name_trans  text,
  text_address_trans   text
)
