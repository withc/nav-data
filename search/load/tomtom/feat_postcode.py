import load.feature

class CPostcode(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'postcode')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into temp_postcode( id, type, iso, org_code )
                    select row_number() over( order by zipcode ), 3136, order00, zipcode
                      from (
                            select order00, postcode as zipcode
                              from org_pi  as p
                              join org_sa as sa
                                on p.id = sa.id and p.feattyp = sa.feattyp
                              join (
                                     select id, feattyp, order00 from org_a8
                                     union
                                     select id, feattyp, order00 from org_a9
                                    ) as a
                                on sa.areid = a.id and sa.aretyp = a.feattyp
                              where postcode is not null
                            union
                            select order00, postcode as zipcode
                              from org_mnpoi_piad  as p
                              join org_mnpoi_pisa  as sa
                                on p.id = sa.id and p.feattyp = sa.poityp
                              join (
                                     select id, feattyp, order00 from org_a8
                                     union
                                     select id, feattyp, order00 from org_a9
                                    ) as a
                                on sa.areid = a.id and sa.aretyp = a.feattyp
                              where postcode is not null
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
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass
        