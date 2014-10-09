import convert.feature

class CPostcode(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'postcode')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into temp_postcode( id, type, iso, org_code )
                    select row_number() over(), 3136, 'CHN', postcode
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
                 select m.key, m.type, 7379, 'P', ST_SetSRID(st_makepoint( mid_gaode_coord(x_coord), mid_gaode_coord(y_coord) ), 4326)
                   from org_postcode  as p
                   join mid_postcode  as m
                     on p.postcode = m.pocode
                   
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
                  select distinct m.key , m.type, 7001, fe.feat_key, fe.feat_type
                    from (
                          select postcode, unnest(string_to_array( ad_codes, '|' )) as ad_code
                            from org_postcode  
                         ) as p
                    join mid_postcode  as m
                      on p.postcode = m.pocode
                    join mid_feat_key   as fe
                      on p.ad_code::int = fe.org_id1 and ( fe.feat_type = 3010 or fe.feat_type = 3009 )
                     order by m.key
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name_geom(self): 
        self._gen_nameid( 'place' )
        self._gen_geomid( 'place' )