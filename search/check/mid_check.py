import common.logger

class CMid_check(object):
    def __init__(self, database):
        self.db     = database
        self.name   = 'mid_check'
        self.logger = common.logger.sub_log( self.name )
    
    def run(self):
        self._check_name()
        self._check_place_point()
        self._check_poi_point()
        
    def _check_name(self):
        sql = '''
              select * 
                from temp_street_name
               where name = ''
             union all
               select * 
                from temp_poi_name
               where name = ''
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'temp_feat_name have empty name:' + str(rows) )
            
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
                         when p.type = 3010 then 4
                         when p.type = 3008 then 5
                         else 6
                        end
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'some place do not set center point:' + str(rows) )
            
        sql = '''
              select p.key, p.type, count(*)
                from mid_place               as p
                join mid_street_to_geometry as g
                  on p.key = g.key and g.code = 7379
               group by p.key, p.type having count(*) > 1
              '''
        rows = self.db.getOneResult(sql )
        if 0 != rows:
            self.logger.info( 'some place have more than one center point:' + str(rows) )
            
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

        