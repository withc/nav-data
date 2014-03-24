import entity

class CLink(entity.CEntity):
    def __init__(self, database):
        entity.CEntity.__init__(self, database, 'link')
          
    def _do(self):
        self._do_gen_id()
        
    def _do_gen_id(self):
        sqlcmd = '''
            insert into tmp_street( key, type, pkey, ptype, id )
            select key, type, pkey, ptype, dense_rank() over ( order by  pkey, ptype, n )
            from (
                 select pkey, ptype, key, type, array_agg( nameid order by nameid ) as n
                 from (
                        select fp.pkey, fp.ptype, l.key, l.type, n.nameid 
                          from mid_link              as l
                          join tmp_feat_lowest_place as fp
                            on l.key = fp.key
                          from mid_feature_to_name   as n
                            on l.key = n.key
                        ) as t
                  group by t.pkey, t.ptype, t.key, t.type
                  ) as t2
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _do_full_name(self):
        sqlcmd = '''
                 insert into tbl_road( key, type, lang, country, state, city, district, road )
                 select 1, 0, f.langcode, p.country, p.state, p.city, p.district,  f.name
                   from (
                          select distinct ff.pkey, ln.langcode, ln.name
                            from mid_link              as l
                            join temp_feat_name        as ln
                              on l.key = ln.key
                            join tmp_feat_lowest_place as ff
                              on l.key = ff.key
                        ) as f
                   join tbl_place as p
                     on f.pkey = p.key and f.langcode = p.lang 
                   order by f.langcode, f.pkey
                 '''
        self.db.do_big_insert(sqlcmd)