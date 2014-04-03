import entity

class CXTblData(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'xtbl_data')
          
    def _do(self):
        pass