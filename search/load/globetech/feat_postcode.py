import load.feature

class CPostcode(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'postcode')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into temp_postcode( id, type, iso, org_code )
                    select row_number() over(), 3136, 'THA', postcode
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
                 insert into temp_place_geom( key, type, code, geotype, geom )
                 select f.feat_key, f.feat_type, 7379, 'P', ST_Centroid(p.the_geom)
                   from ( 
                           select postcode, the_geom, 
                                  row_number() over ( partition by postcode order by st_area(the_geom) desc ) as seq
                             from org_postcode
                        )  as p
                   join temp_postcode            as t
                     on p.postcode = t.org_code and p.seq = 1
                   join mid_feat_key             as f
                     on t.id = f.org_id1 and t.type = f.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        # postcode to place
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select distinct pc.key , pc.type, 7001, fe.feat_key, fe.feat_type
                    from org_admin_point      as ap
                    join mid_postcode         as pc
                      on ap.postcode = pc.pocode and ap.type = 3
                    join temp_admincode       as ta
                      on ap.type      = ta.type       and
                         ap.prov_code = ta.prov_code  and
                         ap.amp_code  = ta.amp_code   and
                         ap.tam_code  = ta.tam_code
                    join mid_feat_key          as fe
                      on ta.org_id1 = fe.org_id1 and ta.org_id2 = fe.org_id2
                     order by pc.key
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name_geom(self): 
        self._gen_nameid( 'place' )
        self._gen_geomid( 'place' )
        