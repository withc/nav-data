import load.base.shp_table
import attribute

module = 'back'
#----------------------------------------------------------#   
class CBLTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'BL')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, module, self.name)
#----------------------------------------------------------#   
class CBNTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'BN')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, module, self.name)
#----------------------------------------------------------#   
class CBPLTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'BPL')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, module, self.name)
#----------------------------------------------------------#   
class CBPTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'BP')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, module, self.name)
#----------------------------------------------------------#   
class CBUPTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'BUP')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, module, self.name)
#----------------------------------------------------------#   
class CDTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'D')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, module, self.name)
    