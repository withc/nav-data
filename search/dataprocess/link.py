import entity

class CLink(entity.CEntity):
    def __init__(self, database):
        entity.CEntity.__init__(self, database, 'link')
          
    def _do(self):
        sqlcmd = '''
                 insert into tbl_road( key, type, lang, country, state, city, district, road )
                 select distinct 1, 0, ln.langcode, p.country, p.state, p.city, p.district,  ln.name
                   from mid_link  as l
                   join temp_feat_name as ln
                     on l.key = ln.key
                   join tmp_feat_lowest_place as ff
                     on l.key = ff.key
                   join tbl_place as p
                     on ff.pkey = p.key and ln.langcode = p.lang 
                   order by ln.langcode, p.country, p.state, p.city, p.district,  ln.name
                 '''
        self.db.do_big_insert(sqlcmd)