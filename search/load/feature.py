
class CFeature(object):

    def __init__(self):
        self.db   = None
        self.name = ''
        
    def attach_db(self, database):
        self.db = database
         
    def make_key(self):
        print ''
        
    def make_feature(self):
        print ''
    
    def make_geomtry(self):
        print ''
        
    def make_name(self):
        print ''
    
    def make_attribute(self):
        print ''
        
    def make_relation(self):
        print ''
        
class CStartProcess(object):
    
    def __init__(self):
        print ''
    def attach_db(self, database):
        self.db = database
    def do(self):
        fp = open(r'.\config\mid_db.sql','r')
        self.db.execute( fp.read() )
        fp.close()

class CEndProcess(object):
    
    def __init__(self):
        print ''
    def attach_db(self, database):
        self.db = database
    def do(self):
        self._gen_nameid()
        self._gen_geomid()
        
    def _gen_nameid(self):
        print 'generate name id'
        sqlcmd = '''
                   insert into temp_feat_name_gen_id( key, type, nametype, langcode, name, nameid )
                   select *, dense_rank() over (order by name, langcode ) 
                     from temp_feat_name
                 '''
        self.db.execute( sqlcmd )
        
        sqlcmd = '''
                   insert into mid_name( id, langcode, name)
                   select distinct nameid, langcode, name
                     from temp_feat_name_gen_id
                     order by nameid
                 '''
        self.db.execute( sqlcmd )
        
        sqlcmd = '''
                   insert into mid_feature_to_name( key, type, nametype, nameid)
                   select  key, type, nametype, nameid
                     from temp_feat_name_gen_id
                     order by key
                 '''
        self.db.execute( sqlcmd )
    
    def _gen_geomid(self):
        print 'generate geometry id'
        sqlcmd = '''
                   insert into temp_feat_geom_gen_id( key, type, code, geotype, geom, geomid )
                   select *, dense_rank() over (order by geotype, geom ) 
                     from temp_feat_geom
                 '''
        self.db.execute( sqlcmd )
        sqlcmd = '''
                   insert into mid_geometry( id, type, geom)
                   select distinct geomid, geotype, geom
                     from temp_feat_geom_gen_id
                     order by geomid
                 '''
        self.db.execute( sqlcmd )
        
        sqlcmd = '''
                   insert into mid_feature_to_geometry( key, type, code, geomid)
                   select  key, type, code, geomid
                     from temp_feat_geom_gen_id
                     order by key
                 '''
        self.db.execute( sqlcmd )
        
        
        
        
        
        