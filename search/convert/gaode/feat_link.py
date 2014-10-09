import convert.feature

class CLink(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'link')
 
    def _domake_key(self):
        # about org_id2, we use a trick to make sure org_id1+org_id2 is uniqueness.
        sqlcmd = '''
                 insert into mid_feat_key( feat_type, org_id1, org_id2 )
                 select 2000, meshid, road*10+2
                   from org_roadsegment
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                 insert into mid_link( key, type )
                 select f.feat_key, f.feat_type
                   from org_roadsegment   as r
                   join mid_feat_key      as f
                     on r.meshid = f.org_id1     and 
                        r.road   = f.org_id2/10  and
                        f.org_id2%10 = 2   
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert into temp_street_geom( key, type, code, geotype, geom )
                    select f.feat_key, f.feat_type, 7000,'L', ST_Scale( ST_LineMerge(r.the_geom), 1.0/3600, 1.0/3600 )
                      from org_roadsegment   as r
                      join mid_feat_key      as f
                        on r.meshid = f.org_id1     and 
                           r.road   = f.org_id2/10  and
                           f.org_id2%10 = 2
                           
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
                 insert into temp_street_name( key, type, nametype, langcode, name, tr_lang, tr_name )
                 select f.feat_key, f.feat_type, 'ON', 'CHI', name_chn, 'PYN', name_py
                   from org_roadsegment   as r
                   join mid_feat_key      as f
                     on r.meshid = f.org_id1     and 
                        r.road   = f.org_id2/10  and
                        f.org_id2%10 = 2
                  where name_chn is not null
    
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_attribute(self):
        pass
    
    def _domake_relation(self):
        # link to place
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select f0.feat_key, f0.feat_type, 7001, f1.feat_key, f1.feat_type
                    from org_roadsegment       as r
                    join mid_feat_key          as f0
                      on r.meshid = f0.org_id1     and 
                         r.road   = f0.org_id2/10  and
                         f0.org_id2%10 = 2
                    join mid_feat_key          as f1
                      on r.ad_code::int = f1.org_id1 and ( f1.feat_type = 3010 or f1.feat_type = 3009 )
                 '''
        self.db.do_big_insert( sqlcmd )
        
       
    def _domake_name_geom(self): 
        self._gen_nameid( 'street' )
        self._gen_geomid( 'street' )
        