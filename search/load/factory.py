
import load.table

def tableFactory( name, loader ):

    if name == 'siwei':
        import load.siwei
        loader.add_table( load.siwei.table_road.CbrTable() )
        pass
    else:
        print '---- unkonw vendor %s' % name
        
