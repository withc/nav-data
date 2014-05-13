import common.logger
import base_check

class CStreet_check(base_check.CBase_check):
    def __init__(self, database):
        self.db     = database
        self.name   = 'street_check'
        self.logger = common.logger.sub_log( self.name )
    
    def _check_empty_name(self):
        sql = '''
              select *
                from mid_link            as p
                join mid_street_to_name  as n
                  on p.key = n.key
           left join mid_street_name     as na
                  on n.nameid = na.id
               where na.name = ''
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'link have empty name:' + str(rows) )
            
    def _check_nametype(self):
        sql = '''
              select key, type, nameid
                from mid_street_to_name
               group by key, type, nameid 
               having count(*) > 1 
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'link have same name, but different type:' + str(rows) )
        