import entity

class CLink(entity.CEntity):
    def __init__(self, database):
        entity.CEntity.__init__(self, database, 'link')
          
    def _do(self):
        self._do_gen_id()
        self._do_street_geom()
        self._do_street_infor()
        self._do_street_name()
        
    def _do_gen_id(self):
        self.logger.info('  do gen id')
        sqlcmd = '''
            insert into tmp_street( key, type, pkey, ptype, nameid, id )
            select key, type, pkey,  ptype, nameid, dense_rank() over ( order by  pkey, ptype, nameid )
              from (
                        select fp.pkey, fp.ptype, l.key, l.type, n.nameid 
                          from mid_link              as l
                          join tmp_feat_lowest_place as fp
                            on l.key = fp.key
                          join mid_street_to_name   as n
                            on l.key = n.key
                    ) as t
              order by pkey, nameid
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _do_street_name(self):
        self.logger.info('  do name')
        sqlcmd = '''
                 insert into tbl_street_name( id, type, lang, name, tr_lang, tr_name )
                 select distinct s.id, fn.nametype, n.langcode, n.name, n.tr_lang, n.tr_name
                   from tmp_street           as s
                   join mid_street_to_name  as fn
                     on s.key = fn.key and s.nameid = fn.nameid
                   join mid_street_name             as n
                     on fn.nameid = n.id
                  order by s.id
                 '''
        self.db.do_big_insert(sqlcmd)
    
    def _do_street_geom(self):
        self.logger.info('  do geom')
        sqlcmd = '''
                 insert into tmp_street_geom( id, geom )
                 select t.id, ST_ClosestPoint( geom, ST_Centroid(geom) )
                   from (
                        select s.id, ST_Union(g.geom) as geom
                          from tmp_street             as s
                          join mid_street_to_geometry as fg
                            on s.key = fg.key
                          join mid_street_geometry    as g
                            on fg.geomid = g.id
                         group by s.id
                        ) as t
                 '''
        self.db.do_big_insert(sqlcmd) 
        
    def _do_street_infor(self):
        self.logger.info('  do street infor')
        sqlcmd = '''
                 insert into tbl_street_info( id, level, area0, area1, area2, area3, lon, lat )
                 select distinct s.id, p.level, p.area0, p.area1, p.area2, p.area3, 
                        srch_coord((st_x(g.geom)*100000)::int), srch_coord((st_y(g.geom)*100000)::int)
                   from tmp_street        as s
                   join tmp_place_area    as p
                     on s.pkey = p.key
                   join tmp_street_geom   as g
                     on s.id = g.id
                  order by s.id
                 '''
        self.db.do_big_insert(sqlcmd)
        