import common.logger

class CEntity(object):
    def __init__(self, name='entity'):
        self.db     = None
        self.name   = name
        self.logger = common.logger.sub_log( self.name )
        
    def attach_db(self, database):
        self.db = database
        
    def copy(self):
        self.logger.info('copy entity')
        self._do()
        