import entity

class CPlace(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'place')
          
    def _do(self):
        sqlcmd = '''
                 insert into tmp_place_name( key, type, lang, name)
                 select p.key, p.type,  n.langcode, n.name
                   from mid_place            as p
                   join mid_feature_to_name  as pn
                     on p.key = pn.key and p.type = pn.type
                   join mid_name             as n
                     on pn.nameid = n.id and n.langcode = 'IND'
                 '''
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