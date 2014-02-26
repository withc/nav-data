import common.database
import common.logger
import load.factory

class CLoader(object):
    def __init__(self):
        self.logger = common.logger.sub_log('load')
        self.vendor  = ''
        self.dbInfor = {}
        self.db = None
        self.proces = []
        self.feats  = []
        
    def load(self, path ):
        self._readConfig(path)
        self.db = common.database.CDB( "default", self._getDBPath() )
        self.db.connect()
        
        self._make_feature_proce()
        self.logger.info( " ----------- start -------------" )
        self._prepare()
        self._process()
        self._finish()
        self.logger.info( " ------------ end  --------------" )
        
        self.db.close()
    
    def add_process(self, proce):
        proce.attach_db( self.db )
        self.proces.append( proce )
        
    def add_feature(self, feat):
        feat.attach_db( self.db )
        self.feats.append( feat )
            
    def _readConfig(self,path):
        fp = open(path,'r')
        self.dbInfor['host'] = 'localhost'
        self.dbInfor['dbname'] = 'mydb'
        self.dbInfor['user'] = 'postgres'
        self.dbInfor['password'] = ''
        
        self.vendor = 'tomtom'
        fp.close()
        
    def _getDBPath(self):
        return 'host=%s dbname=%s user=%s password=%s' % (self.dbInfor['host'],self.dbInfor['dbname'],self.dbInfor['user'],self.dbInfor['password'])
    
    def _prepare(self):
        self.proces[0].do()
     
    def _process(self):
        self._copy_feature_key()
        self._copy_feature()
        self._copy_common_attribute()
        self._copy_attribute()
        self._copy_relationship()
        
    def _finish(self):
        self.proces[1].do()
        pass

    def _make_feature_proce(self):
        load.factory.featureFactory( self.vendor, self )
     
    def _copy_feature_key(self):
        print 'copy_feature_key'
        for f in self.feats:
            f.make_key()
        
    def _copy_feature(self):
        print 'copy_feature'
        for f in self.feats:
            f.make_feature()
        
    def _copy_common_attribute(self):
        print 'copy_geomtry'
        for f in self.feats:
            f.make_geomtry()
            f.make_name()
    
    def _copy_attribute(self):
        print 'copy_attribute'
        for f in self.feats:
            f.make_attribute()
        
    def _copy_relationship(self):
        print 'copy_relationship'
        for f in self.feats:
            f.make_relation()
            
   
        
        
    