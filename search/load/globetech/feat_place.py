import load.feature

class CPlace(load.feature.CFeature):
    def __init__(self ):
        print "globe tech's place"
        load.feature.CFeature.__init__(self, 'place')
 
    def _domake_key(self):
        # add country by myself
        sqlcmd = ''' insert into mid_feat_key( feat_type, org_id1, org_id2 ) 
                     values( 3001, 0, 0 )
                 '''
        self.db.execute( sqlcmd )
        sqlcmd = '''
                    insert into temp_admincode( type, prov_code, amp_code, tam_code, org_id1, org_id2 )
                    select distinct 
                           type, prov_code, amp_code, tam_code,
                           mid_globetech_org1(type,prov_code,amp_code,tam_code), type
                      from org_admin_point
                     order by type, prov_code, amp_code, tam_code
                 '''
        self.db.execute( sqlcmd )
        
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select distinct
                           case org_id2
                             when 1 then 3002
                             when 2 then 3009
                             when 3 then 3010
                             else 0
                            end,
                            org_id1,
                            org_id2
                       from temp_admincode
                 '''
        self.db.execute( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                 insert into  mid_place( key, type )
                      select  feat_key, feat_type 
                        from  mid_feat_key
                       where  3001 <= feat_type and feat_type <= 3010
                    order by  feat_type, feat_key
                 '''
        self.db.execute( sqlcmd )
    
    def _domake_geomtry(self):
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
        self.db.execute( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
             insert into temp_feat_name( key, type, nametype, langcode, name )
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
                  select key, type, 'ON', 'THA', namt from ad
                   union
                  select key, type, 'ON', 'ENG', name from ad
                 '''
        self.db.execute( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass