import load.feature

class CPostcode(load.feature.CFeature):
    def __init__(self ):
        print "mmi's postcode"
        load.feature.CFeature.__init__(self, 'postcode')
 
    def _domake_key(self):
        sqlcmd = '''
                 '''
        self.db.execute( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                 '''
        self.db.execute( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                 '''
        self.db.execute( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
  
                 '''
        self.db.execute( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        sqlcmd = '''
                 '''
        self.db.execute( sqlcmd )
        