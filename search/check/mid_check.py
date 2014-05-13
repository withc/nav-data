import common.logger
import place_check
import poi_check
import street_check

class CMid_check(object):
    def __init__(self, database):
        self.db     = database
        self.name   = 'mid_check'
        self.logger = common.logger.sub_log( self.name )
        self.objs   = []
        
    def run(self):
        self._add_module()
        self._run_module()
        
    def _add_module(self):
        self.objs.append(place_check.CPlace_check(self.db))
        self.objs.append(poi_check.CPOI_check(self.db))
        self.objs.append(street_check.CStreet_check(self.db))
        
    def _run_module(self):
        self.logger.info('-- start check work')
        for o in self.objs:
            o.do_check()
        self.logger.info('-- end check work')
                
    
                  
    

        