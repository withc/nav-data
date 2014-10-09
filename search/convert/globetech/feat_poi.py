import convert.feature

class CPoi(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'poi')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select distinct 1000, objectid, 1000 
                      from org_landmark
                     where prov_code is not null
                     order by objectid
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert  into mid_poi( key, type, gen_code, imp )
                    select  distinct fe.feat_key, fe.feat_type, c.per_code, 0
                      from  org_landmark  as p
                      join  mid_feat_key  as fe
                        on  p.objectid = fe.org_id1 and fe.org_id2 = 1000
                      join  temp_org_category as c
                        on  p.sub_code::int = c.org_code
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert  into temp_poi_geom( key, type, code, geotype, geom )
                    select  distinct fe.feat_key, fe.feat_type, 7000,'P', p.the_geom
                      from  org_landmark  as p
                      join  mid_feat_key  as fe
                        on  p.objectid = fe.org_id1 and fe.org_id2 = 1000
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                    insert into temp_poi_geom( key, type, code, geotype, geom )
                    select  distinct fe.feat_key, fe.feat_type, 9920,'P', 
                            case
                              when p.guide_x1 <> 0 then ST_SetSRID(st_makepoint(guide_x1, guide_y1), 4326)
                              when p.guide_x2 <> 0 then ST_SetSRID(st_makepoint(guide_x2, guide_y2), 4326)
                              when p.guide_x3 <> 0 then ST_SetSRID(st_makepoint(guide_x3, guide_y3), 4326)
                            end   
                      from  org_landmark  as p
                      join  mid_feat_key  as fe
                        on  p.objectid = fe.org_id1 and fe.org_id2 = 1000
                     where  p.guide_x1 <> 0 or p.guide_x2 <> 0 or p.guide_x3 <> 0
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
              insert into temp_poi_name( key, type, nametype, langcode, name, tr_lang, tr_name )
                with pn ( key, type, namt, name, seq )
                as (
                     select fe.feat_key, fe.feat_type, p.nav_namt, mid_globetech_eng_name(p.nav_name),
                            row_number() over ( partition by fe.feat_key order by p.gid ) as seq
                       from (
                               select objectid, nav_namt, nav_name, min(gid) as gid
                                 from org_landmark
                                 group by objectid, nav_namt, nav_name
                            ) as p
                       join mid_feat_key   as fe
                         on p.objectid = fe.org_id1 and fe.org_id2 = 1000
                    )
                select key, type, case seq when 1 then 'ON' else 'AN' end, 'THA', namt, 'ENG', name from pn
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_attribute(self):
        # org_landmark have same poi but set different poi name,
        # about other attribute, we must distinct the record.
        sqlcmd = '''
                insert into mid_poi_address( key, type, lang, name, tr_lang, tr_name, hno )
                select distinct fe.feat_key, fe.feat_type, 'THA', p.location_t, 'ENG', p.location_e,
                       COALESCE(p.hno,'')
                  from org_landmark as p
                  join mid_feat_key as fe
                    on p.location_t is not null and p.objectid = fe.org_id1 and fe.org_id2 = 1000
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                    insert into mid_poi_attr_value( key, type, attr_type, attr_value )
                    select fe.feat_key, fe.feat_type, 'TL', p.tel
                      from org_landmark as p
                      join mid_feat_key as fe
                        on p.tel is not null and p.objectid = fe.org_id1 and fe.org_id2 = 1000
                '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_relation(self):
        # poi to place
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select distinct f0.feat_key, f0.feat_type, 7001, f1.feat_key, f1.feat_type
                    from org_landmark    as p
                    join mid_feat_key    as f0
                      on p.objectid = f0.org_id1 and f0.org_id2 = 1000
                    join temp_admincode  as ta
                      on 3           = ta.type
                     and p.prov_code = ta.prov_code
                     and p.amp_code  = ta.amp_code
                     and p.tam_code  = ta.tam_code
                    join mid_feat_key     as f1
                      on ta.org_id1 = f1.org_id1 and ta.org_id2 = f1.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        # poi to postcode
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select distinct f0.feat_key, f0.feat_type, 7004, po.key, po.type
                    from org_landmark    as p
                    join mid_feat_key    as f0
                      on p.objectid = f0.org_id1 and f0.org_id2 = 1000
                    join mid_postcode  as po
                      on p.postcode = po.pocode
                 '''
        self.db.do_big_insert( sqlcmd )
        
        # poi to link
        
        
    def _domake_name_geom(self): 
        self._gen_nameid( 'poi' )
        self._gen_geomid( 'poi' )
        
        