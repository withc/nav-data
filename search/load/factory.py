
import load.feature

def featureFactory( name, loader ):
    
    
    if name == 'tomtom':
        import load.tomtom
        loader.add_process( load.feature.CStartProcess() )
        loader.add_process( load.feature.CEndProcess() )
        loader.add_feature( load.tomtom.feat_place.CPlace( ) )
        loader.add_feature( load.tomtom.feat_poi.CPoi( ) )
        
    elif name == 'rdf':
        import load.rdf
        pass
    elif name == 'gaode':
        import load.gaode
        pass
    else:
        print '-- unkonw vendor %s' % name
