import common.shapefile
import table

class CTableOfShp(table.CTable):
    def __init__(self, name='shape' ):
        table.CTable.__init__( self, name )
        self.sf = None
        
    def _do_all(self, path):
        self._open( self._get_file( path ) )
        
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
        if self._have_geom():
            self.db.createGist( self.name, 'geom' )
    
    def _get_field_num(self):
        num = len(self.sf.record(0))
        if self._have_geom():
            num += 1
        return num
   
    def _have_geom(self):
        return self.sf.shape(0).shapeType != 0
        
    def _field_sql(self, field, isEnd = False ):
        ''' 
        /************************************************************************/
        /*                       DBFGetNativeFieldType()                        */
        /*                                                                      */
        /*      Return the DBase field type for the specified field.            */
        /*                                                                      */
        /*      Value can be one of: 'C' (String), 'D' (Date), 'F' (Float),     */
        /*                           'N' (Numeric, with or without decimal),    */
        /*                           'L' (Logical),                             */
        /*                           'M' (Memo: 10 digits .DBT block ptr)       */
        /************************************************************************/ 
        '''
        sqlcmd = field[0].lower()
        if 'C' == field[1]:
            sqlcmd += '  varchar(%d)' % field[2]
        elif 'L' == field[1]:
            sqlcmd += '  bool'
        elif 'D' == field[1]:
            pass
        elif 'N' == field[1]:
            if field[3] > 0:
                sqlcmd += '  int8'
            else: 
                sqlcmd += '  float8'
        elif 'F' == field[1]:
            sqlcmd += '  float8'
        else:
            pass
        if  isEnd:
            sqlcmd += '\n'
        else:
            sqlcmd += ',\n'
        return sqlcmd

    def _insert_sql(self, num ):
        sqlcmd = 'insert into ' + self.name + ' values(' + ','.join([ '%s' for x in range(num) ]) +')'
        return sqlcmd
    
    def _geom_sql(self, geom ):
        sqlcmd = 'geom '
        if 1 == geom.shapeType:
            sqlcmd += ' geometry(Point)\n'
        elif 3 == geom.shapeType:
            sqlcmd += ' geometry(LineString)\n'
        elif 5 == geom.shapeType:
            sqlcmd += ' geometry(POLYGON)\n'
        else:
            sqlcmd = ''
            
        return sqlcmd
            
    def _shape_value(self, attr, geom ):
        if 1 == geom.shapeType:
            geomstr = 'POINT(%s)' % ( self.__point_str( geom.points[0] ) )
        elif 3 == geom.shapeType:
            geomstr = 'LINESTRING(%s)' % ( ','.join ( self.__point_str(x) for x in geom.points ) )
        elif 5 == geom.shapeType:
            geomstr = 'POLYGON(%s)' % geom.points
        else:
            geomstr = ''

        item = []
        for v in attr:
            if isinstance(v, str): 
                v=v.decode('CP936').encode('utf-8')
            else:
                v = str(v)
            item.append( v.strip() )
            
        if geomstr != '':
            item.append( geomstr )
            
        return item

    def __point_str(self, point ):
        return ' '.join( [ str(x) for x in point ] )
    