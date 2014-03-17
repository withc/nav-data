import load.feature

class CHouseNumber(load.feature.CFeature):
    def __init__(self ):
        print "rdf's house number"
        load.feature.CFeature.__init__(self, 'housenumber')
 
    def _domake_key(self):
        pass
        
    def _domake_feature(self):
        sqlcmd = '''
                   insert into mid_house_number( key, type, sol, scheme, first, last )
                   select f.feat_key, f.feat_type, %d, h.scheme, h.first_address, h.last_address
                     from rdf_road_link     as l
                     join mid_feat_key      as f
                      on  l.link_id = f.org_id1 and f.org_id2 = 2000 
                     join rdf_address_range as h
                       on l.%s_address_range_id = h.address_range_id and 
                          h.first_address is not null
                 '''
        self.db.do_big_insert( sqlcmd % (1, 'left' ) )
        self.db.do_big_insert( sqlcmd % (2, 'right') )
    
    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass
        