import convert.feature
import attribute_sql

class CPoi(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'poi')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select distinct 1000, poi_id, 1000  
                      from rdf_poi
                     order by poi_id
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_poi( key, type, cat_id, imp )
                    select f.feat_key, f.feat_type, 
                           COALESCE(sc2.id, sc.id, c.id), 
                           case national_importance 
                             when 'Y' then 1
                             else 0 
                           end
                      from rdf_poi              as p
                      join mid_feat_key         as f
                        on p.poi_id = f.org_id1 and
                           1000     = f.org_id2
                      join temp_org_category    as c
                        on p.cat_id = c.org_code
                 left join rdf_poi_subcategory  as s
                        on p.poi_id = s.poi_id and s.seq_num = 1
                 left join temp_org_category    as sc
                        on (p.cat_id*1000+s.subcategory) = sc.org_code
                left join rdf_poi_place_of_worship  as pw
                        on p.poi_id = pw.poi_id
                 left join temp_org_category    as sc2
                        on (p.cat_id*1000+pw.building_type) = sc2.org_code
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        # poi's point
        sqlcmd = '''
                    insert into temp_poi_geom( key, type, code, geotype, geom )
                    select f.feat_key, f.feat_type, 7000, 'P', 
                           ST_SetSRID(st_makepoint( l.lon/100000.0, l.lat/100000.0 ), 4326)
                      from rdf_poi_address as p
                      join mid_feat_key    as f
                        on p.poi_id = f.org_id1 and 1000 = f.org_id2
                      join rdf_location    as l
                        on p.location_id = l.location_id
                 '''
        self.db.do_big_insert( sqlcmd )
        # poi's entry point
        
        # poi's polygon
        sqlcmd = '''
                    insert into temp_poi_geom( key, type, code, geotype, geom )
                    select feat_key,  feat_type, 7010, 'F', 
                           ST_ConvexHull(st_collect(geom))
                      from (
                            select fe.feat_key, fe.feat_type, ST_GeometryFromText(w.face, 4326) as geom
                              from rdf_poi_feature  as p
                              join mid_feat_key     as fe
                                on p.poi_id = fe.org_id1 and 1000 = fe.org_id2
                              join rdf_cf          as c
                                on p.owner = 'V' and p.feature_id = c.cf_id
                              join rdf_cf_building as b
                                on c.cf_id = b.cf_id
                              join rdf_building_face  as f
                                on b.building_id = f.building_id
                              join wkt_face as w
                                on f.face_id = w.face_id
                           ) as t
                     group by feat_key, feat_type
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
                 insert into temp_poi_name( key, type, nametype, langcode, name, tr_lang, tr_name, ph_lang, ph_name )
                 select f.feat_key, f.feat_type, 
                        case  
                             when p.name_type = 'B' and p.is_exonym = 'N' then 'ON'
                             else 'AN'
                           end,
                        n.language_code,n.name,
                        COALESCE(tr.transliteration_type, ''),   COALESCE( tr.name,''),
                        COALESCE(ph.phonetic_language_code, ''), COALESCE( ph.phonetic_string, '') 
                   from rdf_poi_names as p
                   join mid_feat_key  as f
                     on p.poi_id = f.org_id1 and 1000 = f.org_id2
                 ''' + attribute_sql.sql_all_name( 'p','name_id', 'poi' )
        self.db.do_big_insert( sqlcmd )
        
    
    def _domake_attribute(self):
        sqlcmd = '''
                 insert into mid_poi_address( key, type, lang, name, tr_lang, tr_name, hno )
                 select f.feat_key, f.feat_type,
                        COALESCE( language_code, ''),
                        COALESCE( street_name, actual_street_name),
                        '','',
                        COALESCE(house_number, actual_house_number, '' )
                   from rdf_poi_address as p
                   join mid_feat_key    as f
                     on p.poi_id = f.org_id1 and 1000 = f.org_id2
                  where street_name is not null or actual_street_name is not null
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                    insert into mid_poi_attr_value( key, type, attr_type, attr_value )
                    select f.feat_key, f.feat_type, 
                           case p.contact_type
                             when '1' then 'TL'
                             when '5' then 'TL'
                             when '3' then '8L'
                             when '4' then '8M'
                             when '2' then 'TL'
                           end, contact
                      from rdf_poi_contact_information as p
                      join mid_feat_key                as f
                        on p.poi_id = f.org_id1 and 1000 = f.org_id2
                '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_relation(self):
        #poi to place
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype ) 
                  select f.feat_key, f.feat_type, 7001, 
                         COALESCE( a9.feat_key,  a8.feat_key ),
                         COALESCE( a9.feat_type, a8.feat_type )
                    from rdf_poi_address as p
                    join mid_feat_key    as f
                      on p.poi_id = f.org_id1 and 1000 = f.org_id2
                    join mid_feat_key    as a8
                      on p.order8_id = a8.org_id1 and a8.org_id2  = 8
               left join mid_feat_key    as a9
                      on p.builtup_id = a9.org_id1 and a9.org_id2 = 9
                 '''
        self.db.do_big_insert( sqlcmd )
        
        # poi to postcode
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype ) 
                  select f.feat_key, f.feat_type, 7004, fz.feat_key, fz.feat_type
                    from rdf_poi_address as p
                    join mid_feat_key    as f
                      on p.poi_id = f.org_id1 and 1000 = f.org_id2
                    join rdf_country     as c
                      on p.country_id = c.country_id
                    join temp_postcode as z
                      on COALESCE( p.postal_code, p.actual_postal_code) = z.org_code and 
                         c.iso_country_code = z.iso
                    join mid_feat_key  as fz
                      on z.id = fz.org_id1 and z.type = fz.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
        # poi to link
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype ) 
                  select f.feat_key, f.feat_type, 7002, fz.feat_key, fz.feat_type
                    from rdf_poi_address as p
                    join mid_feat_key    as f
                      on p.poi_id = f.org_id1 and 1000 = f.org_id2
                    join rdf_location    as l
                      on p.location_id = l.location_id
                    join mid_feat_key  as fz
                      on l.link_id = fz.org_id1 and 2000 = fz.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name_geom(self): 
        self._gen_nameid( 'poi' )
        self._gen_geomid( 'poi' )
        