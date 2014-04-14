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
        
    def gen_name_geom(self):
        self._domake_name_geom()
        pass
                
    def _domake_key(self):
        pass
        
    def _domake_feature(self):
        pass
    
    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_name_geom(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass
    
    def _domake_common_category(self):
        sqlcmd = '''
                 insert into mid_poi_category(per_code, gen1, gen2, gen3, level, imp, name, tr_name)
                 select per_code, gen1, gen2, gen3, level, imp, name, tr_name
                   from temp_org_category
                   order by level, case level 
                                      when 1 then  0
                                      when 2 then  gen1
                                      else   (gen1<<8) + gen2
                                    end,
                              name
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _gen_nameid( self, feat = None ):
        if not feat:
            return 0
        
        self.logger.info('generate %s name id' % feat) 
        sqlcmd = '''
                   insert into temp_<f>_name_gen_id( gid, nameid )
                   select gid, dense_rank() over ( order by tr_lang, tr_name, langcode, name ) 
                     from temp_<f>_name
                 '''  
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
        
        sqlcmd = '''
                   insert into mid_<f>_name( id, langcode, name, tr_lang, tr_name, ph_lang, ph_name )
                   select nameid, langcode, name, tr_lang, tr_name, ph_lang, ph_name
                     from (
                   select nameid, langcode, name, tr_lang, tr_name, ph_lang, ph_name,
                          row_number() over (partition by nameid order by ph_name desc ) as seq
                     from temp_<f>_name         as n
                     join temp_<f>_name_gen_id  as g
                       on n.gid = g.gid
                          ) as t
                    where seq = 1
                    order by nameid
                 ''' 
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
        
        sqlcmd = '''
                   insert into mid_<f>_to_name( key, type, nametype, nameid)
                   select distinct key, type, nametype, nameid
                     from temp_<f>_name         as n
                     join temp_<f>_name_gen_id  as g
                       on n.gid = g.gid
                    order by key
                 '''
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
    
    def _gen_geomid(self,feat = None):
        if not feat:
            return 0
        
        self.logger.info('generate %s geometry id'%feat)
        sqlcmd = '''
                   insert into temp_<f>_geom_gen_id( gid, geomid )
                   select gid, dense_rank() over (order by geotype, geom ) 
                     from temp_<f>_geom
                 '''
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
        
        # when geom is so close,the geomid will be same, so ,we need select only one geom in that case.
        sqlcmd = '''
                   insert into mid_<f>_geometry( id, type, geom)
                   select geomid, geotype, geom
                     from (
                           select geomid, geotype, geom, row_number() over ( partition by geomid ) as seq
                             from temp_<f>_geom         as e
                             join temp_<f>_geom_gen_id  as g
                               on e.gid = g.gid
                          ) as t
                     where seq = 1
                 '''
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
        
        sqlcmd = '''
                   insert into mid_<f>_to_geometry( key, type, code, geomid)
                   select key, type, code, geomid
                     from temp_<f>_geom         as e
                     join temp_<f>_geom_gen_id  as g
                       on e.gid = g.gid
                    order by key
                 '''
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
        
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
        self._create_index()

    def _create_index(self):
        self.logger.info('create index for mid table')
        self.db.createIndex('mid_poi_attr_value',      'key'    )
        self.db.createIndex('mid_feature_to_feature',  'fkey'   )
        self.db.createIndex('mid_feature_to_feature',  'tkey'   ) 
        
        self.db.createIndex('mid_street_name',        'name'   )
        self.db.createIndex('mid_street_to_name',     'key'    )
        self.db.createIndex('mid_street_to_name',     'nameid' )
        self.db.createIndex('mid_street_to_geometry', 'key'    )

        #self.db.createIndex('mid_poi_name',        'name' )
        self.db.createIndex('mid_poi_to_name',     'key'    )
        self.db.createIndex('mid_poi_to_name',     'nameid' )
        self.db.createIndex('mid_poi_to_geometry', 'key'    )

        
        
       
        

        
        
        