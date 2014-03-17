import entity

class CHouseNumber(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'house_num')
          
    def _do(self):
        self._hno_range()
        self._hno_point()
    
    def _hno_range(self):
        sqlcmd = '''
                insert into tbl_hno_range( id, country, state, city, district, street, scheme, first, last )
                select r.id, p.country, p.state, p.city, p.district, r.name, hn.scheme, hn.first, hn.last
                  from mid_house_number_road    as r
                  join mid_address_range        as hn
                    on r.id = hn.id
                  join mid_feature_to_feature   as ff
                    on r.key = ff.fkey and ff.code = 7001
                  join tbl_place                as p
                    on ff.tkey = p.key and p.type = 3010
                 '''
        self.db.do_big_insert(sqlcmd)
    
    def _hno_point(self):
        sqlcmd = '''
                insert into tbl_hno_point( id, country, state, city, district, street, num )
                select r.id, p.country, p.state, p.city, p.district, r.name, hn.num
                  from mid_house_number_road    as r
                  join mid_address_point        as hn
                    on r.id = hn.id
                  join mid_feature_to_feature   as ff
                    on r.key = ff.fkey and ff.code = 7001
                  join tbl_place                as p
                    on ff.tkey = p.key and p.type = 3010 
                 '''
        self.db.do_big_insert(sqlcmd)