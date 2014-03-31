import common.logger
import house_number
import place
import street
import poi
import poicategory
import postcode
import voice_data

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
        self.logger.info('create rdb table and function') 
        self.db.run( r'.\config\tbl_db.sql' )
        self.db.run( r'.\config\rdb_function.sql' )

    def _addEntity(self):
        self.entity.append( place.CPlace(self.db) )
        self.entity.append( poicategory.CPoicategory(self.db) )
        self.entity.append( poi.CPoi(self.db) )
        self.entity.append( street.CLink(self.db) )
        self.entity.append( house_number.CHouseNumber(self.db) )
        self.entity.append( voice_data.CVoiceData(self.db) )
        