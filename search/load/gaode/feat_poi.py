import load.feature

class CPoi(load.feature.CFeature):
    def __init__(self ):
        print "gaode's poi"
        load.feature.CFeature.__init__(self, 'poi')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 1000, meshid, poi  
                      from org_poi
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert  into mid_poi( key, type, gen_code, imp )
                    select  distinct fe.feat_key, fe.feat_type, c.per_code, 0
                      from  org_poi       as p
                      join  mid_feat_key  as fe
                        on  p.meshid = fe.org_id1 and p.poi = fe.org_id2
                      join  temp_org_category as c
                        on  p.poi_type::int = c.org_code
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert  into temp_feat_geom( key, type, code, geotype, geom )
                    select  fe.feat_key, fe.feat_type, 7000, 'P', 
                            ST_SetSRID(st_makepoint( mid_gaode_coord(x_coord), mid_gaode_coord(y_coord)), 4326)
                      from  org_poi       as p
                      join  mid_feat_key  as fe
                        on  p.meshid = fe.org_id1 and p.poi = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 9920,'P', 
                            ST_SetSRID(st_makepoint( mid_gaode_coord(x_entr), mid_gaode_coord(y_entr)), 4326)
                      from  org_landmark  as p
                      join  mid_feat_key  as fe
                        on  p.objectid = fe.org_id1 and fe.org_id2 = 1000
                     where  x_entr <> 0 and y_entr <> 0
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
        