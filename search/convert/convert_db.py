
import common.logger
import convert.factory

class CConverter(object):
    def __init__(self, database, vendor ):
        self.logger = common.logger.sub_log('convert')
        self.vendor = vendor
        self.db = database
        self.proces = []
        self.feats  = []
        self.part3  = []
        
    def run(self ):
        self._make_feature_proce()
        self.logger.info( " ----------- start -------------" )
        self._prepare()
        self._process()
        self._finish()
        self.logger.info( " ------------ end  --------------" )
        
    def add_process(self, proce):
        proce.attach_db( self.db, self.vendor )
        self.proces.append( proce )
        
    def add_feature(self, feat):
        feat.attach_db( self.db )
        self.feats.append( feat )
        
    def add_part3(self, feat ):
        feat.attach_db( self.db, self.vendor )
        self.part3.append( feat )
               
    def _prepare(self):
        self.proces[0].do()
     
    def _process(self):
        self._copy_feature_key()
        self._copy_feature()
        self._copy_common_attribute()
        self._copy_attribute()
        self._copy_relationship()
        #other data
        self._pro_part3()
        
    def _pro_part3(self):
        for p in self.part3:
            p.run()
        
    def _finish(self):
        self.proces[1].do()
        pass

    def _make_feature_proce(self):
        convert.factory.featureFactory( self.vendor, self )
     
    def _copy_feature_key(self):
        self.logger.info( '--copy_feature_key' )
        for f in self.feats:
            f.make_key()
        
    def _copy_feature(self):
        self.logger.info( '--copy_feature' )
        for f in self.feats:
            f.make_feature()
        
    def _copy_common_attribute(self):
        self.logger.info( '--copy_name_geomtry' )
        for f in self.feats:
            f.make_geomtry()
            f.make_name()
            f.gen_name_geom()
    
    def _copy_attribute(self):
        self.logger.info( '--copy_attribute' )
        for f in self.feats:
            f.make_attribute()
        
    def _copy_relationship(self):
        self.logger.info( '--copy_relationship' )
        for f in self.feats:
            f.make_relation()
            
   
        
        
    