import common.logger
import base_check

class CTbl_check( base_check.CBase_check ):
    def __init__(self, database):
        self.db     = database
        self.name   = 'tbl_check'
        self.logger = common.logger.sub_log( self.name )
        self.objs   = []
        
    def run(self):
        self.do_check()

    def _check_place(self):
        pass
    
    def _check_street(self):
        pass
    
    def _check_poi(self):
        pass
        
    