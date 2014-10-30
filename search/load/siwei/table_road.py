import common.shapefile
import load.table
import attribute

class CbrTable(load.table.CTable):
    def __init__(self ):
        load.table.CTable.__init__(self, 'R_Name')
        self.sf = None
    
    def _do_all(self, path):
        self._open( attribute.MakeFileName(path, self.name) )
        
        self._create_table( )
        self._read_file()
        self._create_index()   
          
    def _open(self, filename ):
        self.sf =  common.shapefile.Reader( filename )
        
    def _create_table(self):
        self.db.dropTable( self.name )
        sqlcmd = 'create table ' + self.name + '\n'
        sqlcmd += '(\n'
        
        for f in self.sf.fields[1:-1]:
            sqlcmd +=  self._field_sql( f )
            
        if self._have_geom():
            sqlcmd +=  self._field_sql( self.sf.fields[-1], False )
        else:
            sqlcmd +=  self._field_sql( self.sf.fields[-1], True )
            
        sqlcmd += self._geom_sql( self.sf.shape(0) )
        
        sqlcmd += ');'

        self.db.do_execute( sqlcmd )

    def _read_file(self):

        sqlcmd = self._insert_sql( self._get_field_num() )
        idx = 0
        count = self.sf.numRecords
        while idx < count:
            item = self.sf.shapeRecord(idx)
            itemValue = self._shape_value( item.record, item.shape)
            self.db.execute( sqlcmd, itemValue )
            idx += 1
            if ( 0 == idx % 10000 ):
                self.db.commit()
                self.logger.info( 'finish insert %d' % idx )

        self.db.commit()
    
    def _create_index(self):
        self.db.createGist( self.name, 'geom' )
    
    def _get_field_num(self):
        num = len(self.sf.record(0))
        if self._have_geom():
            num += 1
        return num
   
    def _have_geom(self):
        return self.sf.shape(0).shapeType != 0
        
        
        
        
        