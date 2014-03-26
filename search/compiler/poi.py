import entity

class CPoi(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'poi')
          
    def _do(self):
        self._do_gen_poiid()
        self._do_poi_geom()
        self._do_poi_attr()
        self._do_poi_infor()
        self._do_poi_address()
        self._do_poi_name()

    def _do_gen_poiid(self):
        self.logger.info('  do gen id')
        sqlcmd = '''
                 insert into tmp_poi( key, type, id)
                 select p.key, p.type, row_number() over (order by pa.area0, pa.area1, p.key )
                   from mid_poi               as p
                   join mid_feature_to_feature as lp
                     on p.key = lp.fkey and lp.code = 7001
                   join tmp_place_area        as pa
                     on lp.tkey = pa.key
                 '''
        self.db.do_big_insert(sqlcmd)
    
    def _do_poi_infor(self):
        self.logger.info('  do poi infor')
        sqlcmd = '''
                 insert into tbl_poi_info( id, lon, lat, entry_lon, entry_lat, 
                                           tel, fax, email, internet, postcode,
                                           imp, gen1, gen2, gen3, 
                                           area0, area1, area2, area3, meshid )
                 select p.id, g.lon, g.lat, g.entry_lon, g.entry_lat, 
                        COALESCE( at.tel,      ''), 
                        COALESCE( at.fax,      ''), 
                        COALESCE( at.email,    ''),
                        COALESCE( at.internet, ''),
                        po.pocode,
                        c.imp, c.gen1, c.gen2, c.gen3,
                        pa.area0, pa.area1, pa.area2, pa.area3, 0
                   from tmp_poi                  as p
                   join tmp_poi_geom             as g
                     on p.id = g.id
              left join tmp_poi_attr             as at
                     on p.id = at.id
                   join mid_poi                  as mp
                     on p.key = mp.key
                   join mid_poi_category         as c
                     on mp.gen_code = c.per_code
                   join tmp_feat_lowest_place    as fp
                     on p.key   = fp.key
                   join tmp_place_area           as pa
                     on fp.pkey = pa.key
              left join mid_feature_to_feature   as ff
                     on p.key = ff.fkey and ff.code = 7004
              left join mid_postcode             as po
                     on ff.tkey = po.key
                  order by p.id
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _do_poi_address(self):
        self.logger.info('  do poi address')
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
                  order by p.id
                 ''' 
        self.db.do_big_insert(sqlcmd)
        
    def _do_poi_name(self):
        self.logger.info('  do poi name')
        sqlcmd = '''
                 insert into tbl_poi_name( id, type, lang, name )
                 select p.id, fn.nametype, n.langcode, n.name
                   from tmp_poi             as p
                   join mid_feature_to_name as fn
                     on p.key = fn.key
                   join mid_name            as n
                     on fn.nameid = n.id
                  order by p.id
                 '''
        self.db.do_big_insert(sqlcmd)
    
    def _do_poi_attr(self):
        self.logger.info('  do poi attr')
        # each attribut, we only choice 1 item. we will fix the problem at next time.
        sqlcmd = '''
                 insert into tmp_poi_attr( id, tel, fax, email, internet )
                 with att ( key, type, attr_type, attr_value)
                   as (
                       select key, type, attr_type, attr_value 
                         from (
                               select key, type, attr_type, attr_value, 
                                      row_number() over ( partition by key, attr_type ) as seq
                                 from mid_poi_attr_value
                               ) as t
                        where t.seq = 1
                        )
                 select p.id, 
                        COALESCE(te.attr_value, ''), 
                        COALESCE(fa.attr_value, ''),
                        COALESCE(em.attr_value, ''),
                        COALESCE(it.attr_value, '')
                   from tmp_poi                  as p
              left join att       as te
                     on p.key = te.key  and  te.attr_type = 'TL'
              left join att       as fa
                     on p.key = fa.key  and  fa.attr_type = 'TX'
              left join att       as em
                     on p.key = em.key  and  em.attr_type = '8M'
              left join att       as it
                     on p.key = it.key  and  it.attr_type = '8L'
                  where te.attr_value is not null or
                        fa.attr_value is not null or
                        em.attr_value is not null or
                        it.attr_value is not null 
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _do_poi_geom(self):
        self.logger.info('  do poi geom')
        sqlcmd = '''
                 insert into tmp_poi_geom( id, lon, lat, entry_lon, entry_lat )
                 select p.id, st_x(g.geom)*100000, st_y(g.geom)*100000, 
                        case
                           when g2.geom is null then 0
                           else st_x(g2.geom)*100000
                        end, 
                        case
                           when g2.geom is null then 0
                           else st_y(g2.geom)*100000
                        end
                   from tmp_poi                  as p
                   join mid_feature_to_geometry  as fg
                     on p.key = fg.key and fg.code = 7000
                   join mid_geometry             as g
                     on fg.geomid = g.id
              left join mid_feature_to_geometry  as fg2
                     on p.key = fg2.key and fg2.code = 9920
              left join mid_geometry             as g2
                     on fg2.geomid = g2.id
                 '''
        self.db.do_big_insert(sqlcmd)
        
        
        