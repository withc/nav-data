import common.shapefile
import load.table

class CbrTable(load.table.CTable):
    def __init__(self ):
        load.table.CTable.__init__(self, 'br')
    
    def _do_all(self):
        sf = common.shapefile.Reader(r"D:\my\shanghai\shanghai\road\Brshanghai")
        shapes = sf.shapes()