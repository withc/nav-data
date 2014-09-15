import load.feature

class CStartProcess(load.feature.CWork):
    
    def __init__(self):
        load.feature.CWork.__init__(self,  'start_pro' )
        
    def do(self):
        self.logger.info('create mid table and function') 
        self.db.run( r'.\config\mid_db.sql' )
        self.db.run( r'.\config\rdb_function.sql' )
        self.db.run( r'.\load\%s\my.sql' % self.name )
        self._add_abbr()
        
        self.logger.info('do some start self work') 
        self._do_my()
        
    def _add_abbr(self):
        try:
            fp = open(r'.\load\%s\abbr.txt' % self.name,'r')
        except:
            return
        
        for line in fp:
            line = line.strip()
            if not line or line[0] == '#':
                continue
            fields = line.split(';')
            sqlcmd = '''
                      insert into mid_abbr_word values(%s,%s,%s,%s)
                     '''
            self.db.execute( sqlcmd, fields )
        self.db.commit()
        self.db.analyze('mid_abbr_word')
        fp.close()    
    def _do_my(self):
        pass

class CEndProcess(load.feature.CWork):
    
    def __init__(self):
        load.feature.CWork.__init__(self, 'end_pro' )
        
    def do(self):
        self._build_postcode_city_by_poi()
        self._create_index()

    def _build_postcode_city_by_poi(self):
        #add relationship between postcode and city.
        #we can build it according poi infor
        #if a poi belong to a place and a postcode, we think the postcode refer to the place
        self.logger.info('build relationship ( postcode X city ) from poi')
        sqlcmd = '''
                 insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                 select distinct po.tkey, po.ttype, 7001, pl.tkey, pl.ttype
                   from mid_feature_to_feature as po
                   join mid_feature_to_feature as pl
                     on po.ftype = 1000    and
                        po.code  = 7004    and
                        po.fkey  = pl.fkey and
                        pl.code  = 7001
                  where not exists (
                        select 1 
                          from mid_feature_to_feature as pp
                         where pp.fkey = po.tkey and 
                               pp.tkey = pl.tkey and 
                               pp.code = 7001
                        )
                  order by po.tkey
                 '''
        self.db.do_big_insert( sqlcmd )

    def _create_index(self):
        self.logger.info('create index for mid table')
        self.db.createIndex('mid_poi_attr_value',      'key'    )
        self.db.createIndex('mid_feature_to_feature', ['fkey','code']   )
        self.db.createIndex('mid_feature_to_feature',  'tkey'   ) 
        
        #self.db.createIndex('mid_place_name',        'name'   )
        self.db.createIndex('mid_place_to_name',     'key'    )
        self.db.createIndex('mid_place_to_name',     'nameid' )
        self.db.createIndex('mid_place_to_geometry', 'key'    )
        
        #self.db.createIndex('mid_street_name',        'name'   )
        self.db.createIndex('mid_street_to_name',     'key'    )
        self.db.createIndex('mid_street_to_name',     'nameid' )
        self.db.createIndex('mid_street_to_geometry', 'key'    )

        #self.db.createIndex('mid_poi_name',        'name' )
        self.db.createIndex('mid_poi_to_name',     'key'    )
        self.db.createIndex('mid_poi_to_name',     'nameid' )
        self.db.createIndex('mid_poi_to_geometry', 'key'    )
