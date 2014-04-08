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
             insert into temp_street_geom( key, type, code, geotype, geom )
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
             insert into temp_street_geom( key, type, code, geotype, geom )
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
             insert into temp_street_geom( key, type, code, geotype, geom )
             select f.feat_key, f.feat_type, 7379, 'P', ST_GeometryFromText(l.location, 4326)
               from rdf_city_poi  as p
               join wkt_location  as l
                 on p.location_id = l.location_id and p.builtup_id = p.named_place_id
               join mid_feat_key  as f
                 on p.builtup_id = f.org_id1 and 9 = f.org_id2
                 ''' 
        self.db.do_big_insert( sqlcmd )
        #get no point place, we will complete later.
        #get more point
        self._get_more_geomtry()
        self._update_geomtry()
        
    def _get_more_geomtry(self):
        ##
        sqlcmd = '''
             insert into temp_place_point( key, type, geom )
               with p ( a0, a1, a2, a8, a9, geom )
               as (
                   select country_id, order1_id, order2_id, order8_id, builtup_id, ST_GeometryFromText(l.location, 4326) as geom
                     from rdf_city_poi  as p
                     join wkt_location  as l
                       on p.location_id = l.location_id 
                     where p.capital_country = 'Y' or p.capital_order1 = 'Y'
                   )
                select distinct f.feat_key, f.feat_type, pp.geom
                  from (
                         select 2 as t, a2 as a, geom from p
                         union 
                         select 8 as t, a8 as a, geom from p
                         union  
                         select 9 as t, a9 as a, geom from p
                       ) as pp
                  join mid_feat_key  as f
                    on pp.a = f.org_id1 and pp.t = f.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        ## a8, a9
        sqlcmd = '''
               insert into temp_place_point( key, type, geom )
               select f.feat_key,  f.feat_type, geom
                 from (  
                      select p.order8_id as a_id, ST_GeometryFromText(l.location, 4326) as geom, row_number() over ( partition by p.order8_id ) as seq
                        from rdf_city_poi  as p
                        join wkt_location  as l
                          on p.location_id = l.location_id 
                       union
                       select p.builtup_id as a_id, ST_GeometryFromText(l.location, 4326) as geom, row_number() over ( partition by p.builtup_id ) as seq
                        from rdf_city_poi  as p
                        join wkt_location  as l
                          on p.location_id = l.location_id 
                          ) as t
                     join mid_feat_key  as f
                       on t.a_id = f.org_id1 and t.seq = 1 
                     where f.feat_key not in ( select key from temp_place_point )
                 '''
        self.db.do_big_insert( sqlcmd )
        
        ## get point from face
        sqlcmd = '''
                insert into temp_place_point( key, type, geom )
                select fk.feat_key,  fk.feat_type, ST_Centroid( st_union( ST_GeometryFromText(w.face, 4326) ))
                  from rdf_carto as c
                  join ( 
                         select *  
                         from rdf_admin_hierarchy
                         where admin_place_id not in ( select distinct order8_id from rdf_city_poi )
                       ) as a
                    on c.named_place_id = a.admin_place_id and a.admin_order = 8
                  join rdf_carto_face as f
                    on c.carto_id = f.carto_id
                  join wkt_face       as w
                    on f.face_id = w.face_id
                  join mid_feat_key  as fk
                    on a.admin_place_id = fk.org_id1 and a.admin_order = fk.org_id2
                 group by fk.feat_key,  fk.feat_type
                 '''
        self.db.do_big_insert( sqlcmd )
        ##
        
    def _update_geomtry(self):
        sqlcmd = '''
                 insert into temp_street_geom( key, type, code, geotype, geom )
                 select tp.key, tp.type, 7379, 'P', geom
                   from temp_place_point as tp
                   where not exists
                         (
                            select key 
                              from temp_street_geom
                              where key = tp.key and code = 7379
                         )
                 '''
        self.db.do_big_insert( sqlcmd )
           
    def _domake_name(self):
        sqlcmd = '''
                 insert into temp_street_name( key, type, nametype, langcode, name )
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
        
        