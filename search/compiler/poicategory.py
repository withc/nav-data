import entity

class CPoicategory(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'Poi_cat')
          
    def _do(self):
        sqlcmd = '''
                 insert into tbl_genre_info( u_code, gen1, gen2, gen3, level, imp, name)
                 select * 
                   from mid_poi_category
                 '''
        self.db.do_big_insert(sqlcmd)