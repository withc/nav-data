import load.feature

class CLink(load.feature.CFeature):
    def __init__(self ):
        print "tomtom's link feature"
        load.feature.CFeature.__init__(self,'link')

    def _domake_key(self):
        # copy all link, even it has no name.
        # some link that has no name is the closest road poi was located.
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 2000, id, feattyp 
                      from org_nw as nw
                     where feattyp in ( 4110, 4130 )
                 '''
        self.db.execute( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_link( key, type )
                    select fe.feat_key, fe.feat_type
                      from org_nw       as nw
                      join mid_feat_key as fe
                        on nw.id = fe.org_id1 and nw.feattyp = fe.org_id2
                 '''
        self.db.execute( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7000,'L', nw.the_geom
                      from org_nw       as nw
                      join mid_feat_key as fe
                        on nw.id = fe.org_id1 and nw.feattyp = fe.org_id2
                 '''
        self.db.execute( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
                    insert into temp_feat_name( key, type, nametype, langcode, name )
                    select fe.feat_key, fe.feat_type,  
                            CASE  
                              WHEN gc.nametyp&1 <> 0 THEN 'ON'
                              WHEN gc.nametyp&4 <> 0 THEN 'RN'
                              WHEN gc.nametyp&8 <> 0 THEN 'BU'
                              ELSE 'AN'
                            END as nametype,
                           gc.namelc, gc.fullname
                    from org_gc       as gc
                    join mid_feat_key as fe
                      on gc.id = fe.org_id1 and gc.feattyp = fe.org_id2
                 '''
        self.db.execute( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select  fe.feat_key, fe.feat_type, 7001, f1.feat_key, f1.feat_type
                    from org_ta       as ta
                    join mid_feat_key as fe
                      on ta.aretyp   in (1119,1120) and
                         ta.id       = fe.org_id1   and
                         ta.trpeltyp = fe.org_id2
                    join mid_feat_key as f1
                      on ta.areid = f1.org_id1 and ta.aretyp = f1.org_id2
                 '''
        self.db.execute( sqlcmd )
        