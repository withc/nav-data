import load.feature

class CPoi(load.feature.CFeature):
    def __init__(self ):
        print "mmi's poi"
        load.feature.CFeature.__init__(self, 'poi')
 
    def _domake_key(self):
        sqlcmd = '''
                     insert into temp_poi_uid( uid,  org_id1, org_id2 )
                     select uid, row_number() over( ), 1000 
                       from org_poi_point
                      order by uid
                 '''
        self.db.execute( sqlcmd )
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 1000, org_id1, org_id2 
                      from temp_poi_uid
                 '''
        self.db.execute( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_poi( key, type, cat_id, imp )
                    select f.feat_key, f.feat_type, 0, p.priority
                      from org_poi_point as p
                      join temp_poi_uid  as t
                        on p.uid     = t.uid
                      join mid_feat_key  as f
                        on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                 '''
        self.db.execute( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select f.feat_key, f.feat_type, 7000, 'P', ST_SetSRID(st_makepoint(p.lon,p.lat), 4326)
                      from org_poi_point as p
                      join temp_poi_uid  as t
                        on p.uid     = t.uid
                      join mid_feat_key  as f
                        on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                 '''
        self.db.execute( sqlcmd )
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select f.feat_key, f.feat_type, 9920, 'P', ST_SetSRID(st_makepoint(p.lon_1,p.lat_1), 4326)
                      from org_poi_point as p
                      join temp_poi_uid  as t
                        on p.uid     = t.uid
                      join mid_feat_key  as f
                        on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                 '''
        self.db.execute( sqlcmd )

    def _domake_name(self):
        sqlcmd = '''
              insert into temp_feat_name( key, type, nametype, langcode, name )
                 '''
        self.db.execute( sqlcmd )
    
    def _domake_attribute(self):
        sqlcmd = '''
                    insert into mid_poi_attr_value( key, type, attr_type, attr_value )
                '''
        self.db.execute( sqlcmd )
        
    def _domake_relation(self):
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype ) 
                 '''
        self.db.execute( sqlcmd )
        