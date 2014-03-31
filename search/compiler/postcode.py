import entity

class CPostcode(entity.CEntity):
    def __init__(self, database):
        entity.CEntity.__init__(self, database, 'postcode')
          
    def _do(self):
        sqlcmd = '''
                 insert into tbl_postcode_info( area0, id, pocode, lon, lat )
                 select 1, row_number() over( order by p.key ), p.pocode, 
                        case 
                          when fg.geomid is null then null
                          else srch_coord((st_x(g.geom)*100000)::int)
                        end,
                        case
                          when fg.geomid is null then null
                          else srch_coord((st_y(g.geom)*100000)::int)
                        end
                   from mid_postcode             as p
              left join mid_feature_to_geometry  as fg
                     on p.key = fg.key and fg.code = 7379
              left join mid_geometry             as g
                     on fg.geomid = g.id
                 '''
        self.db.do_big_insert(sqlcmd)