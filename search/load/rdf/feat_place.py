import load.feature

class CPlace(load.feature.CFeature):
    def __init__(self ):
        print "rdf's place"
        load.feature.CFeature.__init__(self, 'place')
 
    def _domake_key(self):
  
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                 insert into  mid_place( key, type ) 
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):

        sqlcmd = '''
             insert into temp_feat_geom( key, type, code, geotype, geom ) 
                 ''' 
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        
        sqlcmd = '''
                 insert into temp_feat_name( key, type, nametype, langcode, name )
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        sqlcmd = '''
                insert into mid_place_admin( key, type, a0, a1, a2, a7, a8, a9 )
                '''
        self.db.do_big_insert( sqlcmd )
        
        