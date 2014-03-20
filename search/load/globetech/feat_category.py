import load.feature

class CPoiCategory(load.feature.CFeature):
    def __init__(self ):
        print "globe tech's poi category"
        load.feature.CFeature.__init__(self, 'category')
 
    def _domake_key(self):
        fp = open(r'.\load\globetech\category.txt','r')
        for line in fp:
            line = line.strip()
            if line[0] == '#':
                continue
            fields = line.split(';')
            sqlcmd = '''
                      insert into temp_org_category values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                     '''
            self.db.execute( sqlcmd, fields )
        fp.close()
        
    def _domake_feature(self):
        sqlcmd = '''
                 insert into mid_poi_category(per_code, gen1, gen2, gen3, level, imp, name)
                 select per_code, gen1, gen2, gen3, level, imp, name
                   from temp_org_category
                   order by level, case level 
                                      when 1 then  0
                                      when 2 then  gen1
                                      else    gen1<<8 + gen2
                                    end,
                              name
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