import load.feature

class CPostcode(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'postcode')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into temp_postcode( id, sub, org_code )
                    select row_number() over(), 0, zipcode
                      from (
                            select distinct zipcode from org_city_nw_gc_polyline
                             union
                            select distinct zipcode from org_poi_point
                           ) as a
                    where a.zipcode is not null
                    order by zipcode
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                 insert into mid_feat_key( feat_type, org_id1, org_id2 )
                 select 3200, id, sub
                   from temp_postcode
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                 insert into mid_postcode( key, type, sub, pocode )
                 select f.feat_key, f.feat_type, p.sub, p.org_code
                   from temp_postcode as p
                   join mid_feat_key  as f
                     on p.id = f.org_id1 and p.sub = f.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass
        