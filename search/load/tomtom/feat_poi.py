import load.feature

class CPoi(load.feature.CFeature):
    def __init__(self ):
        print "tomtom's poi feature"
        load.feature.CFeature.__init__(self)
        self.name = 'tomtom poi'
        
    def make_key(self):
        print ''
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 1000, id, feattyp 
                    from org_pi as pi
                    where feattyp <> 9920
                 '''
        self.db.execute( sqlcmd )
        
    def make_feature(self):
        print ''
        sqlcmd = '''
                    insert into mid_poi( key, cat_id, imp )
                    select fe.feat_key, 0, pi.import
                    from org_pi as pi
                    join mid_feat_key as fe
                      on pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                 '''
        self.db.execute( sqlcmd )
    
    def make_geomtry(self):
        print ''
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7000,'P', pi.the_geom
                    from org_pi as pi
                    join mid_feat_key as fe
                      on pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                 '''
        self.db.execute( sqlcmd )
        
    def make_name(self):
        print ''
        sqlcmd = '''
                    insert into temp_feat_name( key, type, nametype, langcode, name )
                    select fe.feat_key, fe.feat_type, p.nametyp, p.namelc, p.name
                    from org_pinm as p
                    join mid_feat_key as fe
                      on  p.nametyp in ('ON', 'AN', 'BN', '1Q', '8Y')
                         and p.id = fe.org_id1 
                         and p.feattyp = fe.org_id2
                 '''
        self.db.execute( sqlcmd )
    
    def make_attribute(self):
        print ''
        
    def make_relation(self):
        print ''