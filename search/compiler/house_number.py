import entity

class CHouseNumber(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'house_num')
          
    def _do(self):
        self._do_tmp()
        self._hno_range()
        self._hno_point()
        
    def _do_tmp(self):
        sqlcmd = '''
                 insert into tmp_street_hno_id( id, org_link_id, mid_id)
                 select s.id, k.org_id1, m.id
                   from mid_house_number_road as m
                   join mid_name              as n
                     on m.langcode = n.langcode and m.name = n.name
                   join tmp_street            as s
                     on m.key = s.key     and
                        n.id  = s.nameid
                   join mid_feat_key          as k
                     on s.key = k.feat_key
                  order by s.id
                 '''
        self.db.do_big_insert(sqlcmd)
            
    def _hno_range(self):
        sqlcmd = '''
                 insert into tbl_street_hno_range( id, link_id, side, scheme, prefix, suffix, f_hno, l_hno )
                 select s.id, s.org_link_id, h.side, h.scheme, 
                        srch_hno_prefix(h.first), srch_hno_suffix(h.first), h.first, h.last
                   from mid_house_number_road    as r
                   join mid_address_range        as h
                     on r.id = h.id
                   join tmp_street_hno_id        as s
                     on s.mid_id = r.id
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _hno_point(self):
        sqlcmd = '''
                 insert into tbl_street_hno_point( id, link_id, side, prefix, suffix, hno, lon, lat, entry_lon, entry_lat )
                 select s.id, s.org_link_id, h.side, 
                        srch_hno_prefix(h.num), srch_hno_suffix(h.num), h.num, 
                        srch_coord(h.dis_x), srch_coord(h.dis_y),
                        srch_coord( h.x ), srch_coord( h.y )
                   from mid_house_number_road    as r
                   join mid_address_point        as h
                     on r.id = h.id
                   join tmp_street_hno_id        as s
                     on s.mid_id = r.id
                 '''
        self.db.do_big_insert(sqlcmd)
    
#     def _hno_range(self):
#         sqlcmd = '''
#             insert into tbl_hno_range( id, country, state, city, district, street, scheme, first, last )
#             select id, country, state, city, district, name, scheme,
#                    CASE when f < l then first else last END,
#                    CASE when f < l then last else first END
#             from (
#                 select r.id, p.country, p.state, p.city, p.district, r.name, hn.scheme, hn.first, hn.last,
#                        get_house_number(hn.first) as f, get_house_number(hn.last) as l
#                   from mid_house_number_road    as r
#                   join mid_address_range        as hn
#                     on r.id = hn.id
#                   join tmp_feat_lowest_place    as ff
#                     on r.key = ff.key 
#                   join tbl_place                as p
#                     on ff.pkey = p.key
#                 ) as tbl
#             '''
#         self.db.do_big_insert(sqlcmd)
#     
#     def _hno_point(self):
#         sqlcmd = '''
#                 insert into tbl_hno_point( id, country, state, city, district, street, num )
#                 select r.id, p.country, p.state, p.city, p.district, r.name, hn.num
#                   from mid_house_number_road    as r
#                   join mid_address_point        as hn
#                     on r.id = hn.id
#                   join tmp_feat_lowest_place    as ff
#                     on r.key = ff.key
#                   join tbl_place                as p
#                     on ff.pkey = p.key
#                  '''
#         self.db.do_big_insert(sqlcmd)
#         
#         