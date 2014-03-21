import common.logger

class CEntity(object):
    def __init__(self, database, name='entity'):
        self.db     = database
        self.name   = name
        self.logger = common.logger.sub_log( self.name )
         
    def copy(self):
        self.logger.info('copy entity')
        self._do()
        