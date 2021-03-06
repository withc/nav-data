import entity

class CPlace(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'place')
          
    def _do(self):
        self._do_meta()
        self._do_lowest_place()
        self._do_gen_areaid()
        self._do_name()
        self._do_table()
        
    def _do_meta(self):
        sqlcmd = '''
                 insert into tbl_search_meta( base_lon, base_lat, min_lon, min_lat, max_lon, max_lat )
                 select srch_base_coord(min_lon), srch_base_coord(min_lat), 
                        srch_coord(min_lon),      srch_coord(min_lat), 
                        srch_coord(max_lon),      srch_coord(max_lat)
                   from mid_full_area
                 '''
        self.db.do_big_insert(sqlcmd)
            
    def _do_table(self):
        self.logger.info('  do place infor')
        sqlcmd = '''
                 insert into tbl_city_info( level, area0, area1, area2, area3, lon, lat )
                 select p.level, p.area0, p.area1, p.area2, p.area3, 
                        srch_coord((st_x(g.geom)*100000)::int), srch_coord((st_y(g.geom)*100000)::int)
                   from tmp_place_area           as p
                   join mid_street_to_geometry  as fg
                     on p.key = fg.key and fg.code = 7379
                   join mid_street_geometry             as g
                     on fg.geomid = g.id
                  order by p.level, p.area0, p.area1, p.area2, p.area3
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _do_name(self):
        self.logger.info('  do place name')
        
        sqlcmd = '''
                 insert into tmp_place_name( key, type, nametype, lang, name, tr_lang, tr_name, ph_lang, ph_name )
                 select p.key, p.type, pn.nametype, n.langcode, n.name, n.tr_lang, n.tr_name, n.ph_lang, n.ph_name
                   from mid_place_admin      as p
                   join mid_street_to_name  as pn
                     on p.key = pn.key and p.type = pn.type
                   join mid_street_name             as n
                     on pn.nameid = n.id 
                 ''' 
        self.db.do_big_insert(sqlcmd)
        self.db.createIndex( 'tmp_place_name', 'key' )
        
        sqlcmd = '''
                 insert into tbl_city_name( level, area0, area1, area2, area3, type, lang, name, tr_lang, tr_name, ph_lang, ph_name )
                 select p.level, p.area0, p.area1, p.area2, p.area3, pn.nametype, 
                        pn.lang, pn.name, pn.tr_lang, pn.tr_name, pn.ph_lang, pn.ph_name
                   from tmp_place_area    as p
                   join tmp_place_name    as pn
                     on p.key = pn.key
                  order by p.level, p.area0, p.area1, p.area2, p.area3 
                 '''
        self.db.do_big_insert(sqlcmd)
        
#         sqlcmd = '''
#                  insert into tbl_place_full( key, type, lang, country, state, city, district )
#                  select a.key, a.type, n0.lang, n0.name, n1.name, n8.name, 
#                         COALESCE( n9.name, '' )
#                    from mid_place_admin  as a
#                    join tmp_place_name   as n0
#                      on a.a0 = n0.key
#                    join tmp_place_name   as n1
#                      on a.a1 = n1.key and n0.lang = n1.lang
#                    join tmp_place_name   as n8
#                      on a.a8 = n8.key and n0.lang = n8.lang
#               left join tmp_place_name   as n9
#                      on a.a9 = n9.key and n0.lang = n9.lang
#                    where a.a8 <> 0 or a.a9 <> 0
#                  '''
        #self.db.do_big_insert(sqlcmd)
        #self.db.createIndex( 'tbl_place_full', 'key' )
    
    def _do_gen_areaid(self):
        #for a0
        sqlcmd = '''
                 insert into tmp_place_area( key, type, level, area0, area1, area2, area3)
                 select key, type, 0, row_number() over (), 0,0,0
                   from mid_place_admin
                  where type = 3001
                 '''
        self.db.do_big_insert(sqlcmd)
        #for a1
        sqlcmd = '''
                 insert into tmp_place_area( key, type, level, area0, area1, area2, area3)
                 select pa.key, pa.type, 1, t.area0, 
                        row_number() over ( partition by t.area0 order by pa.key ), 0,0
                   from mid_place_admin  as pa
                   join tmp_place_area   as t
                     on pa.a0 = t.key and pa.type = 3002
                 '''
        self.db.do_big_insert(sqlcmd)
        
        sqlcmd = 'select count(*) from mid_place where type = 3010'
        count = self.db.getResultCount(sqlcmd)
        if  count > 1 :
            self._add_a8_a9()
        else:
            self._add_a7_a8()
            
        self.db.createIndex( 'tmp_place_area', 'key' )
        
    def _add_a7_a8(self):
        #in some country, there is no a9, so, we will set a8 to area3.
        #for a7
        sqlcmd = '''
                 insert into tmp_place_area( key, type, level, area0, area1, area2, area3)
                 select pa.key, pa.type, 2, t.area0, t.area1, 
                        row_number() over ( partition by t.area0, t.area1 order by pa.key ), 0
                   from mid_place_admin  as pa
                   join tmp_place_area   as t
                     on pa.a1 = t.key and pa.type = 3008
                 '''
        self.db.do_big_insert(sqlcmd)
        #for a8
        sqlcmd = '''
                 insert into tmp_place_area( key, type, level, area0, area1, area2, area3)
                 select pa.key, pa.type, 3, t.area0, t.area1, t.area2,
                        row_number() over ( partition by t.area0, t.area1 order by pa.key )
                   from mid_place_admin  as pa
                   join tmp_place_area   as t
                     on pa.a7 = t.key and pa.type = 3009
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _add_a8_a9(self):
        #for a8
        sqlcmd = '''
                 insert into tmp_place_area( key, type, level, area0, area1, area2, area3)
                 select pa.key, pa.type, 2, t.area0, t.area1, 
                        row_number() over ( partition by t.area0, t.area1 order by pa.key ), 0
                   from mid_place_admin  as pa
                   join tmp_place_area   as t
                     on pa.a1 = t.key and pa.type = 3009
                 '''
        self.db.do_big_insert(sqlcmd)
        
        #for a9, discard the a9 that have no center point.
        sqlcmd = '''
                 insert into tmp_place_area( key, type, level, area0, area1, area2, area3)
                 select pa.key, pa.type, 3, t.area0, t.area1, t.area2,
                        row_number() over (partition by t.area0, t.area1,t.area2 order by pa.key )
                   from mid_place_admin  as pa
                   join tmp_place_area   as t
                     on pa.a8 = t.key and pa.type = 3010
                   where exists (
                       select 1 
                         from mid_street_to_geometry  as fg
                        where pa.key = fg.key and fg.code = 7379
                   )
                 '''
        self.db.do_big_insert(sqlcmd)
        
        
    def _do_lowest_place(self):
        ''' when a feature belong to a9, we also add a8( the a9's parent) to table mid_feature_to_feature,
            so, we must filter the a8 record if it is already refer to his a9.
            tmp_feat_lowest_place will contain the lowest admin place only.
        '''
        self.logger.info('  do feat to lowest place')
        sqlcmd = '''
               insert into tmp_feat_lowest_place( key, type, pkey, ptype )
               select fkey, ftype, tkey, ttype 
                from (
                 select ff.fkey, ff.ftype, ff.tkey, ff.ttype, p.a8, 
                        dense_rank() over ( partition by ff.fkey, p.a8 order by ff.ttype desc ) as seq
                   from mid_feature_to_feature  as ff
                   join mid_place_admin         as p
                     on ff.tkey  = p.key  and 
                        ff.code  = 7001   and 
                        ff.ttype in ( 3009, 3010 )
                      ) as t 
                  where seq = 1
                 '''
        self.db.do_big_insert(sqlcmd)
        self.db.createIndex( 'tmp_feat_lowest_place', 'key' )
        
        
        
        
        
        
        
        