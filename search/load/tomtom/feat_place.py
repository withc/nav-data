import load.feature

class CPlace(load.feature.CFeature):
    def __init__(self ):
        print "tomtom's place feature"
        load.feature.CFeature.__init__(self)
        self.name = 'tomtom place'
        
    def make_key(self):
        print ''
        # delete the place which has no-name or is a dummy area
        # in usa/can, one state set to one a0 place,
        # but, we always insist that a0 is country. must do something...
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select distinct 3001, id, feattyp  from org_a0 where name is not null
                    union
                    select distinct 3002, id, feattyp  from org_a1 where name is not null
                    union
                    select distinct 3003, id, feattyp  from org_a2 where name is not null
                    union
                    select distinct 3008, id, feattyp  from org_a7 where name is not null
                    union
                    select distinct 3009, id, feattyp  from org_a8 where name is not null
                    union
                    select distinct 3010, id, feattyp  from org_a9 where name is not null
                 '''
        self.db.execute( sqlcmd )
        
    def make_feature(self):
        print ''
        sqlcmd = '''
                 insert into mid_place( key, type )
                     select feat_key, feat_type 
                     from mid_feat_key
                     where  3001 <= feat_type and feat_type <= 3010
                     order by feat_type, feat_key
                 '''
        self.db.execute( sqlcmd )
        
        
    def make_geomtry(self):
        print ''
        tbs = ['org_a0','org_a1','org_a2','org_a8','org_a9']
        for tb in tbs:
            self._geomtry(tb)
        
    def make_name(self):
        print ''
        sqlcmd = '''
                    insert into temp_feat_name( key, type, nametype, langcode, name )
                    select fe.feat_key, fe.feat_type, an.nametyp, an.namelc, an.name
                    from org_an as an
                    join mid_feat_key as fe
                      on an.id = fe.org_id1 
                 '''
        self.db.execute( sqlcmd )
        
    def make_attribute(self):
        print ''
        
    def make_relation(self):
        print ''
        sqlcmd = '''
                 insert into mid_place_admin( key, type, a0, a1, a2, a7, a8, a9 )
                   select mf.feat_key, mf.feat_type, mf.feat_key, 0, 0, 0, 0, 0 
                   from org_a0 as a0
                   join mid_feat_key mf
                     on a0.id = mf.org_id1
                 '''
        self.db.execute( sqlcmd )
        sqlcmd = '''
                 insert into mid_place_admin( key, type, a0, a1, a2, a7, a8, a9 )
                   select mf.feat_key, mf.feat_type, mf0.feat_key, mf.feat_key, 0, 0, 0, 0
                   from org_a1 as a1
                   join mid_feat_key mf
                     on a1.id = mf.org_id1
                   join org_a0 as a0
                     on a1.order00 = a0.order00
                   join mid_feat_key mf0
                     on a0.id = mf0.org_id1
                 '''
        self.db.execute( sqlcmd )
        
    def _geomtry(self, tb):
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7000,'A', a.geom
                    from (
                        select id, st_multi (st_union(the_geom)) as geom
                        from  %s  
                        group by id
                     ) as a
                    join mid_feat_key as fe
                      on a.id = fe.org_id1 
                 ''' % tb
        self.db.execute( sqlcmd )
        
        if tb.find('a8') >= 0 or tb.find('a9') >= 0:
            sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7379, 'P', sm.the_geom
                    from %s as a
                    join mid_feat_key as fe
                      on a.id = fe.org_id1
                    join org_sm as sm
                      on a.citycenter = sm.id
                    ''' % tb
            self.db.execute( sqlcmd )
        