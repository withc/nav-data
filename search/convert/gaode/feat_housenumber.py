import convert.feature

class CHouseNumber(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'house_num')
 
    def _domake_key(self):
        sqlcmd = '''
                 insert into temp_road_link( linkid, feattyp, langcode, name ) 
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_feature(self):
        sqlcmd = '''
                 insert into mid_link_road( id, key, type, langcode, name )
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
                 '''
        self.db.do_big_insert( sqlcmd  )

    def _make_hn_by_point(self):
        pass
        