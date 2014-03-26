import load.feature

class CPoi(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'poi')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select distinct 1000, poi_id, 1000  
                      from rdf_poi
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_poi( key, type, gen_code, imp )
                    select f.feat_key, f.feat_type, c.per_code, 
                           case national_importance 
                             when 'Y' then 1
                             else 0 
                           end
                      from rdf_poi       as p
                      join mid_feat_key  as f
                        on p.poi_id = f.org_id1 and 1000 = f.org_id2
                      join temp_org_category as c
                        on p.cat_id = c.org_code
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        # poi's point
#         sqlcmd = '''
#                     insert into temp_feat_geom( key, type, code, geotype, geom )
#                     select f.feat_key, f.feat_type, 7000, 'P', ST_SetSRID(st_makepoint(p.lon,p.lat), 4326)
#                       from rdf_poi as p
#                       join mid_feat_key    as f
#                         on p.poi_id = f.org_id1 and 1000 = f.org_id2
#                  '''
#         self.db.do_big_insert( sqlcmd )
        # poi's entry point
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select f.feat_key, f.feat_type, 7000, 'P', ST_GeometryFromText(l.location, 4326) 
                      from rdf_poi_address as p
                      join mid_feat_key    as f
                        on p.poi_id = f.org_id1 and 1000 = f.org_id2
                      join wkt_location    as l
                        on p.location_id = l.location_id
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
                 insert into temp_feat_name( key, type, nametype, langcode, name )
                 select f.feat_key, f.feat_type, 
                        case  
                             when p.name_type = 'B' and p.is_exonym = 'N' then 'ON'
                             else 'AN'
                           end,
                        n.language_code,n.name
                   from rdf_poi_names as p
                   join mid_feat_key  as f
                     on p.poi_id = f.org_id1 and 1000 = f.org_id2
                   join rdf_poi_name  as n
                     on p.name_id = n.name_id
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        sqlcmd = '''
              insert into mid_poi_attr_value( key, type, attr_type, attr_value )
                with pa ( key, type, number, street )
                as (
                    select f.feat_key, f.feat_type, 
                           COALESCE(house_number, actual_house_number ),
                           COALESCE(street_name, actual_street_name)
                      from rdf_poi_address as p
                      join mid_feat_key    as f
                        on p.poi_id = f.org_id1 and 1000 = f.org_id2
                    )
               select  key, type, '6T', street  from pa where street is not null
                union
               select  key, type, '9H', number  from pa where number is not null
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
                         COALESCE( a9.feat_type, a8.feat_key )
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
                    join temp_postcode as z
                      on p.postal_code = z.org_code
                    join mid_feat_key  as fz
                      on z.id = fz.org_id1 and z.sub = fz.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
        # poi to link
        
        
        