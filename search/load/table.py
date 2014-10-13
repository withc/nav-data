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
        
    def input(self):
        self._do_all()
        pass
    
    def _do_all(self):
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
        
    def _shape_value(self, attr, geom ):
        if 1 == geom.shapeType:
            geomstr = 'POINT(%s)' % ( ' '.join( [ str(x) for x in  geom.points[0] ] ) )
        elif 3 == geom.shapType:
            geomstr = 'LINE(%s)' % geom.points 
        elif 5 == geom.shapType:
            geomstr = 'POLY(%s)' % geom.points
        else:
            geomstr = ''

        item = [ str(x).strip()  for x in attr ]
        item.append( geomstr )
        return item
