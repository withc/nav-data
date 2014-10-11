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
