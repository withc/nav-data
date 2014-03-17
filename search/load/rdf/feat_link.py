import load.feature

class CLink(load.feature.CFeature):
    def __init__(self ):
        print "rdf's link"
        load.feature.CFeature.__init__(self, 'link')
 
    def _domake_key(self):
        sqlcmd = '''
                 insert into mid_feat_key( feat_type, org_id1, org_id2 )
                 select 2000, link_id, 2000
                   from ( 
                         select distinct link_id
                           from rdf_road_link
                          order by link_id
                        ) as l
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_link( key, type )
                    select fe.feat_key, fe.feat_type
                      from ( 
                           select distinct link_id
                             from rdf_road_link
                            order by link_id
                           )              as l
                      join mid_feat_key   as fe
                        on l.link_id = fe.org_id1 and   fe.org_id2 = 2000
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        sqlcmd = '''
                 '''
        self.db.do_big_insert( sqlcmd )
        