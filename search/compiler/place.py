import config.config
import entity

class CPlace(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'place')
          
    def _do(self):
        self._do_temp_table()
        sqlcmd = '''
                 insert into tmp_place_name( key, type, lang, name)
                 select p.key, p.type,  n.langcode, n.name
                   from mid_place            as p
                   join mid_feature_to_name  as pn
                     on p.key = pn.key and p.type = pn.type
                   join mid_name             as n
                     on pn.nameid = n.id and n.langcode = '%s'
                 ''' % config.config.Config.get_instance().getLangCode()
                 
        self.db.do_big_insert(sqlcmd)
        
        sqlcmd = '''
                 insert into tbl_place( key, type, country, state, city, district )
                 select a.key, a.type, n0.name, n1.name, n8.name, 
                        COALESCE( n9.name, '' )
                   from mid_place_admin  as a
                   join tmp_place_name   as n0
                     on a.a0 = n0.key
                   join tmp_place_name   as n1
                     on a.a1 = n1.key
                   join tmp_place_name   as n8
                     on a.a8 = n8.key
              left join tmp_place_name   as n9
                     on a.a9 = n9.key
                   where a.a8 <> 0 or a.a9 <> 0
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _do_temp_table(self):
        ''' when a feature belong to a9, we also add a8( the a9's parent) to table mid_feature_to_feature,
            so, we must filter the a8 record if it is already refer to his a9.
            tmp_feat_lowest_place will contain the lowest admin place only.
        '''
        sqlcmd = '''
               insert into tmp_feat_lowest_place( key, type, pkey, ptype )
                 with ff ( fkey, ftype, tkey, ttype, a8 ) as 
                 (
                 select ff.fkey, ff.ftype, ff.tkey, ff.ttype, p.a8
                   from mid_feature_to_feature  as ff
                   join mid_place_admin         as p
                     on ff.tkey  = p.key  and 
                        ff.code  = 7001   and 
                        ff.ttype in ( 3009, 3010 )
                 )
                 select ff.fkey, ff.ftype, ff.tkey, ff.ttype
                   from ff
                   join (
                          select fkey, ftype, a8, max(ttype) as ttype
                            from ff
                           group by fkey, ftype, a8
                         ) as t
                      on ff.fkey  = t.fkey  and 
                         ff.ftype = t.ftype and
                         ff.a8    = t.a8    and
                         ff.ttype = t.ttype
                 '''
        self.db.do_big_insert(sqlcmd)
        
        
        
        
        
        
        
        