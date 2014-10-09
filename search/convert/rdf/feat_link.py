import convert.feature
import attribute_sql

class CLink(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'link')
 
    def _domake_key(self):
        sqlcmd = '''
                 insert into mid_feat_key( feat_type, org_id1, org_id2 )
                 select 2000, link_id, 2000
                   from rdf_nav_link 
                  order by link_id
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_link( key, type, frc, fow, fnode, tnode )
                    select fe.feat_key, fe.feat_type, functional_class, -1, ff.feat_key , ft.feat_key
                      from rdf_nav_link   as nl
                      join rdf_link       as l
                        on nl.link_id = l.link_id
                      join mid_feat_key   as fe
                        on nl.link_id = fe.org_id1      and
                           fe.org_id2 = 2000
                      join mid_feat_key   as ff
                        on l.ref_node_id = ff.org_id1   and
                           ff.org_id2    = 1002
                      join mid_feat_key   as ft
                        on l.nonref_node_id = ft.org_id1 and
                           ft.org_id2       = 1002
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert into temp_street_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7000,'L', ST_GeometryFromText(l.link, 4326) as geom
                      from wkt_link      as l
                      join mid_feat_key  as fe
                        on l.link_id = fe.org_id1 and 2000 = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
                    insert into temp_street_name( key, type, nametype, langcode, name, tr_lang, tr_name, ph_lang, ph_name )
                    select f.feat_key, f.feat_type, 
                           case 
                             when n.route_type is not null then 'RN'
                             when n.name_type = 'B' and n.is_exonym = 'N' then 'ON'
                             else 'AN'
                           end,
                           n.language_code,n.street_name,
                           COALESCE(tr.transliteration_type, ''),   COALESCE( tr.name,''),
                           COALESCE(ph.phonetic_language_code, ''), COALESCE( ph.phonetic_string, '') 
                    from rdf_road_link  as r
                    join mid_feat_key   as f
                      on r.link_id = f.org_id1 and f.org_id2 = 2000
                 ''' + attribute_sql.sql_all_name( 'r','road_name_id', 'road' )
                 
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        #link to place
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select f.feat_key, f.feat_type, 7001, fp.feat_key, fp.feat_type
                    from ( 
                           select link_id, left_admin_place_id as place_id
                             from rdf_link
                         union all
                           select link_id, right_admin_place_id as place_id
                             from rdf_link  
                            where left_admin_place_id <> right_admin_place_id     
                         ) as l
                    join mid_feat_key  as f
                      on l.link_id = f.org_id1 and f.org_id2 = 2000
                    join mid_feat_key  as fp
                      on l.place_id = fp.org_id1    and 
                         ( fp.feat_type between 3001 and 3010)
                 '''
        self.db.do_big_insert( sqlcmd )
        #link to postcode
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select f.feat_key, f.feat_type, 7004, fz.feat_key, fz.feat_type
                    from ( 
                           select link_id, left_postal_area_id as postal_id
                             from rdf_link
                             where left_postal_area_id is not null
                         union 
                           select link_id, right_postal_area_id as postal_id
                             from rdf_link  
                            where right_postal_area_id is not null 
                         ) as l
                    join mid_feat_key    as f
                      on l.link_id = f.org_id1 and f.org_id2 = 2000
                    join rdf_postal_area as po
                      on l.postal_id = po.postal_area_id
                    join rdf_country     as c
                      on po.country_id = c.country_id
                    join temp_postcode   as z
                      on po.postal_code = z.org_code and c.iso_country_code = z.iso
                    join mid_feat_key    as fz
                      on z.id = fz.org_id1 and z.type = fz.org_id2  
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name_geom(self): 
        self._gen_nameid( 'street' )
        self._gen_geomid( 'street' )
        