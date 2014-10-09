import convert.feature

class CPoi(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'poi')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 1000, meshid, poi*10+1  
                      from org_poi
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert  into mid_poi( key, type, gen_code, imp )
                    select  distinct fe.feat_key, fe.feat_type, c.per_code, 0
                      from  org_poi       as p
                      join  mid_feat_key  as fe
                        on  p.meshid = fe.org_id1     and
                            p.poi    = fe.org_id2/10  and
                            fe.org_id2%10 = 1
                      join  temp_org_category as c
                        on  p.poi_type::int = c.org_code
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert  into temp_poi_geom( key, type, code, geotype, geom )
                    select  fe.feat_key, fe.feat_type, 7000, 'P', 
                            ST_SetSRID(st_makepoint( mid_gaode_coord(x_coord), mid_gaode_coord(y_coord)), 4326)
                      from  org_poi       as p
                      join  mid_feat_key  as fe
                        on  p.meshid = fe.org_id1     and
                            p.poi    = fe.org_id2/10  and
                            fe.org_id2%10 = 1
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                    insert into temp_poi_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 9920,'P', 
                            ST_SetSRID(st_makepoint( mid_gaode_coord(x_entr), mid_gaode_coord(y_entr)), 4326)
                      from  org_poi       as p
                      join  mid_feat_key  as fe
                        on  p.meshid = fe.org_id1     and
                            p.poi    = fe.org_id2/10  and
                            fe.org_id2%10 = 1
                     where  x_entr <> 0 and y_entr <> 0
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
                 insert into temp_poi_name( key, type, nametype, langcode, name, tr_lang, tr_name )
                 with poi  
                 as (
                     select fe.feat_key, fe.feat_type, p.name, p.alias, p.meshid
                       from org_poi       as p
                       join mid_feat_key  as fe
                         on p.meshid = fe.org_id1     and
                            p.poi    = fe.org_id2/10  and
                            fe.org_id2%10 = 1
                   )
                 select poi.feat_key, poi.feat_type, 'ON', 'CHI', n.name_chn, 'PYN', n.name_py
                   from poi
                   join org_poiname   as n
                     on poi.name = n.name and poi.meshid = n.meshid
                 union
                 select poi.feat_key, poi.feat_type, 'AN', 'CHI', a.alias_chn, 'PYN', a.alias_py
                   from poi
                   join org_poialias   as a
                     on poi.alias = a.alias and poi.meshid = a.meshid
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        sqlcmd = '''
                insert into mid_poi_address( key, type, lang, name, tr_lang, tr_name, hno )
                select fe.feat_key, fe.feat_type, 'CHI', a.addr_chn, 'PYN', a.addr_py, ''
                  from org_poi       as p
                  join mid_feat_key  as fe
                    on p.meshid = fe.org_id1     and
                       p.poi    = fe.org_id2/10  and
                       fe.org_id2%10 = 1
                  join org_poiaddress  as a
                    on p.addr = a.addr and p.meshid = a.meshid
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                    insert into mid_poi_attr_value( key, type, attr_type, attr_value )
                    with poi  
                    as (
                     select fe.feat_key, fe.feat_type, p.district, p.telephone, p.mobile, p.fax 
                       from org_poi       as p
                       join mid_feat_key  as fe
                         on p.meshid = fe.org_id1     and
                            p.poi    = fe.org_id2/10  and
                            fe.org_id2%10 = 1
                     )
                    select p.feat_key, p.feat_type, 'TL', p.district||'-'||regexp_split_to_table(p.telephone,E'\\\\|')
                      from poi as p
                      where p.telephone is not null
                    union all
                    select p.feat_key, p.feat_type, 'TL', p.mobile
                      from poi as p
                      where p.mobile is not null
                    union all
                    select p.feat_key, p.feat_type, 'TX', p.fax
                      from poi as p
                      where p.fax is not null
                '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_relation(self):
        #poi to place
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select f0.feat_key, f0.feat_type, 7001, f1.feat_key, f1.feat_type
                    from org_poi       as p
                    join mid_feat_key  as f0
                      on p.meshid = f0.org_id1     and
                         p.poi    = f0.org_id2/10  and
                         f0.org_id2%10 = 1
                    join mid_feat_key          as f1
                      on p.ad_code::int = f1.org_id1 and ( f1.feat_type = 3010 or f1.feat_type = 3009 )
                 '''
        self.db.do_big_insert( sqlcmd )
        #poi to postcode
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select f0.feat_key, f0.feat_type, 7004, m.key, m.type
                    from org_poi       as p
                    join mid_feat_key  as f0
                      on p.meshid = f0.org_id1     and
                         p.poi    = f0.org_id2/10  and
                         f0.org_id2%10 = 1
                    join mid_postcode  as m
                      on p.postcode = m.pocode
                 '''
        self.db.do_big_insert( sqlcmd )

    def _domake_name_geom(self): 
        self._gen_nameid( 'poi' )
        self._gen_geomid( 'poi' )
          