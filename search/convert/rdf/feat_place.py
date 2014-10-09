import convert.feature
import attribute_sql

class CPlace(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'place')
 
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
                 insert into  mid_place( key, type, pop, cap )
                      select  feat_key, feat_type, 0, 'N' 
                        from  mid_feat_key
                       where  3001 <= feat_type and feat_type <= 3010
                    order by  feat_type, feat_key
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        self._get_place_polygon()
        self._get_place_center()
        #get no point place, we will complete later.
        #get more point
        self._get_more_center()
        self._update_center()
        
    def _get_place_center(self):
        # we could miss lots of points for place!!!!
        # get country, state point 
        sqlcmd = '''
             insert into temp_place_geom( key, type, code, geotype, geom )
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
             insert into temp_place_geom( key, type, code, geotype, geom )
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
             insert into temp_place_geom( key, type, code, geotype, geom )
             select f.feat_key, f.feat_type, 7379, 'P', ST_GeometryFromText(l.location, 4326)
               from rdf_city_poi  as p
               join wkt_location  as l
                 on p.location_id = l.location_id and p.builtup_id = p.named_place_id
               join mid_feat_key  as f
                 on p.builtup_id = f.org_id1 and 9 = f.org_id2
                 ''' 
        self.db.do_big_insert( sqlcmd )
        
        
    def _get_more_center(self):
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
                select feat_key, feat_type, geom
                  from (
                        select f.feat_key, f.feat_type, pp.geom, row_number() over ( partition by f.feat_key ) as seq 
                          from (
                                 select 1 as t, a1 as a, geom from p
                                 union 
                                 select 2 as t, a2 as a, geom from p
                                 union 
                                 select 8 as t, a8 as a, geom from p
                                 union  
                                 select 9 as t, a9 as a, geom from p
                               ) as pp
                          join mid_feat_key  as f
                            on pp.a = f.org_id1 and pp.t = f.org_id2
                       ) as tt
                       where seq = 1
                 '''
        self.db.do_big_insert( sqlcmd )
        ## a1, a2, a8, a9
        sqlcmd = '''
               insert into temp_place_point( key, type, geom )
               select f.feat_key, f.feat_type, ST_GeometryFromText(l.location, 4326) as geom
                 from (
                     select p.order1_id as a_id, p.location_id,
                             row_number() over ( partition by p.order1_id 
                                                 order by case 
                                                             when population is null then 0
                                                             else population 
                                                          end desc, street_name
                                                ) as seq
                        from rdf_city_poi  as p
                    union
                      select p.order2_id as a_id, p.location_id,
                             row_number() over ( partition by p.order2_id 
                                                 order by case 
                                                             when population is null then 0
                                                             else population 
                                                          end desc, street_name
                                                ) as seq
                        from rdf_city_poi  as p
                      union 
                      select p.order8_id as a_id, p.location_id,
                             row_number() over ( partition by p.order8_id 
                                                 order by case 
                                                             when population is null then 0
                                                             else population 
                                                          end desc, street_name
                                                ) as seq
                        from rdf_city_poi  as p
                       union
                       select p.builtup_id as a_id, p.location_id,
                              row_number() over ( partition by p.builtup_id 
                                                  order by case 
                                                             when population is null then 0
                                                             else population 
                                                           end desc, street_name
                                                 ) as seq
                        from rdf_city_poi  as p
                          ) as t
                     join mid_feat_key  as f
                       on t.a_id = f.org_id1 and ( f.feat_type between 3001 and 3010 ) and t.seq = 1 
                     join wkt_location  as l
                       on t.location_id = l.location_id  
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
                         where admin_place_id  not  in
                              ( 
                               select id 
                                 from (
                                        select  country_id as id from rdf_city_poi
                                        union
                                        select  order1_id as id from rdf_city_poi
                                        union
                                        select  order2_id as id from rdf_city_poi
                                        union
                                        select  order8_id as id from rdf_city_poi
                                        union
                                        select  builtup_id as id from rdf_city_poi 
                                      ) as tt 
                                  where id is not null
                                )
                       ) as a
                    on c.named_place_id = a.admin_place_id
                  join rdf_carto_face as f
                    on c.carto_id = f.carto_id
                  join wkt_face       as w
                    on f.face_id = w.face_id
                  join mid_feat_key  as fk
                    on a.admin_place_id = fk.org_id1 and a.admin_order = fk.org_id2
                 group by fk.feat_key,  fk.feat_type
                 '''
        self.db.do_big_insert( sqlcmd )
        ##get point from link for a9
        sqlcmd = '''
                 insert into temp_place_point( key, type, geom )
                 select feat_key, feat_type, ST_ClosestPoint( geom, ST_Centroid(geom) )
                   from (
                         select fk.feat_key, fk.feat_type, ST_Collect( ST_GeometryFromText( w.link, 4326) ) as geom
                           from (
                                  select link_id, left_admin_place_id as place_id from rdf_link
                                  union
                                  select link_id, right_admin_place_id as place_id from rdf_link
                                ) as l
                           join wkt_link      as w
                             on l.link_id = w.link_id
                           join mid_feat_key  as fk
                             on l.place_id = fk.org_id1 and  ( fk.feat_type between 3001 and 3010 ) 
                          where fk.feat_key not in 
                                 (
                                   select key from temp_place_point where type between 3001 and 3010
                                   union
                                   select key from temp_place_geom where type between 3001 and 3010
                                 )
                           group by fk.feat_key,  fk.feat_type
                         ) as t
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _update_center(self):
        sqlcmd = '''
                 insert into temp_place_geom( key, type, code, geotype, geom )
                 select tp.key, tp.type, 7379, 'P', geom
                   from temp_place_point as tp
                   where not exists
                         (
                            select key 
                              from temp_place_geom
                              where key = tp.key and code = 7379
                         )
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _get_place_polygon(self):
        sqlcmd = '''
                insert into temp_place_geom( key, type, code, geotype, geom )
                select feat_key,  feat_type, 7000, 'F', st_union(geom)
                  from (
                    select fe.feat_key, fe.feat_type, ST_GeometryFromText(w.face, 4326) as geom
                      from rdf_admin_place  as p
                      join mid_feat_key     as fe 
                        on fe.org_id1 = p.admin_place_id and  3001 <= fe.feat_type and fe.feat_type <= 3010 
                      join rdf_carto as c
                        on p.admin_place_id = c.named_place_id and c.named_place_type = 'A'
                      join rdf_carto_face as f
                        on c.carto_id = f.carto_id
                      join wkt_face as w
                        on f.face_id = w.face_id
                       ) as t
                 group by feat_key,  feat_type
                 '''
        self.db.do_big_insert( sqlcmd )
            
    def _domake_name(self):
        sqlcmd = '''
                 insert into temp_place_name( key, type, nametype, langcode, name, tr_lang, tr_name, ph_lang, ph_name )
                 select p.key, p.type, 
                        case  
                          when ns.name_type = 'B' and ns.is_exonym = 'N' then 'ON'
                          else 'AN'
                        end,
                        n.language_code, n.name,
                        COALESCE(tr.transliteration_type, ''),   COALESCE( tr.name,''),
                        COALESCE(ph.phonetic_language_code, ''), COALESCE( ph.phonetic_string, '')
                   from mid_place               as p
                   join mid_feat_key            as f
                     on p.key = f.feat_key and p.type = f.feat_type
                   join rdf_feature_names       as ns
                     on f.org_id1  = ns.feature_id and ns.owner = 'A'
                ''' + attribute_sql.sql_all_name( 'ns', 'name_id', 'feature' )

        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        sqlcmd = '''
                 insert into mid_country_profile( iso, off_lang, key, type )
                 select distinct a0.iso_country_code, a0.language_code, f.feat_key, f.feat_type
                   from mid_feat_key    as f
                   join rdf_country     as a0
                     on a0.country_id = f.org_id1 and
                        0 = f.org_id2
                   --join rdf_country_profile  as c
                   --  on a0.iso_country_code = c.iso_country_code
                  order by a0.iso_country_code
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
                    on a.admin_place_id = fe.org_id1 and 3001 <= fe.feat_type and fe.feat_type <= 3010
             left join mid_feat_key        as f0
                    on a.country_id = f0.org_id1 and f0.feat_type = 3001
             left join mid_feat_key        as f1
                    on a.order1_id = f1.org_id1  and f1.feat_type = 3002
             left join mid_feat_key        as f2
                    on a.order2_id = f2.org_id1  and f2.feat_type = 3003
             left join mid_feat_key        as f8 
                    on a.order8_id = f8.org_id1  and f8.feat_type = 3009
             left join mid_feat_key        as f9
                    on a.builtup_id = f9.org_id1 and f9.feat_type = 3010
                 order by fe.feat_type, fe.feat_key
                '''
        self.db.do_big_insert( sqlcmd )
        
        