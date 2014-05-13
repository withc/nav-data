import load.feature

class CPostcode(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'postcode')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into temp_postcode( id, type, org_code )
                    select row_number() over( order by country_id, zipcode ), 3136, zipcode
                      from (
                            select country_id, postal_code as zipcode
                              from rdf_poi_address where postal_code is not null
                            union
                            select country_id, actual_postal_code as zipcode
                              from rdf_poi_address where actual_postal_code is not null
                            union
                            select country_id, postal_code as zipcode
                              from rdf_postal_area
                            union
                            select c.country_id, full_postal_code as zipcode
                              from rdf_postal_code_midpoint as p
                              join rdf_country              as c
                                on p.iso_country_code = c.iso_country_code
                           ) as a
                    where a.zipcode is not null
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
                 select f.feat_key, f.feat_type, 7379, 'P', 
                        ST_SetSRID(st_makepoint( p.lon/100000.0, p.lat/100000.0 ), 4326)
                   from rdf_postal_code_midpoint as p
                   join temp_postcode            as t
                     on p.full_postal_code = t.org_code
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
        