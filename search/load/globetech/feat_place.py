import load.feature

class CPlace(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'place')
 
    def _domake_key(self):
        # add country by myself
        sqlcmd = ''' insert into mid_feat_key( feat_type, org_id1, org_id2 ) 
                     values( 3001, 0, 0 )
                 '''
        self.db.do_big_insert( sqlcmd )
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
                    select case org_id2
                             when 1 then 3002
                             when 2 then 3009
                             when 3 then 3010
                             else 0
                            end,
                            org_id1,
                            org_id2
                       from temp_admincode
                      order by type, prov_code, amp_code, tam_code
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
        # add the country point by myself
        self.db.do_big_insert( ''' insert into temp_feat_geom( key, type, code, geotype, geom )
                             select key, type, 7379, 'P',  ST_SetSRID(st_makepoint(100.5018272, 13.7541276), 4326)
                               from mid_place where type = 3001
                         ''' )
        sqlcmd = '''
             insert into temp_feat_geom( key, type, code, geotype, geom )
                  select fe.feat_key, fe.feat_type, 7379, 'P', a.the_geom
                    from org_admin_point as a
                    join temp_admincode  as ta
                      on a.type      = ta.type
                     and a.prov_code = ta.prov_code
                     and a.amp_code  = ta.amp_code
                     and a.tam_code  = ta.tam_code
                    join mid_feat_key     as fe
                      on ta.org_id1 = fe.org_id1 and ta.org_id2 = fe.org_id2
                 ''' 
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        # add the country name by myself
        self.db.do_big_insert( ''' insert into temp_feat_name( key, type, nametype, langcode, name, tr_lang, tr_name )
                             select key, type, 'ON', 'THA', '\xe0\xb9\x84\xe0\xb8\x97\xe0\xb8\xa2',
                                    'ENG', 'Thailand'
                               from mid_place where type = 3001
                         ''' )
        
        sqlcmd = '''
             insert into temp_feat_name( key, type, nametype, langcode, name, tr_lang, tr_name )
                with ad ( key, type, namt, name )
                as (select fe.feat_key, fe.feat_type,  a.namt, a.name
                    from org_admin_point as a
                    join temp_admincode  as ta
                      on a.type      = ta.type
                     and a.prov_code = ta.prov_code
                     and a.amp_code  = ta.amp_code
                     and a.tam_code  = ta.tam_code
                    join mid_feat_key     as fe
                      on ta.org_id1 = fe.org_id1 and ta.org_id2 = fe.org_id2
                    )
                  select key, type, 'ON', 'THA', namt, 'ENG', name from ad
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
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
        
        