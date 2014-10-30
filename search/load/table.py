import common.logger

class CTable(object):
    
    def __init__(self, name='table'):
        self.db     = None
        self.name   = name
        self.logger = common.logger.sub_log( self.name )
        self.logger.info('init')
   
    def attach_db(self, database, vendor=''):
        self.db = database
        self.vendor = vendor
        
    def input(self, path):
        self.logger.info('begin load table %s' % self.name )
        self._do_all( path )
        self.logger.info('end load table %s' % self.name )
        pass
    
    def _do_all(self, path):
        pass

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
                v.decode('gb2312') #.encode('utf-8')
            else:
                v = str(v)
            item.append( v.strip() )
            
        if geomstr != '':
            item.append( geomstr )
            
        return item

    def __point_str(self, point ):
        return ' '.join( [ str(x) for x in point ] )
    
    