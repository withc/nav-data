import convert.feature

class CHouseNumber(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'house_num')
 
    def _domake_key(self):
        sqlcmd = '''
                 insert into temp_road_link( linkid, feattyp, langcode, name )
                 select id, feattyp, namelc, fullname
                   from org_gc
                  where l_struct not in ( 0, 1) or
                        r_struct not in ( 0, 1) 
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_feature(self):
        sqlcmd = '''
                 insert into mid_link_road( id, key, type, langcode, name )
                 select t.id, f.feat_key, f.feat_type, t.langcode, t.name
                   from temp_road_link    as t
                   join mid_feat_key      as f
                     on t.linkid = f.org_id1 and t.feattyp = f.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )

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
        sqlcmd = '''
               insert into mid_address_range( id, side, scheme, first, last )
                 with hn ( id, l, l_f, l_t, r, r_f, r_t ) as
                 (
                   select t.id, g.l_struct, g.l_f_f_add, g.l_t_f_add,
                                g.r_struct, g.r_f_f_add, g.r_t_f_add 
                     from temp_road_link     as t
                     join org_gc             as g
                       on t.linkid   = g.id       and
                          t.feattyp  = g.feattyp  and
                          t.name     = g.fullname and
                          t.langcode = g.namelc
                  )
                  select id, 1, 
                         case 
                           when l = 2 then 'E'
                           when l = 3 then 'O'
                           when l = 4 then 'M'
                           else '$'
                         end, l_f, l_t from hn where l not in (0,1)
                 union
                 select id, 2, 
                         case 
                           when r = 2 then 'E'
                           when r = 3 then 'O'
                           when r = 4 then 'M'
                           else '$'
                         end, r_f, r_t from hn where r not in (0,1)
                 '''
        self.db.do_big_insert( sqlcmd  )

    def _make_hn_by_point(self):
       pass
        