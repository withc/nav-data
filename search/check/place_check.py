import common.logger
import base_check

class CPlace_check(base_check.CBase_check):
    def __init__(self, database):
        self.db     = database
        self.name   = 'place_check'
        self.logger = common.logger.sub_log( self.name )
    
    def _check_prime_key(self):
        sql = '''
                select fkey, ftype, code, tkey, ttype
                  from mid_feature_to_feature
                  group by fkey, ftype, code, tkey, ttype
                  having count(*) > 1
               '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'mid_feature_to_feature have duplicate record:' + str(rows) )
            
    def _check_empty_name(self):
        sql = '''
              select *
                from mid_place           as p
           left join mid_street_to_name  as n
                  on p.key = n.key
           left join mid_street_name     as na
                  on n.nameid = na.id
               where n.nameid is null or na.name = ''
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'place have empty name:' + str(rows) )
            
    def _check_ON_name(self):
        sql = '''
              select p.* 
                from mid_place           as p
           left join mid_street_to_name  as n
                  on p.key = n.key and n.nametype = 'ON'
               where n.nameid is null 
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'place don\'t have ON name:' + str(rows) )
        
        sql = '''
              select p.key, p.type 
                from mid_place           as p
                join mid_street_to_name  as n
                  on p.key = n.key and n.nametype = 'ON'
                group by p.key, p.type having count(*) > 1
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'place have more than 1 ON name:' + str(rows) )
            
    def _check_place_point(self):
        sql = '''
              select p.key, p.type 
                from mid_place               as p
           left join mid_street_to_geometry as g
                  on p.key = g.key and g.code = 7379
               where g.key is null 
               order by case 
                         when p.type = 3009 then 1
                         when p.type = 3002 then 2
                         when p.type = 3001 then 3
                         when p.type = 3003 then 4
                         when p.type = 3008 then 5
                         when p.type = 3010 then 6
                         else 7
                        end
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'some place do not set center point:' + str(rows) )
    
    def _check_place_more_point(self):
 
        sql = '''
              select p.key, p.type, count(*)
                from mid_place               as p
                join mid_street_to_geometry as g
                  on p.key = g.key and g.code = 7379
               group by p.key, p.type having count(*) > 1
              '''
        rows = self.db.getOneResult( sql )
        if 0 != rows:
            self.logger.info( 'some place have more than one center point:' + str(rows) )
            