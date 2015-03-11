import load.base.shp_table
import attribute

module = 'other'
#----------------------------------------------------------#   
class CAdminTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'Admin')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, module, self.name)
#----------------------------------------------------------#   
class CFNameTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'FName')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, module, self.name)