import load.base.shp_table
import attribute

module = 'land'
#----------------------------------------------------------#   
class CTTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'T')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, module, self.name)