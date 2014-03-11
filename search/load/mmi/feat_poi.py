import load.feature

class CPoi(load.feature.CFeature):
    def __init__(self ):
        print "mmi's poi"
        load.feature.CFeature.__init__(self, 'poi')
 
    def _domake_key(self):
        sqlcmd = '''
                     insert into temp_poi_uid( uid,  org_id1, org_id2 )
                     select uid, row_number() over( ), 1000 
                       from org_poi_point
                      order by uid
                 '''
        self.db.do_big_insert( sqlcmd )
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 1000, org_id1, org_id2 
                      from temp_poi_uid
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_poi( key, type, cat_id, imp )
                    select f.feat_key, f.feat_type, c.id, p.priority
                      from org_poi_point as p
                      join temp_poi_uid  as t
                        on p.uid     = t.uid
                      join mid_feat_key  as f
                        on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                      join temp_poi_category as c
                        on p.cat_code = c.org_code
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select f.feat_key, f.feat_type, 7000, 'P', ST_SetSRID(st_makepoint(p.lon,p.lat), 4326)
                      from org_poi_point as p
                      join temp_poi_uid  as t
                        on p.uid     = t.uid
                      join mid_feat_key  as f
                        on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select f.feat_key, f.feat_type, 9920, 'P', ST_SetSRID(st_makepoint(p.lon_1,p.lat_1), 4326)
                      from org_poi_point as p
                      join temp_poi_uid  as t
                        on p.uid     = t.uid
                      join mid_feat_key  as f
                        on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )

    def _domake_name(self):
        sqlcmd = '''
               insert into temp_feat_name( key, type, nametype, langcode, name )
               with pn ( key, type, on_n, an_n, br_n )
               as ( select f.feat_key, f.feat_type, p.std_name, p.alt_name, p.brand_nme
                      from org_poi_point as p
                      join temp_poi_uid  as t
                        on p.uid     = t.uid
                      join mid_feat_key  as f
                        on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                    )
                select key, type, 'ON', 'ENG', on_n from pn where on_n is not null
                 union
                select key, type, 'AN', 'ENG', regexp_split_to_table(an_n, ';') from pn where an_n is not null
                union
                select key, type, 'BN', 'ENG', br_n from pn where br_n is not null
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        sqlcmd = '''
               insert into mid_poi_attr_value( key, type, attr_type, attr_value )
               with pa ( key, type,  phone, phone2, street, hno )
               as ( select f.feat_key, f.feat_type, p.phone, p.phone2, p.street, p.hno
                      from org_poi_point as p
                      join temp_poi_uid  as t
                        on p.uid     = t.uid
                      join mid_feat_key  as f
                        on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                    )
                select  key, type, 'TL', phone   from pa where phone is not null
                union
                select  key, type, 'TL', phone2  from pa where phone2 is not null
                union
                select  key, type, '6T', street  from pa where street is not null
                union
                select  key, type, '9H', hno     from pa where hno    is not null
                '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_relation(self):
        # poi to zipcode
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype ) 
                  select f.feat_key, f.feat_type, 7001, fz.feat_key, fz.feat_type
                    from org_poi_point as p
                    join temp_poi_uid  as t
                      on p.uid     = t.uid
                    join mid_feat_key  as f
                      on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                    join temp_postcode as z
                      on p.zipcode = z.org_code
                    join mid_feat_key  as fz
                      on z.id = fz.org_id1 and z.sub = fz.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
        # poi to place
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype ) 
                  select f.feat_key, f.feat_type, 7001, fa.feat_key, fa.feat_type
                    from org_poi_point as p
                    join temp_poi_uid  as t
                      on p.uid     = t.uid
                    join mid_feat_key  as f
                      on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                    join temp_admincode as ta
                      on p.adminid = ta.id
                    join mid_feat_key   as fa
                      on ta.org_id1 = fa.org_id1 and 
                         ta.org_id2 = fa.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
        # poi to link
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype ) 
                  select f.feat_key, f.feat_type, 7002, l.feat_key, l.feat_type
                    from org_poi_point as p
                    join temp_poi_uid  as t
                      on p.uid     = t.uid
                    join mid_feat_key  as f
                      on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                    join mid_feat_key  as l
                      on p.edge_id = l.org_id1 and l.org_id2 = 4110
                 '''
        self.db.do_big_insert( sqlcmd )
        
        
        