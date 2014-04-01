import entity

class CHouseNumber(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'house_num')
          
    def _do(self):
        self._do_tmp()
        self._hno_range()
        self._hno_point()
        self._bldg_point()
        self._update_to_rdb_link()
        
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
        self.logger.info('  do hno range')
        sqlcmd = '''
                 insert into tbl_street_hno_range( id, link_id, side, scheme, prefix, suffix, 
                                                   f_hno, l_hno, rdb_link_id, s_fraction, e_fraction )
                 select s.id, s.org_link_id, h.side, h.scheme, 
                        srch_hno_prefix(h.first), srch_hno_suffix(h.first), h.first, h.last,
                        0, 0, 0
                   from mid_house_number_road    as r
                   join mid_address_range        as h
                     on r.id = h.id
                   join tmp_street_hno_id        as s
                     on s.mid_id = r.id
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _hno_point(self):
        self.logger.info('  do hno point')
        sqlcmd = '''
                 insert into tbl_street_hno_point( id, link_id, side, prefix, suffix, hno, lon, lat, entry_lon, entry_lat, rdb_link_id )
                 select s.id, s.org_link_id, h.side, 
                        srch_hno_prefix(h.num), srch_hno_suffix(h.num), h.num, 
                        srch_coord(h.dis_x), srch_coord(h.dis_y),
                        srch_coord( h.x ), srch_coord( h.y ), 0
                   from mid_house_number_road    as r
                   join mid_address_point        as h
                     on r.id = h.id
                   join tmp_street_hno_id        as s
                     on s.mid_id = r.id
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _bldg_point(self):
        self.logger.info('  do bldg point')
        sqlcmd = '''
                 insert into tbl_bldg_point( id, area0,area1, area2, area3, link_id, side, hno, lon, lat, entry_lon, entry_lat, rdb_link_id )
                 select p.area0, p.area1, p.area2, p.area3, f.org_id1, b.side, b.num,
                        srch_coord(b.x), srch_coord(b.y),
                        srch_coord( b.entry_x ), srch_coord( b.entry_y ), 0
                   from mid_bldg_point    as b
                   join tmp_place_area    as p
                     on b.pkey = p.key
                   join mid_feat_key      as f
                     on b.lkey = f.feat_key
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _update_to_rdb_link(self):
        self.logger.info('  update to rdb_link_id')
        sqlcmd = '''
                 update tbl_street_hno_range as h 
                 set  rdb_link_id = u.target_link_id, s_fraction = u.s, e_fraction = u.e
                 from  (
                        select org_link_id, target_link_id, (s*65535)::int as s, (e*65535)::int as e
                         from (
                              select org_link_id, target_link_id, 
                                     case flag when false then s_fraction else e_fraction end as s, 
                                     case flag when false then e_fraction else s_fraction end as e, 
                                     row_number() over ( partition by org_link_id ) as seq
                                from temp_link_org_rdb
                              ) as t  
                              where t.seq = 1
                       ) as u
                      where u.org_link_id = h.link_id 
                 '''
        self.db.do_big_insert(sqlcmd)
        
        sqlcmd = '''
                 update tbl_street_hno_point as h 
                    set rdb_link_id = u.target_link_id
                    from (
                        select org_link_id, target_link_id  
                         from ( select org_link_id, target_link_id,
                                      row_number() over ( partition by org_link_id ) as seq
                                 from temp_link_org_rdb 
                              ) as t
                        where t.seq = 1 
                      ) as u
                      where u.org_link_id = h.link_id 
                 '''
        self.db.do_big_insert(sqlcmd)
        
        sqlcmd = '''
                 update tbl_bldg_point as h 
                    set rdb_link_id = u.target_link_id
                    from (
                        select org_link_id, target_link_id  
                         from ( select org_link_id, target_link_id,
                                      row_number() over ( partition by org_link_id ) as seq
                                 from temp_link_org_rdb 
                              ) as t
                        where t.seq = 1 
                      ) as u
                      where u.org_link_id = h.link_id 
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