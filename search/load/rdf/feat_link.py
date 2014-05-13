import load.feature
import attribute_sql

class CLink(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'link')
 
    def _domake_key(self):
        sqlcmd = '''
                 insert into mid_feat_key( feat_type, org_id1, org_id2 )
                 select 2000, link_id, 2000
                   from ( 
                         select distinct link_id
                           from rdf_road_link
                          order by link_id
                        ) as l
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_link( key, type )
                    select fe.feat_key, fe.feat_type
                      from ( 
                           select distinct link_id
                             from rdf_road_link
                            order by link_id
                           )              as l
                      join mid_feat_key   as fe
                        on l.link_id = fe.org_id1 and   fe.org_id2 = 2000
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
        
    def _domake_name_geom(self): 
        self._gen_nameid( 'street' )
        self._gen_geomid( 'street' )
        