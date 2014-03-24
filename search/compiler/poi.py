import entity

class CPoi(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'poi')
          
    def _do(self):
        self._do_gen_poiid()
        self._do_poi_info()
        self._do_poi_address()
        self._do_poi_name()

    def _do_gen_poiid(self):
        sqlcmd = '''
                 insert into tmp_poi( key, type, id)
                 select p.key, p.type, row_number() over (order by pa.area0, pa.area1, p.key )
                   from mid_poi               as p
                   join tmp_feat_lowest_place as lp
                     on p.key = lp.key
                   join tmp_place_area        as pa
                     on lp.pkey = pa.key
                 '''
        self.db.do_big_insert(sqlcmd)
    
    def _do_poi_info(self):
        sqlcmd = '''
                 insert into tbl_poi_info( id, lon, lat, entry_lon, entry_lat, 
                                           tel, fax, email, internet, postcode,
                                           imp, gen1, gen2, gen3, 
                                           area0, area1, area2, area3, meshid )
                 select p.id, st_x(g.geom)*100000, st_y(g.geom)*100000, st_x(g2.geom)*100000, st_y(g2.geom)*100000,
                        COALESCE(te.attr_value, ''), 
                        COALESCE(fa.attr_value, ''),
                        COALESCE(em.attr_value, ''),
                        COALESCE(it.attr_value, ''), 
                        po.pocode,
                        c.imp, c.gen1, c.gen2, c.gen3,
                        pa.area0, pa.area1, pa.area2, pa.area3 
                   from tmp_poi                  as p
                   join mid_poi                  as mp
                     on p.key = mp.key
                   join mid_poi_category         as c
                     on mp.gen_code = c.per_code
                   join mid_feature_to_geometry  as fg
                     on p.key   = fg.key and fg.code = 7000
                   join mid_geometry             as g
                     on fg.geomid = g.id
                   join tmp_feat_lowest_place    as fp
                     on p.key   = fp.key
                   join tmp_place_area           as pa
                     on fp.pkey = pa.key
              left join mid_feature_to_feature   as ff
                     on p.key = ff.fkey and ff.code = 7004
              left join mid_postcode             as po
                     on ff.tkey = po.key
              left join mid_feature_to_geometry  as fg2
                     on p.key = fg.key and fg.code = 9920
              left join mid_geometry             as g2
                     on fg2.geomid = g2.id
              left join mid_poi_attr_value       as te
                     on p.key = te.key  and  te.attr_type = 'TL'
              left join mid_poi_attr_value       as fa
                     on p.key = fa.key  and  fa.attr_type = 'TX'
              left join mid_poi_attr_value       as em
                     on p.key = em.key  and  em.attr_type = '8M'
              left join mid_poi_attr_value       as it
                     on p.key = it.key  and  it.attr_type = '8L'
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _do_poi_address(self):
        sqlcmd = '''
                 insert into tbl_poi_address( id, lang, street, hno )
                 select p.id, '', 
                        COALESCE(st.attr_value, ''), 
                        COALESCE(hn.attr_value, '')
                   from tmp_poi            as p
              left join mid_poi_attr_value as st
                     on p.key = st.key and st.attr_type = '6T'
              left join mid_poi_attr_value as hn
                     on p.key = hn.key and hn.attr_type = '9H'
                 ''' 
        self.db.do_big_insert(sqlcmd)
        
    def _do_poi_name(self):
        sqlcmd = '''
                 insert into tbl_poi_name( id, type, lang, name )
                 select p.id, fn.nametype, n.langcode, n.name
                   from tmp_poi             as p
                   join mid_feature_to_name as fn
                     on p.key = fn.key
                   join mid_name            as n
                     on fn.nameid = n.id
                 '''
        self.db.do_big_insert(sqlcmd)
        
        