import common.logger
import house_number
import place
import street

class CCompiler(object):
    def __init__(self, database):
        self.db     = database
        self.name   = 'compiler'
        self.logger = common.logger.sub_log( self.name )
        self.entity = []
    
    def run(self):
        self._prepare()
        self._addEntity()
        for en in self.entity:
            en.copy()
            
    def _prepare(self):
        self.logger.info('create rdb table and function') 
        fp = open(r'.\config\rdb_db.sql','r')
        self.db.execute( fp.read() )
        fp.close()
        
    def _addEntity(self):
        self.entity.append( place.CPlace(self.db) )
        self.entity.append( street.CLink(self.db) )
        self.entity.append( house_number.CHouseNumber(self.db) )
        