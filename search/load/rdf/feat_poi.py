import load.feature

class CPoi(load.feature.CFeature):
    def __init__(self ):
        print "rdf's poi"
        load.feature.CFeature.__init__(self, 'poi')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_poi( key, type, gen_code, imp )
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                 '''
        self.db.do_big_insert( sqlcmd )
        
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
        sqlcmd = '''
                    insert into mid_poi_attr_value( key, type, attr_type, attr_value )
                '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_relation(self):
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype ) 
                 '''
        self.db.do_big_insert( sqlcmd )
        