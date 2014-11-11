import load.base.shp_table
import attribute

#----------------------------------------------------------#   
class CBrTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'Br')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)
    
#----------------------------------------------------------#        
class CCNLTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'CNL')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)        

#----------------------------------------------------------#          
class CCondTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'Cond')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)       

#----------------------------------------------------------#          
class CCRTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'CR')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)  
    
#----------------------------------------------------------#          
class CCTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'C')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)

#----------------------------------------------------------#          
class CDmTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'Dm')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)
    
#----------------------------------------------------------#          
class CDrTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'Dr')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)
    
#----------------------------------------------------------#          
class CICTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'IC')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name) 

#----------------------------------------------------------#          
class CLnTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'Ln')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)  

#----------------------------------------------------------#          
class CNTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'N')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)

#----------------------------------------------------------#          
class CR_LNameTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'R_LName')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)

#----------------------------------------------------------#          
class CR_LZoneTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'R_LZone')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)   

#----------------------------------------------------------#          
class CR_NameTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'R_Name')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)

#----------------------------------------------------------#          
class CRTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'R')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)
 
#----------------------------------------------------------#     
class CTrfcSignTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'TrfcSign')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)

#----------------------------------------------------------#     
class CZ_LevelTable(load.base.shp_table.CTableOfShp):
    def __init__(self ):
        load.base.shp_table.CTableOfShp.__init__(self, 'Z_Level')
        self.sf = None
    
    def _get_file(self, path):
        return attribute.MakeFileName(path, self.name)
