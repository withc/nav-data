import common.logger

class CMid_check(object):
    def __init__(self, database):
        self.db     = database
        self.name   = 'mid_check'
        self.logger = common.logger.sub_log( self.name )
    
    def run(self):
        self._check_name()
        self._check_place_point()
        
    def _check_name(self):
        sql = '''
              select * 
                from temp_feat_name
               where name = ''
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'temp_feat_name have empty name:' + str(rows) )
            
    def _check_place_point(self):
        sql = '''
              select * 
                from mid_place               as p
           left join mid_feature_to_geometry as g
                  on p.key = g.key and g.code = 7379
               where g.key is null
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'some place do not set center point:' + str(rows) )
        