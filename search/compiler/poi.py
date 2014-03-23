import entity

class CPoi(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'poi')
          
    def _do(self):
        pass
    
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