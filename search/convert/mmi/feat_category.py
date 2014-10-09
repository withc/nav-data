import convert.feature

class CPoiCategory(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'category')
 
    def _domake_key(self):
        # for mmi, the org_code is character.
        sqlcmd = '''
                    DROP TABLE IF EXISTS temp_org_category   CASCADE;
                    create table temp_org_category
                    (
                        per_code   bigint       not null,
                        gen1       int          not null,
                        gen2       int          not null,
                        gen3       int          not null,
                        level      smallint     not null,
                        name       varchar(128) not null,
                        imp        smallint     not null,
                        org_code   varchar(16)  not null,
                        tr_name    varchar(128) not null default ''
                    );
                 '''
        self.db.execute(sqlcmd)
        
        fp = open(r'.\convert\mmi\category.txt','r')
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