
class CBase_check(object):
    def __init__(self):
        pass
    
    def callback(self, name ):
        method = getattr(self, name, None)
        if callable(method):
            return method()
        
    def do_check(self):
        for fun in self.__class__.__dict__:
            if '_check_'== fun[0:7]:
                self.callback(fun)
                
    def _log_one_result(self, sql, infor ):
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( infor + str(rows) )