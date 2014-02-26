-- place
create table rdb_place
(
    id      int     not null,
    type    char(4) not null,
    nmsetid int     not null,
    x       int     not null,
    y       int     not null,
    PRIMARY KEY( id )
);

create table rdb_place_name
(
    id    int          not null,
    name  varchar(256) not null,
    lang  char(3)      not null,
    PRIMARY KEY( id ),
    CONSTRAINT unique_placeName UNIQUE ( name, lang )
);

create table rdb_place_nameset
(
    id    int     not null,
    type  char(2) not null,
    nmid  int     not null,
    PRIMARY KEY( id ),
    FOREIGN KEY (nmid) references rdb_place_name(id)
);

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
-- poi
create table rdb_poi
(
    id      int     not null,
    nmsetid int     not null,
    x       int     not null,
    y       int     not null,
    PRIMARY KEY( id )
);
create table rdb_poi_name
(
    id    int          not null,
    name  varchar(256) not null,
    lang  char(3)      not null,
    PRIMARY KEY( id ),
    CONSTRAINT unique_placeName UNIQUE ( name, lang )
);

create table rdb_poi_nameset
(
    id    int     not null,
    type  char(2) not null,
    nmid  int     not null,
    PRIMARY KEY( id ),
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
    id      int          not null,
    lang    char(3)      not null,
    string  varchar(2048) not null,
);