DROP TABLE IF EXISTS rdb_place          CASCADE;
DROP TABLE IF EXISTS rdb_place_name      CASCADE;
DROP TABLE IF EXISTS rdb_place_nameset   CASCADE;
DROP TABLE IF EXISTS rdb_place_admin     CASCADE;
DROP TABLE IF EXISTS rdb_place_in_place  CASCADE;
DROP TABLE IF EXISTS rdb_placeset        CASCADE;

DROP TABLE IF EXISTS rdb_category          CASCADE;
DROP TABLE IF EXISTS rdb_poi               CASCADE;
DROP TABLE IF EXISTS rdb_poi_name          CASCADE;
DROP TABLE IF EXISTS rdb_poi_nameset       CASCADE;
DROP TABLE IF EXISTS rdb_poi_to_content    CASCADE;
DROP TABLE IF EXISTS rdb_poi_contentstring CASCADE;

DROP TABLE IF EXISTS rdb_link              CASCADE;
DROP TABLE IF EXISTS rdb_link_name         CASCADE;
DROP TABLE IF EXISTS rdb_link_nameset      CASCADE;

DROP TABLE IF EXISTS rdb_road              CASCADE;
DROP TABLE IF EXISTS rdb_road_link         CASCADE;
--------------------------------------------------
-- place
-------------------------------------------------
create table rdb_place
(
    id      int      not null PRIMARY KEY,
    type    smallint not null,
    nmsetid int      not null,
    x       int      not null,
    y       int      not null
);

create table rdb_place_name
(
    id    int          not null PRIMARY KEY,
    lang  char(3)      not null,
    name  varchar(256) not null
);

create table rdb_place_nameset
(
    id    int      not null,
    seq   smallint not null,
    type  char(2)  not null,
    nmid  int      not null,
    
    FOREIGN KEY (nmid) references rdb_place_name(id)
);

create table rdb_place_admin
(
    id     int not null PRIMARY KEY,
    type   smallint not null,
    a0     int not null,
    a1     int not null,
    a2     int not null,
    a7     int not null,
    a8     int not null,
    a9     int not null
);
--
-- 
create table rdb_place_in_place
(
    cid    int not null,
    pid    int not null
);

create table rdb_placeset
(
    id     int not null,
    seq    int not null,
    plid   int not null,
    PRIMARY KEY( id )
);

-- poi category
create table rdb_category
(
    id         int not null,
    parent_id  int not null,
    name       varchar(70) not null,
    PRIMARY KEY( id )
);

--------------------------------------------------
-- poi
-------------------------------------------------
create table rdb_poi
(
    id      int     not null PRIMARY KEY,
    catid   bigint  not null,
    nmsetid int     not null,
    imp     int     not null,
    x       int     not null,
    y       int     not null
);
create table rdb_poi_name
(
    id    int          not null PRIMARY KEY,
    name  varchar(256) not null,
    lang  char(3)      not null,
    
    CONSTRAINT unique_placeName UNIQUE ( name, lang )
);

create table rdb_poi_nameset
(
    id    int     not null,
    seq   smallint not null,
    type  char(2) not null,
    nmid  int     not null,

    FOREIGN KEY (nmid) references rdb_poi_name(id)
);
-- poi content
create table rdb_poi_to_content
(
    id        int          not null,
    type      varchar(128) not null,
    seq       int          not null,
    contentid int          not null
);

create table rdb_poi_contentstring
(
    id      int           not null,
    lang    char(3)       not null,
    string  varchar(2048) not null
);
--------------------------------------------------
-- link
-------------------------------------------------
create table rdb_link
(
    id         int not null PRIMARY KEY,
    left_pid   int not null,
    right_pid  int not null,
    nmsetid    int not null
);

create table rdb_link_name
(
    id    int          not null PRIMARY KEY,
    name  varchar(256) not null,
    lang  char(3)      not null
);

create table rdb_link_nameset
(
    id    int     not null,
    seq   smallint not null,
    type  char(2) not null,
    nmid  int     not null
);

create table rdb_link_hno_range
(
    link_id  int          not null,
    nmid     int          not null,
    side     smallint     not null CONSTRAINT valid_sol    CHECK (side IN (1,2)),
    scheme   char(1)      not null CONSTRAINT valid_scheme CHECK (scheme IN ('M', 'O', 'E','$')),
    format   char(1)      not null,
    first    varchar(128) not null,
    last     varchar(128) not null
);

create table rdb_link_hno_point
(
    link_id  int          not null,
    nmid     int          not null,
    side     smallint     not null CONSTRAINT valid_sol    CHECK (side IN (1,2)),
    format   char(1)      not null,
    hno      varchar(128) not null,
    x        int          not null,
    y        int          not null,
    en_x     int          ,
    en_y     int              
);
--------------------------------------------------
-- road
-------------------------------------------------
create table rdb_road
(
    id       int not null,
    placeid  int not null,
    nameid  int not null,
    x        int not null,
    y        int not null
);

create table rdb_road_link
(
    id       int not null,
    seq      int not null,
    linkid   int not null
);
-------------------------------------
-- temp table 
------------------------------------
DROP TABLE IF EXISTS tmp_place_name_id    CASCADE;
DROP TABLE IF EXISTS tmp_place_id         CASCADE;

create table tmp_place_name_id
( 
  name_id    int      not null,
  key        bigint   not null,
  type       smallint not null
);

create table tmp_place_id
( 
  place_id  int      not null,
  key       bigint   not null,
  type      smallint not null
);
