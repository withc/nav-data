import entity

class CHouseNumber(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'house_num')
          
    def _do(self):
        self._do_tmp()
        self._hno_range()
        self._hno_point()
        self._bldg_point()

        
    def _do_tmp(self):
        self.logger.info('  do hno temp table')
        # get from link + street name
        sqlcmd = '''
                 insert into tmp_street_hno_id( id, org_link_id, mid_id)
                 select s.id, k.org_id1, m.id
                   from mid_link_road         as m
                   join mid_street_name       as n
                     on m.langcode = n.langcode and m.name = n.name
                   join tmp_street            as s
                     on m.key = s.key     and
                        n.id  = s.nameid
                   join mid_feat_key          as k
                     on s.key = k.feat_key
                  order by s.id
                 '''
        self.db.do_big_insert(sqlcmd)
        
        # get from place + street name
        sqlcmd = '''
                 insert into tmp_street_hno_id( id, org_link_id, mid_id)
                 select distinct s.id, 0, m.id
                   from mid_place_road        as m
                   join mid_street_name       as n
                     on (m.lang = n.langcode and m.name = n.name) or (m.lang = n.tr_lang and m.name = n.tr_name)
                   join tmp_street            as s
                     on m.pkey = s.pkey   and
                        n.id  = s.nameid
                  order by s.id
                 '''
        self.db.do_big_insert(sqlcmd)
        
        #get the org link which split to many rdb link
        sqlcmd = '''
                 insert into tmp_org_to_many_rdb_link( org_link_id, s_org, e_org, rdb_link_id, s_rdb, e_rdb, flag, seq )
                  select *, row_number() over ( partition by org_link_id order by abs( (s_org+e_org)/2 - 0.5 ) ) as seq
                   from (
                         select t.org_link_id, 
                                ST_Line_Locate_Point(g.geom, ST_StartPoint(mid_geom)) as s_org,
                                ST_Line_Locate_Point(g.geom, ST_EndPoint(mid_geom))   as e_org,
                                target_link_id, t.s_fraction , t.e_fraction, t.flag
                           from temp_link_org_rdb as t
                            join ( 
                                        select org_link_id
                                          from temp_link_org_rdb  
                                         group by org_link_id having count(*) > 1 
                                  ) as r
                               on t.org_link_id = r.org_link_id
                             join mid_feat_key  as f
                               on t.org_link_id = f.org_id1 and f.feat_type = 2000
                             join mid_street_to_geometry as fg
                                on f.feat_key = fg.key
                              join mid_street_geometry    as g
                                on fg.geomid = g.id
                         ) as f
                 '''
        self.db.do_big_insert(sqlcmd)
            
    def _hno_range(self):
        self._range_to_one_rdb()
        self._range_of_one_value_to_many_rdb()
        self._range_of_many_value_to_many_rdb()
        
    def _hno_point(self):
        self.logger.info('  do hno point')
        sqlcmd = '''
                 insert into tbl_street_hno_point( id, link_id, side, prefix, suffix, hno, lon, lat, entry_lon, entry_lat, rdb_link_id )
                 select s.id, s.org_link_id, 
                        case  
                          when rdb.flag = true and side = 1 then 2
                          when rdb.flag = true and side = 2 then 1
                          else side
                        end, 
                        srch_hno_prefix(h.num), srch_hno_suffix(h.num), h.num, 
                        srch_coord(h.dis_x), srch_coord(h.dis_y),
                        srch_coord( h.x ), srch_coord( h.y ), rdb.target_link_id
                   from mid_link_road            as r
                   join mid_address_point        as h
                     on r.id = h.id
                   join tmp_street_hno_id        as s
                     on s.mid_id = r.id
                   join (
                          select t.org_link_id,  t.target_link_id, t.flag
                            from temp_link_org_rdb        as t
                       left join tmp_org_to_many_rdb_link as m
                              on t.org_link_id    = m.org_link_id  and
                                 t.target_link_id = m.rdb_link_id
                            where m.seq = 1 or m.seq is null
                         ) as rdb
                      on s.org_link_id = rdb.org_link_id
                 '''
        self.db.do_big_insert(sqlcmd)
        # get the hno in place + street name
        sqlcmd = '''
                 insert into tbl_street_hno_point( id, link_id, side, prefix, suffix, hno, lon, lat, entry_lon, entry_lat, rdb_link_id )
                 select s.id, s.org_link_id, h.side, 
                        srch_hno_prefix(h.num), srch_hno_suffix(h.num), h.num, 
                        srch_coord(h.dis_x), srch_coord(h.dis_y),
                        srch_coord( h.x ), srch_coord( h.y ), 0
                   from mid_place_road           as r
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
                 select row_number() over( order by p.area0, p.area1, p.area2, p.area3, b.num ), 
                        p.area0, p.area1, p.area2, p.area3, f.org_id1, 
                        case  
                          when rdb.flag = true and side = 1 then 2
                          when rdb.flag = true and side = 2 then 1
                          else side
                        end, b.num,
                        srch_coord(b.x), srch_coord(b.y),
                        srch_coord( b.entry_x ), srch_coord( b.entry_y ), rdb.target_link_id
                   from mid_bldg_point    as b
                   join tmp_place_area    as p
                     on b.pkey = p.key
                   join mid_feat_key      as f
                     on b.lkey = f.feat_key
                   join (
                          select t.org_link_id,  t.target_link_id, t.flag
                            from temp_link_org_rdb        as t
                       left join tmp_org_to_many_rdb_link as m
                              on t.org_link_id    = m.org_link_id  and
                                 t.target_link_id = m.rdb_link_id
                           where m.seq = 1 or m.seq is null
                         ) as rdb
                      on f.org_id1 = rdb.org_link_id
                 '''
        self.db.do_big_insert(sqlcmd)
    
    def _range_to_one_rdb(self):
        #org link to only one rdb link
        sqlcmd = '''
                 insert into tbl_street_hno_range( id, link_id, side, scheme, prefix, suffix, 
                                                   f_hno, l_hno, rdb_link_id, s_fraction, e_fraction )
                 select s.id, s.org_link_id,
                        CASE  
                           when flag and h.side = 1 then 2
                           when flag and h.side = 2 then 1
                           else h.side
                        END,
                        h.scheme, 
                        srch_hno_prefix(h.first), srch_hno_suffix(h.first),
                        CASE flag when false then h.first else h.last  END, 
                        CASE flag when false then h.last  else h.first END,
                        rdb.target_link_id, 
                        CASE flag when false then s_rdb else e_rdb END, 
                        CASE flag when false then e_rdb else s_rdb END
                   from mid_link_road            as r
                   join mid_address_range        as h
                     on r.id = h.id
                   join tmp_street_hno_id        as s
                     on s.mid_id = r.id
                   join (
                          select t.org_link_id, (t.s_fraction*65535)::int as s_rdb,(t.e_fraction*65535)::int as e_rdb, t.target_link_id, t.flag
                            from temp_link_org_rdb as t
                           where not exists ( 
                                  select 1
                                    from tmp_org_to_many_rdb_link  as r
                                   where t.org_link_id = r.org_link_id
                                )
                        ) as rdb
                     on s.org_link_id = rdb.org_link_id
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _range_of_one_value_to_many_rdb(self):
        #the range have only one value, select the rdb link which locate in middle
        sqlcmd = '''
                 insert into tbl_street_hno_range( id, link_id, side, scheme, prefix, suffix, 
                                                   f_hno, l_hno, rdb_link_id, s_fraction, e_fraction )
                 select s.id, s.org_link_id,
                        CASE  
                           when flag and h.side = 1 then 2
                           when flag and h.side = 2 then 1
                           else h.side
                        END as side,
                        h.scheme, 
                        srch_hno_prefix(h.first), srch_hno_suffix(h.first),
                        h.first, h.last,
                        rdb.rdb_link_id, 
                        CASE flag when false then s_rdb else e_rdb END, 
                        CASE flag when false then e_rdb else s_rdb END
                   from mid_link_road            as r
                   join mid_address_range        as h
                     on r.id = h.id
                   join tmp_street_hno_id        as s
                     on s.mid_id = r.id
                   join (
                          select org_link_id, rdb_link_id, flag,
                                 (s_rdb*65535)::int as s_rdb, (e_rdb*65535)::int as e_rdb
                            from tmp_org_to_many_rdb_link
                           where seq = 1
                        ) as rdb
                     on s.org_link_id = rdb.org_link_id
                  where h.first = h.last
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _range_of_many_value_to_many_rdb(self):
        #the range have many value and org link refer to many rdb link
        #we need split the range and distribute the sub-range to many rdb link
        sqlcmd = '''
               insert into tbl_street_hno_range( id, link_id, side, scheme, prefix, suffix, 
                                                f_hno, l_hno, rdb_link_id, s_fraction, e_fraction )
               select id, org_link_id,
                        CASE  
                           when flag and  side = 1 then 2
                           when flag and  side = 2 then 1
                           else side
                        END as side,
                        scheme, 
                        f_pre, f_suf,
                        f_pre||s::varchar||f_suf, f_pre||e::varchar||f_suf,
                        rdb_link_id, 
                        CASE flag when false then s_rdb else e_rdb END, 
                        CASE flag when false then e_rdb else s_rdb END
              from ( 
                   select id, side, scheme, org_link_id, rdb_link_id, s_rdb, e_rdb, flag, 
                          f_pre, f_suf, f_num, l_pre, l_suf, l_num, 
                          srch_s_e_num( scheme, s_num, e_num, true) as s,
                          srch_s_e_num( scheme, s_num, e_num, false) as e
                     from ( 
                           select id, side, scheme, org_link_id, rdb_link_id, s_rdb, e_rdb, flag,
                                  f_pre, f_suf, f_num, l_pre, l_suf, l_num,
                                  f_num + (s_org*(l_num-f_num)) as s_num, f_num + (e_org*(l_num-f_num)) as e_num
                             from (
                                  select s.id, h.side, h.scheme, 
                                         srch_hno_prefix(h.first) as f_pre, srch_hno_num(h.first) as f_num, srch_hno_suffix(h.first) as f_suf, 
                                         srch_hno_prefix(h.last)  as l_pre, srch_hno_num(h.last) as l_num,  srch_hno_suffix(h.last) as l_suf,
                                         rdb.*
                                    from mid_link_road            as r
                                    join mid_address_range        as h
                                      on r.id = h.id
                                    join tmp_street_hno_id        as s
                                      on s.mid_id = r.id
                                    join tmp_org_to_many_rdb_link as rdb
                                      on s.org_link_id = rdb.org_link_id
                                   where h.first <> h.last
                                   order by id
                                   ) as t2
                            ) as t3
                    ) as t4
              where s <> -1 and e <> -1
                 '''
        self.db.do_big_insert(sqlcmd)
       