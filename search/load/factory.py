
import load.base.table

def tableFactory( name, loader ):

    if name == 'siwei':
        import load.siwei

#         loader.add_table( load.siwei.table_road.CBrTable() )
#         loader.add_table( load.siwei.table_road.CCNLTable() )
#         loader.add_table( load.siwei.table_road.CCondTable() )
#         loader.add_table( load.siwei.table_road.CCRTable() )
#         loader.add_table( load.siwei.table_road.CCTable() )
#         loader.add_table( load.siwei.table_road.CDmTable() )
#         loader.add_table( load.siwei.table_road.CDrTable() )
#         loader.add_table( load.siwei.table_road.CICTable() )
#         loader.add_table( load.siwei.table_road.CLnTable() )
#         loader.add_table( load.siwei.table_road.CNTable() )
#         loader.add_table( load.siwei.table_road.CR_LNameTable() )
#         loader.add_table( load.siwei.table_road.CR_LZoneTable() )
#         loader.add_table( load.siwei.table_road.CR_NameTable() )
        loader.add_table( load.siwei.table_road.CRTable() )
#         loader.add_table( load.siwei.table_road.CTrfcSignTable() )
#         loader.add_table( load.siwei.table_road.CZ_LevelTable() )
#         
#         loader.add_table( load.siwei.table_back.CBLTable() )
#         loader.add_table( load.siwei.table_back.CBNTable() )
#         loader.add_table( load.siwei.table_back.CBPLTable() )
#         loader.add_table( load.siwei.table_back.CBPTable() )
#         loader.add_table( load.siwei.table_back.CBUPTable() )
#         loader.add_table( load.siwei.table_back.CDTable() )
#         
#         loader.add_table( load.siwei.table_land.CTTable() )
#         
#         loader.add_table( load.siwei.table_other.CAdminTable() )
#         loader.add_table( load.siwei.table_other.CFNameTable() )

        pass
    else:
        print '---- unkonw vendor %s' % name
        
