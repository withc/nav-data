import load.feature

class CPlace(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'place')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into temp_admincode( type, prov_code, amp_code, tam_code, org_id1, org_id2 )
                    select distinct 
                           type, prov_code, amp_code, tam_code,
                           mid_globetech_org1(type,prov_code,amp_code,tam_code), type
                      from org_admin_point
                     order by type, prov_code, amp_code, tam_code
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 3001, id, type
                      from org_country
                    union all
                    (select case org_id2
                              when 1 then 3002
                              when 2 then 3009
                              when 3 then 3010
                              else 0
                            end,
                            org_id1,
                            org_id2
                       from temp_admincode
                      order by type, prov_code, amp_code, tam_code
                      )
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                 insert into  mid_place( key, type )
                      select  feat_key, feat_type 
                        from  mid_feat_key
                       where  3001 <= feat_type and feat_type <= 3010
                    order by  feat_type, feat_key
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        # add the country point
        self.db.do_big_insert( ''' insert into temp_street_geom( key, type, code, geotype, geom )
                             select f.feat_key, f.feat_type, 7379, 'P',  ST_SetSRID(st_makepoint(c.lon, c.lat), 4326)
                               from org_country  as c
                               join mid_feat_key as f
                                 on f.feat_type = 3001 and c.id = f.org_id1 and c.type = f.org_id2
                         ''' )
        # there  are more then one point for some city, we just select the first one
        sqlcmd = '''
             insert into temp_street_geom( key, type, code, geotype, geom )
             select feat_key, feat_type, 7379, 'P', the_geom
               from (
                  select fe.feat_key, fe.feat_type,  a.the_geom,
                         row_number() over (partition by fe.feat_key order by a.gid ) as seq
                    from org_admin_point as a
                    join temp_admincode  as ta
                      on a.type      = ta.type       and
                         a.prov_code = ta.prov_code  and
                         a.amp_code  = ta.amp_code   and
                         a.tam_code  = ta.tam_code
                    join mid_feat_key     as fe
                      on ta.org_id1 = fe.org_id1 and ta.org_id2 = fe.org_id2
                      ) as t
                 where seq = 1
                 ''' 
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        # add the country name by myself
        self.db.do_big_insert( ''' 
                      insert into temp_street_name( key, type, group, nametype, langcode, name )
                      with tb (key, type, group, nametype, lang, name, tr_lang, tr_name )as (
                      select f.feat_key, f.feat_type, 1, 'ON', 'THA', c.namt, 'ENG', c.name
                        from org_country  as c
                        join mid_feat_key as f
                          on f.feat_type = 3001 and c.id = f.org_id1 and c.type = f.org_id2
                          )
                          select key, type, group, nametype, lang, name from tb
                          union
                          select key, type, group, 'TN', tr_lang, tr_name from tb
                      ''' )
        
        sqlcmd = '''
              insert into temp_street_name( key, type, nametype, langcode, name, tr_lang, tr_name )
              select feat_key, feat_type, case seq when 1 then 'ON' else 'AN' end, 'THA', namt, 'ENG', name 
                from (
                  select fe.feat_key, fe.feat_type,  a.namt, a.name,
                         row_number() over (partition by fe.feat_key order by a.gid ) as seq
                    from org_admin_point as a
                    join temp_admincode  as ta
                      on a.type      = ta.type
                     and a.prov_code = ta.prov_code
                     and a.amp_code  = ta.amp_code
                     and a.tam_code  = ta.tam_code
                    join mid_feat_key     as fe
                      on ta.org_id1 = fe.org_id1 and ta.org_id2 = fe.org_id2
                    ) as t
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        sqlcmd = '''
                 insert into mid_country_profile( iso, off_lang, key, type )
                 select 'THA', 'THA', f.feat_key, f.feat_type
                   from mid_feat_key as f
                  where feat_type = 3001
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                 insert into mid_full_area( min_lon, min_lat, max_lon, max_lat )
                 select st_xmin(geom)*100000, st_ymin(geom)*100000, 
                        st_xmax(geom)*100000, st_ymax(geom)*100000
                   from ( select ST_extent(the_geom) as geom from org_admin_poly ) as a
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_relation(self):
        # add the country admin by myself
        self.db.do_big_insert( ''' insert into mid_place_admin( key, type, a0, a1, a2, a7, a8, a9 )
                             select key, type, key, 0,0,0,0,0
                               from mid_place where type = 3001
                         ''' )
        sqlcmd = '''
              insert into mid_place_admin( key, type, a0, a1, a2, a7, a8, a9 )
              with ad ( f_key, f_type, type, prov_code, amp_code, tam_code )
                as (
                  select fe.feat_key, fe.feat_type, ta.type, ta.prov_code, ta.amp_code, ta.tam_code
                    from temp_admincode  as ta
                    join mid_feat_key     as fe
                      on ta.org_id1 = fe.org_id1 and ta.org_id2 = fe.org_id2
                    ) 
              select a1.f_key, a1.f_type, ( select key from mid_place where type = 3001 ) , a1.f_key, 0, 0, 0, 0
                from ad as a1
               where a1.type = 1
               union
              select  a8.f_key, a8.f_type, ( select key from mid_place where type = 3001 ) , a1.f_key, 0, 0,a8.f_key, 0
                from ad as a8
                join ad as a1
                  on a1.type      = 1            and 
                     a1.prov_code = a8.prov_code
               where a8.type      = 2
               union
              select  a9.f_key, a9.f_type, ( select key from mid_place where type = 3001 ) , a1.f_key, 0, 0,a8.f_key, a9.f_key
                from ad as a9
                join ad as a1
                  on a1.type      = 1            and 
                     a9.prov_code = a1.prov_code
                join ad as a8
                  on a8.type      = 2            and 
                     a9.prov_code = a8.prov_code and
                     a9.amp_code  = a8.amp_code
               where a9.type      = 3
           '''
        self.db.do_big_insert( sqlcmd )
        
        