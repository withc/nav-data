import common.logger
import house_number
import place
import link
import road

class CCompiler(object):
    def __init__(self, database):
        self.db     = database
        self.name   = 'compiler'
        self.logger = common.logger.sub_log( self.name )
        self.entity = []
    
    def run(self):
        self.logger.info('------------ start -------------')
        self._prepare()
        self._addEntity()
        for en in self.entity:
            en.copy()
        self.logger.info('------------ end -------------')
            
    def _prepare(self):
        self.logger.info('create dest table and function') 
        self.db.run( r'.\config\des_db.sql' )
        self.db.run( r'.\config\rdb_function.sql' )

    def _addEntity(self):
        self.entity.append( place.CPlace(self.db) )
        #self.entity.append( link.CLink(self.db) )
        #self.entity.append( house_number.CHouseNumber(self.db) )
        