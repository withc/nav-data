import load.feature

class CPlace(load.feature.CFeature):
    def __init__(self ):
        print "globe tech's place"
        load.feature.CFeature.__init__(self, 'place')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select distinct
                           case type
                             when 1 then 3002
                             when 2 then 3009
                             when 3 then 3010
                            end,
                            case type
                              when 1 then prov_code::integer*10000
                              when 2 then prov_code::integer*10000 + amp_code::integer*100
                              when 3 then prov_code::integer*10000 + amp_code::integer*100 + tam_code::integer
                            end,
                            type
                    from org_admin_point
                    order by 3, 2
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