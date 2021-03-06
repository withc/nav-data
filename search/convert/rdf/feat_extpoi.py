import convert.feature

class CExtPoi(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'ext-poi')
 
    def _domake_key(self):
        sqlcmd = '''
                 insert into temp_ext_poi ( poi_source, poi_key, cat_id, lang, name, iso,
                                            pl2, pl3, pl4, pl5, postcode,
                                            st, hno, tel, lon, lat )
                 select %s, poi_key, category_id_text::int, poi_name_lan_code, text_text, countrycode_text,
                        plclvl2_text, plclvl3_text, plclvl4_text, plclvl5_text, nt_postal_text,
                        case sttype_before
                           when 'true'  then sttype_text||' '||stname_text
                           when 'false' then stname_text||' '||sttype_text
                           else stname_text
                        end,
                        hnr_text,
                        num_text, lon_text::double precision*100000,  lat_text::double precision*100000
                   from %s
                 ''' 
        self.db.do_big_insert( sqlcmd % ( '101', 'xcorepoipoi') )
        self.db.do_big_insert( sqlcmd % ( '102', 'xextlistpoi') )

        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select distinct 1000, poi_key, poi_source  
                      from temp_ext_poi
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_poi( key, type, gen_code, imp )
                    select f.feat_key, f.feat_type, 
                           case
                             when c.per_code = 440532992 then srch_place_worship(p.name)+c.per_code
                             else c.per_code
                           end, 0
                      from temp_ext_poi          as p
                      join mid_feat_key          as f
                        on p.poi_source = f.org_id2 and
                           p.poi_key    = f.org_id1
                      join temp_org_category    as c
                        on p.cat_id = c.org_code
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        # poi's point
        sqlcmd = '''
                    insert into temp_poi_geom( key, type, code, geotype, geom )
                    select f.feat_key, f.feat_type, 7000, 'P', 
                           ST_SetSRID(st_makepoint( p.lon/100000.0, p.lat/100000.0 ), 4326)
                      from temp_ext_poi          as p
                      join mid_feat_key          as f
                        on p.poi_source = f.org_id2 and
                           p.poi_key    = f.org_id1
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
              insert into temp_poi_name( key, type, nametype, langcode, name, tr_lang, tr_name )
              select f.feat_key, f.feat_type, 'ON', p.lang, p.name, '', ''
                from temp_ext_poi          as p
                join mid_feat_key          as f
                  on p.poi_source = f.org_id2 and
                     p.poi_key    = f.org_id1
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        sqlcmd = '''
                 insert into mid_poi_address( key, type, lang, name, tr_lang, tr_name, hno )
                 select f.feat_key, f.feat_type, p.lang, p.st, '','', COALESCE(p.hno, '' )
                   from temp_ext_poi          as p
                   join mid_feat_key          as f
                     on p.poi_source = f.org_id2 and
                        p.poi_key    = f.org_id1
                  where p.st is not null
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                    insert into mid_poi_attr_value( key, type, attr_type, attr_value )
                    select f.feat_key, f.feat_type, 'TL', p.tel
                      from temp_ext_poi          as p
                      join mid_feat_key          as f
                        on p.poi_source = f.org_id2 and
                           p.poi_key    = f.org_id1
                     where p.tel is not null
                '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_relation(self):
        #the next sql is so slow in some database, we have analyze table when call do_big_insert, 
        #but it is fail to analyze table in some database.
        #anyway, analyze table mid_street_name again here.
        #self.db.analyze('mid_place_name')
        #poi to place
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype ) 
                  with 
                  pl as (
                  select k.key, k.type, n0.iso, n1.nameid as n1, n2.nameid as n2, n3.nameid as n3, COALESCE( n4.nameid, 0 ) as n4
                    from (
                         select key, type, 
                                srch_get_admin( ary, 1 ) as k0,
                                srch_get_admin( ary, 2 ) as k1,
                                srch_get_admin( ary, 3 ) as k2,
                                srch_get_admin( ary, 4 ) as k3,
                                srch_get_admin( ary, 5 ) as k4
                           from (
                                 select key, type, array[ a0, a1, a2, a7, a8, a9] as ary
                                   from mid_place_admin
                                   where a8 > 0 or a9 > 0
                                ) as t
                            ) as k
                         join mid_country_profile as n0
                           on k.k0 = n0.key
                         join mid_place_to_name as n1
                           on k.k1 = n1.key and n1.nametype = 'ON'
                         join mid_place_to_name as n2
                           on k.k2 = n2.key and  n2.nametype = 'ON'
                         join mid_place_to_name as n3
                           on k.k3 = n3.key and  n3.nametype = 'ON'
                    left join mid_place_to_name as n4
                           on k.k4 = n4.key and  n4.nametype = 'ON'
                     ),
                 p as (
                  select f.feat_key, f.feat_type, p.iso, n1.id as id1, n2.id as id2, n3.id as id3, COALESCE( n4.id, 0 ) as id4 
                    from temp_ext_poi          as p
                    join mid_feat_key          as f
                      on p.poi_source = f.org_id2 and
                         p.poi_key    = f.org_id1
                    join mid_place_name  as n1
                      on p.pl2 = n1.name and p.lang = n1.langcode
                    join mid_place_name  as n2
                      on p.pl3 = n2.name and p.lang = n2.langcode
                    join mid_place_name  as n3
                      on p.pl4 = n3.name and p.lang = n3.langcode
                   left join mid_place_name  as n4
                      on p.pl5 = n4.name and p.lang = n4.langcode
                     )
                  select p.feat_key, p.feat_type, 7001, pl.key, pl.type
                    from p
                    join pl
                      on p.iso = pl.iso and
                         p.id1 = pl.n1  and 
                         p.id2 = pl.n2  and 
                         p.id3 = pl.n3  and 
                         p.id4 = pl.n4
                 '''
        self.db.do_big_insert( sqlcmd )
        
        # poi to postcode
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype ) 
                  select f.feat_key, f.feat_type, 7004, fz.feat_key, fz.feat_type
                    from temp_ext_poi          as p
                    join mid_feat_key          as f
                      on p.poi_source = f.org_id2 and
                         p.poi_key    = f.org_id1
                    join temp_postcode as z
                      on p.postcode = z.org_code and p.iso = z.iso
                    join mid_feat_key  as fz
                      on z.id = fz.org_id1 and z.type = fz.org_id2 
                 '''
        self.db.do_big_insert( sqlcmd )
        
        # poi to link
        
    
    
    