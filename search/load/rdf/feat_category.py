import load.feature

class CPoiCategory(load.feature.CFeature):
    def __init__(self ):
        print "rdf's poi category"
        load.feature.CFeature.__init__(self, 'category')
 
    def _domake_key(self):
        fp = open(r'.\load\rdf\category.txt','r')
        for line in fp:
            line = line.strip()
            if line[0] == '#':
                continue
            fields = line.split(';')
            sqlcmd = '''
                      insert into temp_org_category values(%s,%s,%s)
                     '''
            self.db.execute( sqlcmd, fields )
        fp.close()
        sqlcmd = ''' 
                 insert into temp_poi_category( level, org_code, name, imp )
                 select 1, org_code, name, imp
                   from temp_org_category
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = ''' 
                 insert into mid_poi_category( id, parent_id, level, imp, name )
                 select c.id, 0, c.level, c.imp, c.name
                   from temp_poi_category as c
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass