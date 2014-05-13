import common.logger
import base_check

class CPOI_check(base_check.CBase_check):
    def __init__(self, database):
        self.db     = database
        self.name   = 'poi_check'
        self.logger = common.logger.sub_log( self.name )

    def _check_empty_name(self):
        sql = '''
              select *
                from mid_poi          as p
           left join mid_poi_to_name  as n
                  on p.key = n.key
           left join mid_poi_name     as na
                  on n.nameid = na.id
               where n.nameid is null or na.name = ''
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'poi have empty name:' + str(rows) )
            
    def _check_nametype(self):
        sql = '''
              select key, type, nameid
                from mid_poi_to_name
               group by key, type, nameid 
               having count(*) > 1 
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'poi have same name, but different type:' + str(rows) )
            
    def _check_ON_name(self):
        sql = '''
              select p.* 
                from mid_poi         as p
           left join mid_poi_to_name as n
                  on p.key = n.key and n.nametype = 'ON'
               where n.nameid is null 
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'poi don\'t have ON name:' + str(rows) )
        
        sql = '''
              select p.key, p.type 
                from mid_poi         as p
                join mid_poi_to_name as n
                  on p.key = n.key and n.nametype = 'ON'
               group by p.key, p.type having count(*) > 1
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'poi have more than 1 ON name:' + str(rows) )
    
    def _check_poi_point(self):
        sql = '''
              select p.key, p.type 
                from mid_poi                 as p
           left join mid_poi_to_geometry as g
                  on p.key = g.key and g.code = 7000
               where g.key is null
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'some poi do not set point:' + str(rows) )
            
        sql = '''
              select p.key, count(*)
                from mid_poi             as p
                join mid_poi_to_geometry as g
                  on p.key = g.key and g.code = 9920
               group by p.key having count(*) > 1
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'some poi have more than one entry point:' + str(rows) )
            
    def _check_duplicate_poi(self):
        pass 
    
    