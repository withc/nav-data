import load.feature

class CPostcode(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'postcode')
 
    def _domake_key(self):
        #get postcode from extern table
        if self.db.existTable('xpostal_code'):
            self.logger.info('  have xpostal_code')
            sqlcmd = '''
                    insert into temp_postcode( id, type, iso, org_code )
                    select row_number() over( order by iso_ctry, post_full ), 3136, iso_ctry, post_full
                      from xpostal_code
                     '''
            self.db.do_big_insert( sqlcmd )
            
        #get postcode from core table
        sqlcmd = '''
                    insert into temp_postcode( id, type, iso, org_code )
                    select COALESCE( (select max(id) from temp_postcode), 0 ) + row_number() over( order by iso, p.zipcode ), 3136, 
                           iso, zipcode
                      from (
                            select iso_country_code as iso, postal_code as zipcode
                              from rdf_poi_address where postal_code is not null
                            union
                            select iso_country_code as iso, actual_postal_code as zipcode
                              from rdf_poi_address where actual_postal_code is not null
                            union
                            select iso_country_code as iso, postal_code as zipcode
                              from rdf_postal_area  as p
                              join rdf_country      as c
                                on p.country_id = c.country_id
                            union
                            select iso_country_code as iso, full_postal_code as zipcode
                              from rdf_postal_code_midpoint as p
                           ) as p
                    where p.zipcode is not null  and
                          not exists
                          (
                            select 1
                              from temp_postcode as t
                             where t.iso      = p.iso     and
                                   t.org_code = p.zipcode
                          ) 
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                 insert into mid_feat_key( feat_type, org_id1, org_id2 )
                 select 3200, id, type
                   from temp_postcode
                  order by iso, org_code
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        self._domake_common_postcode()
    
    def _domake_geomtry(self):
        if self.db.existTable('xpostal_code'):
            sqlcmd = '''
                    insert into temp_street_geom( key, type, code, geotype, geom )
                    select pc.key , pc.type, 7379, 'P', 
                           ST_SetSRID(st_makepoint( x.lon, x.lat ), 4326)  
                      from xpostal_code  as x
                      join mid_postcode  as pc
                        on x.post_full = pc.pocode and x.iso_ctry = pc.iso 
                     '''
            self.db.do_big_insert( sqlcmd )
            
        sqlcmd = '''
                 insert into temp_street_geom( key, type, code, geotype, geom )
                 select pc.key, pc.type, 7379, 'P', 
                        ST_SetSRID(st_makepoint( p.lon/100000.0, p.lat/100000.0 ), 4326)
                   from rdf_postal_code_midpoint as p
                   join mid_postcode             as pc
                     on p.full_postal_code = pc.pocode and p.iso_country_code = pc.iso
                  where not exists
                         ( select 1 
                             from temp_street_geom
                             where key  = pc.key  and
                                   type = pc.type and
                                   code = 7379
                         )
                 '''
        self.db.do_big_insert( sqlcmd )
        #get more point from poi
        sqlcmd = '''
                 insert into temp_street_geom( key, type, code, geotype, geom )
                 select pc.key , pc.type, 7379, 'P', 
                        ST_SetSRID(st_makepoint( p.lon/100000.0, p.lat/100000.0 ), 4326)
                   from (
                          select * 
                            from (
                                select * , row_number() over ( partition by iso, zipcode order by cnt desc ) as seq
                                from (
                                select distinct iso_country_code as iso, actual_postal_code as zipcode, l.lon, l.lat, 
                                       count(*) over ( partition by iso_country_code, actual_postal_code, l.lon, l.lat ) as cnt
                                  from rdf_poi_address as p
                                  join rdf_location    as l
                                    on p.location_id = l.location_id
                                 where iso_country_code = 'SGP' and actual_postal_code is not null
                                    ) as t
                                 ) as tt
                           where seq = 1
                         ) as p
                    join mid_postcode      as pc
                      on p.zipcode = pc.pocode and p.iso = pc.iso
                   where not exists
                         ( select 1 
                             from temp_street_geom
                             where key  = pc.key  and
                                   type = pc.type and
                                   code = 7379
                         )
                  order by pc.key
                 '''
        self.db.do_big_insert( sqlcmd )

    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select distinct pc.key , pc.type, 7001, fe.feat_key, fe.feat_type
                    from (
                           select admin_place_id, postal_area_id
                             from rdf_place_postal
                           union
                            select left_admin_place_id as admin_place_id, left_postal_area_id as postal_area_id
                              from rdf_link 
                              where left_admin_place_id is not null and  left_postal_area_id is not null
                            union
                            select right_admin_place_id as admin_place_id, right_postal_area_id as postal_area_id
                              from rdf_link 
                              where right_admin_place_id is not null and  right_postal_area_id is not null
                         ) as pp
                    join rdf_postal_area   as p
                      on pp.postal_area_id = p.postal_area_id
                    join rdf_country       as c
                      on p.country_id = c.country_id
                    join mid_postcode      as pc
                      on p.postal_code = pc.pocode and c.iso_country_code = pc.iso
                    join mid_feat_key      as fe
                      on pp.admin_place_id = fe.org_id1 and 
                         ( fe.feat_type between 3001 and 3010 )
                   order by pc.key, fe.feat_key
                  '''
        self.db.do_big_insert( sqlcmd )
        
        