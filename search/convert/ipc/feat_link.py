import convert.feature

class CLink(convert.feature.CFeature):
    def __init__(self ):
        print "jpc's link"
        convert.feature.CFeature.__init__(self, 'link')
 
    def _domake_key(self):
        sqlcmd = '''
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
  
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        sqlcmd = '''
                 '''
        self.db.do_big_insert( sqlcmd )
        