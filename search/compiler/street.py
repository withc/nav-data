import entity

class CLink(entity.CEntity):
    def __init__(self, database):
        entity.CEntity.__init__(self, database, 'link')
          
    def _do(self):
        self._do_gen_id()
        self._do_street_infor()
        self._do_street_name()
        
    def _do_gen_id(self):
        sqlcmd = '''
            insert into tmp_street( key, type, pkey, ptype, nameid, id )
            select key, type, pkey,  ptype, nameid, dense_rank() over ( order by  pkey, ptype, nameid )
              from (
                        select fp.pkey, fp.ptype, l.key, l.type, n.nameid 
                          from mid_link              as l
                          join tmp_feat_lowest_place as fp
                            on l.key = fp.key
                          join mid_feature_to_name   as n
                            on l.key = n.key
                    ) as t
              order by pkey, nameid
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _do_street_name(self):
        sqlcmd = '''
                 insert into tbl_street_name( id, type, lang, name )
                 select s.id, fn.nametype, n.langcode, n.name
                   from tmp_street  as s
                   join mid_feature_to_name  as fn
                     on s.key = fn.key
                   join mid_name    as n
                     on fn.nameid = n.id
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _do_street_infor(self):
        sqlcmd = '''
                 insert into tbl_street_info( id, level, area0, area1, area2, area3, lon, lat )
                 select s.id, p.level, p.area0, p.area1, p.area2, p.area3, 0, 0
                   from tmp_street        as s
                   join tmp_place_area    as p
                     on s.pkey = p.key
                 '''
        self.db.do_big_insert(sqlcmd)
           
    def _do_full_name(self):
        sqlcmd = '''
                 insert into tbl_road_full( key, type, lang, country, state, city, district, road )
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
        