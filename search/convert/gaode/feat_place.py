import convert.feature

class CPlace(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'place')
 
    def _domake_key(self):
  
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select distinct
                           case ad_level 
                              when 0 then 3001
                              when 2 then 3002
                              when 3 then 3009
                              when 4 then 3010
                              else 0
                           end, ad_code::int, ad_level*10
                      from org_adminarea where ad_level < 5
                      order by ad_level*10, ad_code
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

        sqlcmd = '''
                 insert into temp_place_geom( key, type, code, geotype, geom ) 
                 select f.feat_key, f.feat_type, 7379, 'P', ST_SetSRID(st_makepoint( lon, lat), 4326)
                   from ( 
                          select distinct ad_code::int as code, ad_level, 
                                 mid_gaode_coord(x_coord) as lon, mid_gaode_coord(y_coord) as lat
                            from org_adminarea
                           where x_coord <> 0 and y_coord <> 0
                        )  as ad
                   join mid_feat_key   as f
                     on ad.code     = f.org_id1 and 
                        ad.ad_level = f.org_id2/10 and
                        f.org_id2%10 = 0
                 ''' 
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        
        sqlcmd = '''
                 insert into temp_place_name( key, type, nametype, langcode, name, tr_lang, tr_name )
                 select f.feat_key, f.feat_type, 'ON',  'CHI', name_chn, 'PYN', name_py
                   from ( 
                          select distinct ad_code::int as code, ad_level, name_chn, name_py, name_eng 
                            from org_adminarea
                           where name_chn is not null
                        )  as ad
                   join mid_feat_key   as f
                     on ad.code     = f.org_id1 and 
                        ad.ad_level = f.org_id2/10 and
                        f.org_id2%10 = 0
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        sqlcmd = '''
                 insert into mid_country_profile( iso, off_lang, key, type )
                 select 'CHN', 'CHI', f.feat_key, f.feat_type
                   from mid_feat_key as f
                  where feat_type = 3001
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                 insert into mid_full_area( min_lon, min_lat, max_lon, max_lat )
                 select mid_gaode_coord(st_xmin(geom)), mid_gaode_coord(st_ymin(geom)), 
                        mid_gaode_coord(st_xmax(geom)), mid_gaode_coord(st_ymax(geom))
                   from (
                          select ST_extent(the_geom) as geom 
                            from org_adminarea
                           where ad_level = 0
                        ) as a
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_relation(self):
        sqlcmd = '''
                insert into mid_place_admin( key, type, a0, a1, a2, a7, a8, a9 )
                select feat_key, feat_type, feat_key, 0, 0, 0, 0, 0
                  from mid_feat_key
                 where feat_type = 3001
               union
                select a1.feat_key, a1.feat_type, a0.feat_key, a1.feat_key, 0, 0, 0, 0
                  from mid_feat_key  as a1
                  join mid_feat_key  as a0
                    on a1.feat_type = 3002 and
                       a0.feat_type = 3001 
                union
                select a8.feat_key, a8.feat_type, a0.feat_key, a1.feat_key, 0, 0, a8.feat_key, 0
                  from mid_feat_key  as a8
                  join mid_feat_key  as a1
                    on a8.feat_type = 3009 and
                       a1.feat_type = 3002 and
                       a8.org_id1/10000  = a1.org_id1/10000
                  join mid_feat_key  as a0
                    on a0.feat_type = 3001  
                union
                select a9.feat_key, a9.feat_type, a0.feat_key, a1.feat_key, 0, 0, a8.feat_key, a9.feat_key
                  from mid_feat_key  as a9
                  join mid_feat_key  as a8
                    on a9.feat_type = 3010 and
                       a8.feat_type = 3009 and
                       a9.org_id1/100  = a8.org_id1/100
                  join mid_feat_key  as a1
                    on a8.feat_type = 3009 and
                       a1.feat_type = 3002 and
                       a8.org_id1/10000  = a1.org_id1/10000
                  join mid_feat_key  as a0
                    on a0.feat_type = 3001
                '''
        self.db.do_big_insert( sqlcmd )
        
        