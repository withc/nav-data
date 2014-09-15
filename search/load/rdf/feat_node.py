import load.feature

class CNode(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'node')
 
    def _domake_key(self):
        sqlcmd = '''
                 insert into mid_feat_key( feat_type, org_id1, org_id2 )
                 select 1002, node_id, 1002
                   from ( 
                          select l.ref_node_id as node_id
                            from rdf_link      as l
                            join rdf_nav_link  as r
                              on r.link_id = l.link_id
                          union 
                          select l.nonref_node_id as node_id
                            from rdf_link      as l
                            join rdf_nav_link  as r
                              on r.link_id = l.link_id
                         ) as n
                    order by node_id
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_node( key, type )
                    select fe.feat_key, fe.feat_type 
                      from rdf_node       as n
                      join mid_feat_key   as fe
                        on n.node_id = fe.org_id1 and  fe.org_id2 = 1002
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert into temp_street_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7000,'P',
                           ST_SetSRID(st_makepoint( n.lon/100000.0, n.lat/100000.0 ), 4326)
                      from rdf_node       as n
                      join mid_feat_key   as fe
                        on n.node_id = fe.org_id1 and  fe.org_id2 = 1002
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass
        