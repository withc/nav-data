import common.logger

class CMid_check(object):
    def __init__(self, database):
        self.db     = database
        self.name   = 'mid_check'
        self.logger = common.logger.sub_log( self.name )
    
    def run(self):
        self._check_name()
        
    def _check_name(self):
        sql = '''
              select * 
                from temp_feat_name
               where name = ''
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'temp_feat_name have empty name:' + str(rows) )
        