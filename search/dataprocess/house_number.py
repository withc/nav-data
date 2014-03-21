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
            select id, country, state, city, district, name, scheme,
                   CASE when f < l then first else last END,
                   CASE when f < l then last else first END
            from (
                select r.id, p.country, p.state, p.city, p.district, r.name, hn.scheme, hn.first, hn.last,
                       get_house_number(hn.first) as f, get_house_number(hn.last) as l
                  from mid_house_number_road    as r
                  join mid_address_range        as hn
                    on r.id = hn.id
                  join tmp_feat_lowest_place    as ff
                    on r.key = ff.key 
                  join tbl_place                as p
                    on ff.pkey = p.key
                ) as tbl
            '''
        self.db.do_big_insert(sqlcmd)
    
    def _hno_point(self):
        sqlcmd = '''
                insert into tbl_hno_point( id, country, state, city, district, street, num )
                select r.id, p.country, p.state, p.city, p.district, r.name, hn.num
                  from mid_house_number_road    as r
                  join mid_address_point        as hn
                    on r.id = hn.id
                  join tmp_feat_lowest_place    as ff
                    on r.key = ff.key
                  join tbl_place                as p
                    on ff.pkey = p.key
                 '''
        self.db.do_big_insert(sqlcmd)
        
        