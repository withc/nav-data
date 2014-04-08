import entity

class CXTblData(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'xtbl_data')
          
    def _do(self):
        self.db.run( r'.\config\xtbl_db.sql' )
        self._do_city()
        self._do_street()
        self._do_poi()
        
    def _do_city(self):
        sqlcmd = '''
                 insert into xtbl_city_info( int_area_id1, int_area_id2, int_area_id3, var_name, int_area_lon, int_area_lat, full_name )
                 select  c.area1, c.area2, c.area3, n.name, c.lon, c.lat, ''
                   from tbl_city_info  as c
                   join tbl_city_name  as n
                     on c.area0 = n.area0 and 
                        c.area1 = n.area1 and 
                        c.area2 = n.area2 and 
                        c.area3 = n.area3 and
                        n.lang = (select off_lang from mid_country_profile )
                 '''
        self.db.do_big_insert(sqlcmd)
    
    def _do_street(self):
        sqlcmd = '''
                 insert into xtbl_street_info( int_street_id, int_area_id1, int_area_id2, int_area_id3, var_name, int_street_lon, int_street_lat )
                 select s.id, s.area1,  s.area2, s.area3, n.name, s.lon, s.lat
                   from tbl_street_info  as s
                   join tbl_street_name  as n
                     on s.id = n.id and 
                        n.lang = ( select off_lang from mid_country_profile )
                 '''
        self.db.do_big_insert(sqlcmd)
    
    def _do_poi(self):
        sqlcmd = '''
                 insert into xtbl_poi_info( int_poi_id, int_poi_lon, int_poi_lat, int_entry_point_lon, int_entry_point_lat,
                           text_poi_name, text_phone_number, text_address, text_postcode,
                           int_genre_code, int_important, 
                           int_area_id1, int_area_id2, int_area_id3, int_mesh_id )
                 select p.id, p.lon, p.lat, p.entry_lon, p.entry_lat, n.name, p.tel, 
                        case
                           when a.hno <> '' then a.hno || ',' || a.street
                           else a.street
                        end, p.postcode, (p.gen1<<24)+(p.gen2<<16)+p.gen3, p.imp,
                        p.area1, p.area2, p.area3, p.meshid
                   from tbl_poi_info    as p
              left join tbl_poi_address as a
                     on p.id = a.id
              left join tbl_poi_name    as n
                     on p.id = n.id and n.type = 'ON'
                  order by n.name
                 '''
        self.db.do_big_insert(sqlcmd)
    
        
