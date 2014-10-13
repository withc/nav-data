import common.shapefile
import load.table

class CbrTable(load.table.CTable):
    def __init__(self ):
        load.table.CTable.__init__(self, 'br')
        self.sf = None
    
    def _do_all(self):
        self.sf = common.shapefile.Reader(r"D:\my\shanghai\shanghai\road\Brshanghai")
        
        self._create_table( )
        self._read_file()
        self._create_index()     
        
    def _create_table(self):
        self.db.dropTable( self.name )
        sqlcmd = 'create table ' + self.name + '\n'
        sqlcmd += '(\n'
        for f in self.sf.fields:
            sqlcmd +=  self._field_sql( f )
        sqlcmd += ');'

        sqlcmd = '''
                create table <t>
                (
                  --gid       serial PRIMARY KEY,
                  mapid     int4,
                  id        int8,
                  nodeid    int8,
                  inlinkid  int8,
                  outlinkid int8,
                  direction varchar(1),
                  patternno varchar(8),
                  arrowno   varchar(8),
                  guidattr  varchar(1),
                  namekind  varchar(1),
                  passlid   varchar(120),
                  type      varchar(1),
                  geom      geometry(Point)
                );
                 '''
        sqlcmd = sqlcmd.replace( '<t>', self.name )
        self.db.do_execute( sqlcmd )
        
    def _read_file(self):
        
        shapes  = self.sf.shapes()
        records = self.sf.records()
        
        sqlcmd = self._insert_sql( len(records[0])+1 )
        for ( attr, geo ) in zip( records, shapes ):
            item = self._shape_value( attr,geo)
            self.db.execute( sqlcmd, item )
            
        self.db.commit()
    
    def _create_index(self):
        self.db.createGist( self.name, 'geom' )
        
        
        
        