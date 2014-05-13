import load.feature

class CPostcode(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'postcode')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into temp_postcode( id, type, org_code )
                    select row_number() over(), 3136, postcode
                      from ( 
                           select distinct postcode
                             from org_postcode
                            order by postcode
                            ) as t
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                 insert into mid_feat_key( feat_type, org_id1, org_id2 )
                 select 3200, id, type
                   from temp_postcode
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        self._domake_common_postcode()
    
    def _domake_geomtry(self):
        sqlcmd = '''
                 insert into temp_street_geom( key, type, code, geotype, geom )
                 select f.feat_key, f.feat_type, 7379, 'P', ST_Centroid(p.the_geom)
                   from org_postcode             as p
                   join temp_postcode            as t
                     on p.postcode = t.org_code
                   join mid_feat_key             as f
                     on t.id = f.org_id1 and t.type = f.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass
        