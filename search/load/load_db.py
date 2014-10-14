
import common.logger
import load.factory

class CLoader(object):
    def __init__(self, database, vendor ):
        self.logger = common.logger.sub_log('load')
        self.vendor = vendor
        self.db = database
        self.tables  = []

    def run(self ):
        self.logger.info( " ----------- start -------------" )
        self._make_table()
        self._prepare()
        self._process()
        self._finish()
        self.logger.info( " ------------ end  --------------" )
           
    def add_table(self, table):
        table.attach_db( self.db, self.vendor )
        self.tables.append( table )
        
    def _make_table(self):
        load.factory.tableFactory( self.vendor, self )
        
    def _prepare(self):
        pass
    
    def _process(self):
        for t in self.tables:
            t.input()
            
    def _finish(self):
        pass