import load.feature

class CHouseNumber(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'house_num')
 
    def _domake_key(self):
        pass
    
    def _domake_feature(self):
        sqlcmd = '''
                 
                 '''
        #self.db.do_big_insert( sqlcmd )

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
        pass

    def _make_hn_by_point(self):
        pass
        