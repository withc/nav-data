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
        
    def input(self, path):
        self.logger.info('begin load table %s' % self.name )
        self._do_all( path )
        self.logger.info('end load table %s' % self.name )
        pass
    
    def _do_all(self, path):
        pass
    
    def _get_file(self, path):
        pass

    