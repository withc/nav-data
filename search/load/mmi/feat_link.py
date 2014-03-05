import load.feature

class CLink(load.feature.CFeature):
    def __init__(self ):
        print "mmi's link"
        load.feature.CFeature.__init__(self, 'link')
 
    def _domake_key(self):
        sqlcmd = '''
                 insert into mid_feat_key( feat_type, org_id1, org_id2 )
                 select 2000, id, feattyp
                   from org_city_nw_gc_polyline
                 '''
        self.db.execute( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_link( key, type )
                    select fe.feat_key, fe.feat_type
                      from org_city_nw_gc_polyline  as nw
                      join mid_feat_key             as fe
                        on nw.id = fe.org_id1 and nw.feattyp = fe.org_id2
                 '''
        self.db.execute( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7000,'L', nw.the_geom
                      from org_city_nw_gc_polyline  as nw
                      join mid_feat_key             as fe
                        on nw.id = fe.org_id1 and nw.feattyp = fe.org_id2
                 '''
        self.db.execute( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
                  insert into temp_feat_name( key, type, nametype, langcode, name )
                    with f ( key, type, namelc, name, pop_name, alt_name, routenum )
                    as ( select fe.feat_key, fe.feat_type, namelc, name, pop_name, alt_name, routenum
                           from org_city_nw_gc_polyline  as nw
                           join mid_feat_key             as fe
                             on nw.id = fe.org_id1 and nw.feattyp = fe.org_id2
                          where nw.name     is not null or
                                nw.pop_name is not null or
                                nw.alt_name is not null or
                                nw.routenum is not null
                       )
                 select key, type, 'ON', namelc, name     
                   from f where name is not null
                 union
                 select key, type, 'AN', namelc, pop_name 
                   from f where pop_name is not null
                 union
                 select key, type, 'AN', namelc, regexp_split_to_table(alt_name, ';') 
                   from f where alt_name is not null
                 union
                 select key, type, 'RN', namelc, routenum 
                   from f where routenum is not null
                 '''
        self.db.execute( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        sqlcmd = '''
                 '''
        self.db.execute( sqlcmd )
        