import common.logger

class CFeature(object):

    def __init__(self, name='feature'):
        self.db     = None
        self.name   = name
        self.logger = common.logger.sub_log( self.name )
        self.logger.info('init')
        
    def attach_db(self, database):
        self.db = database
         
    def make_key(self):
        self.logger.info('make key')
        self._domake_key()
        
    def make_feature(self):
        self.logger.info('make feature')
        self._domake_feature()
    
    def make_geomtry(self):
        self.logger.info('make geomtry')
        self._domake_geomtry()
        
    def make_name(self):
        self.logger.info('make name')
        self._domake_name()
    
    def make_attribute(self):
        self.logger.info('make attribute')
        self._domake_attribute()
        
    def make_relation(self):
        self.logger.info('make relation')
        self._domake_relation()
        
    def _domake_key(self):
        pass
        
    def _domake_feature(self):
        pass
    
    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass
        
class CStartProcess(object):
    
    def __init__(self):
        self.logger = common.logger.sub_log( 'start_pro' )
    def attach_db(self, database,vendor):
        self.db   = database
        self.name = vendor
    def do(self):
        self.logger.info('create mid table and function') 
        self.db.run( r'.\config\mid_db.sql' )
        self.db.run( r'.\load\%s\my.sql' % self.name )

class CEndProcess(object):
    
    def __init__(self):
        self.logger = common.logger.sub_log( 'end_pro' )
        
    def attach_db(self, database, vendor):
        self.db = database
        self.name = vendor
    def do(self):
        self._gen_nameid()
        self._gen_geomid()
        self._create_index()
        
    def _gen_nameid(self):
        self.logger.info('generate name id') 
        sqlcmd = '''
                   insert into temp_feat_name_gen_id( key, type, nametype, langcode, name, nameid )
                   select *, dense_rank() over (order by name, langcode ) 
                     from temp_feat_name
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                   insert into mid_name( id, langcode, name)
                   select distinct nameid, langcode, name
                     from temp_feat_name_gen_id
                     order by nameid
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                   insert into mid_feature_to_name( key, type, nametype, nameid)
                   select distinct key, type, nametype, nameid
                     from temp_feat_name_gen_id
                     order by key
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _gen_geomid(self):
        self.logger.info('generate geometry id')
        sqlcmd = '''
                   insert into temp_feat_geom_gen_id( key, type, code, geotype, geom, geomid )
                   select *, dense_rank() over (order by geotype, geom ) 
                     from temp_feat_geom
                 '''
        self.db.do_big_insert( sqlcmd )
        
        # when geom is so close,the geomid will be same, so ,we need select only one geom in that case.
        sqlcmd = '''
                   insert into mid_geometry( id, type, geom)
                   select geomid, geotype, geom
                     from (
                           select geomid, geotype, geom, row_number() over ( partition by geomid ) as seq
                             from temp_feat_geom_gen_id
                          ) as t
                     where seq = 1
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                   insert into mid_feature_to_geometry( key, type, code, geomid)
                   select  key, type, code, geomid
                     from temp_feat_geom_gen_id
                     order by key
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _create_index(self):
        self.logger.info('create index for mid table')
        self.db.createIndex('mid_poi_attr_value',      'key'    )
        self.db.createIndex('mid_feature_to_feature',  'fkey'   )
        self.db.createIndex('mid_feature_to_feature',  'tkey'   ) 
        self.db.createIndex('mid_feature_to_name',     'key'    )
        self.db.createIndex('mid_feature_to_name',     'nameid' )
        self.db.createIndex('mid_feature_to_geometry', 'key'    )
        self.db.createIndex('mid_feature_to_geometry', 'geomid' )
        self.db.createIndex('mid_name', 'name' )
        
       
        

        
        
        