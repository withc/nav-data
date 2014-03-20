import load.feature

class CHouseNumber(load.feature.CFeature):
    def __init__(self ):
        print "mmi's house number"
        load.feature.CFeature.__init__(self, 'house_num')
 
    def _domake_key(self):
        sqlcmd = '''
                 insert into temp_road_link( linkid, feattyp, langcode, name )
                 select id, feattyp, namelc, fullname
                   from org_gc
                  where l_struct not in ( 0, 1) or
                        r_struct not in ( 0, 1) 
                 '''
        #self.db.do_big_insert( sqlcmd )
    
    def _domake_feature(self):
        sqlcmd = '''
                 insert into mid_house_number_road( id, key, type, langcode, name )
                 select t.id, f.feat_key, f.feat_type, t.langcode, t.name
                   from temp_road_link    as t
                   join mid_feat_key      as f
                     on t.linkid = f.org_id1 and t.feattyp = f.org_id2
                 '''
        #self.db.do_big_insert( sqlcmd )

    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        self._make_hn_by_link()
        self._make_hn_by_point()
        
    def _domake_relation(self):
        pass
    
    def _make_hn_by_link(self):
        pass

    def _make_hn_by_point(self):
       pass
        