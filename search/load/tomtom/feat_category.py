import load.feature

class CPoiCategory(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'category')
 
    def _domake_key(self):
        fp = open(r'.\load\tomtom\category.txt','r')
        for line in fp:
            line = line.strip()
            if line[0] == '#':
                continue
            fields = line.split(';')
            sqlcmd = '''
                      insert into temp_org_category values(%s,%s,%s,%s,%s,%s,%s,%s)
                     '''
            self.db.execute( sqlcmd, fields )
        self.db.commit()
        self.db.analyze('temp_org_category')
        fp.close()
        
    def _domake_feature(self):
        self._domake_common_category()
    
    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass