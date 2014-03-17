import load.feature

class CHouseNumber(load.feature.CFeature):
    def __init__(self ):
        print "rdf's house number"
        load.feature.CFeature.__init__(self, 'house_num')
 
    def _domake_key(self):
        pass
    
    def _domake_feature(self):
        self._make_hn_by_link()
        self._make_hn_by_point()
       
    def _make_hn_by_link(self):
        sqlcmd = '''
                   insert into mid_house_number( key, type, side, scheme, first, last )
                   select f.feat_key, f.feat_type, %d, h.scheme, h.first_address, h.last_address
                     from rdf_road_link     as l
                     join mid_feat_key      as f
                       on l.link_id = f.org_id1 and f.org_id2 = 2000 
                     join rdf_address_range as h
                       on l.%s_address_range_id = h.address_range_id and 
                          h.first_address is not null
                 '''
        self.db.do_big_insert( sqlcmd % (1, 'left' ) )
        self.db.do_big_insert( sqlcmd % (2, 'right') )
    
    def _make_hn_by_point(self):
        sqlcmd = '''
                insert into mid_address_point( key, type, side, num, x, y, dis_x, dis_y )
                select f.feat_key, f.feat_type, 
                       case
                          when p.side = 'R' then 2
                          else 1
                       end, 
                       p.address, p.lon, p.lat, p.display_lon, p.display_lat
                  from rdf_address_point as p
                  join rdf_road_link     as l
                    on p.road_link_id= l.road_link_id
                  join mid_feat_key      as f
                       on l.link_id = f.org_id1 and f.org_id2 = 2000 
                '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass
        