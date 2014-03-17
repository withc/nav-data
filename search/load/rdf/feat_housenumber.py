import load.feature

class CHouseNumber(load.feature.CFeature):
    def __init__(self ):
        print "rdf's house number"
        load.feature.CFeature.__init__(self, 'house_num')
 
    def _domake_key(self):
        sqlcmd = '''
                 insert into temp_road_link( linkid, nameid )
                 select r.link_id, r.road_name_id
                   from rdf_road_link     as r
                   join rdf_address_range as hl
                     on r.left_address_range_id = hl.address_range_id
                   join rdf_address_range as hr
                     on r.right_address_range_id = hr.address_range_id
                  where  
                        hl.first_address is not null or
                        hr.first_address is not null
                  union
                  select r.link_id, r.road_name_id
                    from rdf_road_link     as r
                    join rdf_address_point as p
                      on r.road_link_id = p.road_link_id
                    where r.road_name_id is not null and
                          p.address is not null
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_feature(self):
        sqlcmd = '''
                 insert into mid_house_number_road( id, key, type, langcode, name )
                 select t.id, f.feat_key, f.feat_type, n.language_code, n.street_name
                   from temp_road_link    as t
                   join mid_feat_key      as f
                     on t.linkid = f.org_id1 and f.org_id2 = 2000
                   join rdf_road_name     as n
                     on t.nameid = n.road_name_id
                 '''
        self.db.do_big_insert( sqlcmd )
        
       
    
        
    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        self._make_hn_by_link()
        self._make_hn_by_point()
        
    def _domake_relation(self):
        pass
    
    def _make_hn_by_link(self):
        sqlcmd = '''
                   insert into mid_address_range( id, side, scheme, first, last )
                   select t.id, %d, h.scheme, h.first_address, h.last_address
                     from temp_road_link     as t
                     join rdf_road_link      as l
                       on t.linkid = l.link_id and t.nameid = l.road_name_id 
                     join rdf_address_range as h
                       on l.%s_address_range_id = h.address_range_id and 
                          h.first_address is not null
                 '''
        self.db.do_big_insert( sqlcmd % (1, 'left' ) )
        self.db.do_big_insert( sqlcmd % (2, 'right') )
    
    def _make_hn_by_point(self):
        sqlcmd = '''
                insert into mid_address_point( id, side, num, x, y, dis_x, dis_y )
                select t.id, 
                       case
                          when p.side = 'R' then 2
                          else 1
                       end, 
                       p.address, p.lon, p.lat, p.display_lon, p.display_lat
                  from rdf_address_point as p
                  join rdf_road_link     as l
                    on p.road_link_id= l.road_link_id
                  join temp_road_link    as t
                       on l.link_id = t.linkid and l.road_name_id = t.nameid 
                '''
        self.db.do_big_insert( sqlcmd )
        