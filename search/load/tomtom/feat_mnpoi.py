import load.feature

class CMNPoi(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self,'mnpoi')
        
    def _domake_key(self):
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 1000, id, feattyp 
                      from org_mnpoi_pi as pi
                     where feattyp <> 9920
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_poi( key, type, gen_code, imp )
                    select fe.feat_key, fe.feat_type, 0, pi.import
                      from org_mnpoi_pi  as pi
                      join mid_feat_key  as fe
                        on pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7000,'P', pi.the_geom
                      from org_mnpoi_pi as pi
                      join mid_feat_key as fe
                        on pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                  insert into temp_feat_geom( key, type, code, geotype, geom )
                  select fe.feat_key, fe.feat_type, 9920,'P', p1.the_geom
                    from org_mnpoi_pi   as pi
                    join mid_feat_key   as fe
                      on pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    join org_mnpoi_pipr as pr
                      on pi.id = pr.poiid
                    join org_mnpoi_pi   as p1
                      on pr.belpoityp = 9920 and pr.belpoiid = p1.id 
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
                  insert into temp_feat_name( key, type, nametype, langcode, name )
                  select fe.feat_key, fe.feat_type, p.nametyp, p.namelc, p.name
                    from org_mnpoi_pinm as p
                    join mid_feat_key   as fe
                      on p.nametyp in ('ON', 'AN', 'BN', '1Q', '8Y') and
                         p.id      = fe.org_id1                      and
                         p.feattyp = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        sqlcmd = '''
                  insert into mid_poi_attr_value( key, type, attr_type, attr_value )
                     select fe.feat_key, fe.feat_type, 'TL', pi.telnum
                     from org_mnpoi_pi as pi
                     join mid_feat_key as fe
                       on pi.telnum is not null and pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    union
                     select fe.feat_key, fe.feat_type, 'TX', pi.faxnum
                     from org_mnpoi_pi as pi
                     join mid_feat_key as fe
                       on pi.faxnum is not null and pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    union
                     select fe.feat_key, fe.feat_type, '8M', pi.email
                     from org_mnpoi_pi as pi
                     join mid_feat_key as fe
                       on pi.email is not null and pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    union
                     select fe.feat_key, fe.feat_type, '8L', pi.http
                     from org_mnpoi_pi as pi
                     join mid_feat_key as fe
                       on pi.http is not null and pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    union
                     select fe.feat_key, fe.feat_type, '6T', pi.stname
                     from org_mnpoi_piad as pi
                     join mid_feat_key   as fe
                       on pi.stname is not null and pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    union
                     select fe.feat_key, fe.feat_type, '9H', pi.hsnum
                     from org_mnpoi_piad as pi
                     join mid_feat_key   as fe
                       on pi.hsnum is not null and pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_relation(self):
        
        # poi to a8,a9
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select fe.feat_key, fe.feat_type, 7001, f1.feat_key, f1.feat_type
                    from org_mnpoi_pisa as sa
                    join mid_feat_key   as fe
                      on sa.aretyp in (1119,1120) and sa.id = fe.org_id1 and sa.poityp = fe.org_id2
                    join mid_feat_key as f1
                      on sa.areid = f1.org_id1 and sa.aretyp = f1.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
        # poi to link
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select fe.feat_key, fe.feat_type, 7002, f1.feat_key, f1.feat_type
                    from org_mnpoi_pi  as pi
                    join mid_feat_key  as fe
                      on pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    join mid_feat_key  as f1
                      on pi.cltrpelid = f1.org_id1 and f1.org_id2 in (4110,4130)
                 '''
        self.db.do_big_insert( sqlcmd )
        