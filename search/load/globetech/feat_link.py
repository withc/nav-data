import load.feature

class CLink(load.feature.CFeature):
    def __init__(self ):
        print "globe tech's link"
        load.feature.CFeature.__init__(self, 'link')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 2000, routeid, 2000 
                    from org_l_tran as tr
                 '''
        self.db.execute( sqlcmd )
        
    def _domake_feature(self):
        pass
    
    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass