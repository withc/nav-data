import load.feature

class CPlace(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'place')
 
    def _domake_key(self):
  
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 3001+admin_order, admin_place_id, admin_order
                      from rdf_admin_hierarchy
                     order by admin_order, admin_place_id
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
        # we could miss lots of points for place!!!!
        # get country, state point 
        sqlcmd = '''
             insert into temp_feat_geom( key, type, code, geotype, geom )
               with p ( a0, a1, a0_c, a1_c, geom )
               as (
                   select country_id, order1_id, 
                          capital_country, capital_order1, ST_GeometryFromText(l.location, 4326) as geom
                     from rdf_city_poi  as p
                     join wkt_location  as l
                       on p.location_id = l.location_id 
                     where p.capital_country = 'Y' or p.capital_order1 = 'Y'
                   )
                select f.feat_key, f.feat_type, 7379, 'P', geom
                  from p
                  join mid_feat_key  as f
                    on p.a0 = f.org_id1 and 0 = f.org_id2 and p.a0_c = 'Y'
                union
                select f.feat_key, f.feat_type, 7379, 'P', geom
                  from p
                  join mid_feat_key  as f
                    on p.a1 = f.org_id1 and 1 = f.org_id2 and p.a1_c = 'Y'
                 ''' 
        self.db.do_big_insert( sqlcmd )
        # get a8 point
        sqlcmd = '''
             insert into temp_feat_geom( key, type, code, geotype, geom )
             select f.feat_key, f.feat_type, 7379, 'P', ST_GeometryFromText(l.location, 4326)
               from rdf_city_poi  as p
               join wkt_location  as l
                 on p.location_id = l.location_id and p.order8_id = p.named_place_id
               join mid_feat_key  as f
                 on p.order8_id = f.org_id1 and 8 = f.org_id2
                 ''' 
        self.db.do_big_insert( sqlcmd )
        # get a9 point
        sqlcmd = '''
             insert into temp_feat_geom( key, type, code, geotype, geom )
             select f.feat_key, f.feat_type, 7379, 'P', ST_GeometryFromText(l.location, 4326)
               from rdf_city_poi  as p
               join wkt_location  as l
                 on p.location_id = l.location_id and p.builtup_id = p.named_place_id
               join mid_feat_key  as f
                 on p.builtup_id = f.org_id1 and 9 = f.org_id2
                 ''' 
        self.db.do_big_insert( sqlcmd )
        #get more point
        self._get_more_geomtry()
        
    def _get_more_geomtry(self):
        
        sqlcmd = '''
            insert into temp_feat_geom( key, type, code, geotype, geom )
             with p ( a0, a1, a2, a8, a9, geom )
               as (
                   select country_id, order1_id, order2_id, order8_id, builtup_id, ST_GeometryFromText(l.location, 4326) as geom
                     from rdf_city_poi  as p
                     join wkt_location  as l
                       on p.location_id = l.location_id 
                     where p.capital_country = 'Y' or p.capital_order1 = 'Y'
                   )
                select f.feat_key, f.feat_type, 7379, 'P', geom
                  from p
                  join mid_feat_key  as f
                    on p.a1 = f.org_id1 and 1 = f.org_id2
                union
                select f.feat_key, f.feat_type, 7379, 'P', geom
                  from p
                  join mid_feat_key  as f
                    on p.a9 = f.org_id1 and 9 = f.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
          
    def _domake_name(self):
        
        sqlcmd = '''
                 insert into temp_feat_name( key, type, nametype, langcode, name )
                 select p.key, p.type, 
                        case  
                          when ns.name_type = 'B' and ns.is_exonym = 'N' then 'ON'
                          else 'AN'
                        end,
                        m.language_code, m.name
                   from mid_place         as p
                   join mid_feat_key      as f
                     on p.key = f.feat_key and p.type = f.feat_type
                   join rdf_feature_names as ns
                     on f.org_id1  = ns.feature_id
                   join rdf_feature_name as m
                     on ns.name_id = m.name_id
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        sqlcmd = '''
                 insert into mid_country_profile( iso, off_lang, key, type )
                 select distinct a0.iso_country_code, a0.language_code, f.feat_key, f.feat_type
                   from mid_feat_key    as f
                   join rdf_country     as a0
                     on a0.country_id = f.org_id1 and  0 = f.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        sqlcmd = '''
                 insert into mid_full_area(min_lon, min_lat, max_lon, max_lat )
                 select st_xmin(geom)*100000, st_ymin(geom)*100000, 
                        st_xmax(geom)*100000, st_ymax(geom)*100000
                   from ( 
                          select ST_extent( ST_GeometryFromText(g.face, 4326)  ) as geom 
                            from rdf_carto      as c
                            join rdf_carto_face as f
                              on c.carto_id = f.carto_id and c.named_place_type = 'A'
                            join wkt_face       as g
                              on g.face_id = f.face_id 
                        ) as a
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_relation(self):
        sqlcmd = '''
                insert into mid_place_admin( key, type, a0, a1, a2, a7, a8, a9 )
                select fe.feat_key, fe.feat_type, 
                       f0.feat_key, 
                       COALESCE( f1.feat_key, 0 ),
                       COALESCE( f2.feat_key, 0 ),
                       0,
                       COALESCE( f8.feat_key, 0 ),
                       COALESCE( f9.feat_key, 0 )
                  from rdf_admin_hierarchy as a
             left join mid_feat_key        as fe
                    on a.admin_place_id = fe.org_id1
             left join mid_feat_key        as f0
                    on a.country_id = f0.org_id1
             left join mid_feat_key        as f1
                    on a.order1_id = f1.org_id1
             left join mid_feat_key        as f2
                    on a.order2_id = f2.org_id1
             left join mid_feat_key        as f8
                    on a.order8_id = f8.org_id1
             left join mid_feat_key        as f9
                    on a.builtup_id = f9.org_id1
                '''
        self.db.do_big_insert( sqlcmd )
        
        