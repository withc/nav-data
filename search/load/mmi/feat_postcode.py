import load.feature

class CPostcode(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'postcode')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into temp_postcode( id, type, org_code )
                    select row_number() over( order by zipcode ), 3136, zipcode
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
                 select 3200, id, type
                   from temp_postcode
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        self._domake_common_postcode()
    
    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass
        