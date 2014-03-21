import entity

class CLink(entity.CEntity):
    def __init__(self, database):
        entity.CEntity.__init__(self, database, 'link')
          
    def _do(self):
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