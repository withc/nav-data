import common.logger

class CTable(object):
    
    def __init__(self, name='table'):
        self.db     = None
        self.name   = name
        self.logger = common.logger.sub_log( self.name )
        self.logger.info('init')
   
    def attach_db(self, database, vendor=''):
        self.db = database
        self.vendor = vendor
        
    def input(self):
        self._do_all()
        pass
    
    def _do_all(self):
        pass