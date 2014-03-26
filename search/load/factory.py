
import load.feature

def featureFactory( name, loader ):
    
    if name == 'tomtom':
        import load.tomtom
        loader.add_process( load.feature.CStartProcess() )
        loader.add_process( load.feature.CEndProcess() )
        loader.add_feature( load.tomtom.feat_category.CPoiCategory() )
        loader.add_feature( load.tomtom.feat_place.CPlace( ) )
        loader.add_feature( load.tomtom.feat_poi.CPoi( ) )
        loader.add_feature( load.tomtom.feat_link.CLink( ) )
        loader.add_feature( load.tomtom.feat_housenumber.CHouseNumber())
        
    elif name == 'globetech':
        import  load.globetech 
        loader.add_process( load.feature.CStartProcess() )
        loader.add_process( load.feature.CEndProcess() )
        loader.add_feature( load.globetech.feat_category.CPoiCategory() )
        loader.add_feature( load.globetech.feat_place.CPlace( ) )
        loader.add_feature( load.globetech.feat_postcode.CPostcode( ) )
        loader.add_feature( load.globetech.feat_poi.CPoi( ) )
        loader.add_feature( load.globetech.feat_link.CLink( ) )
         
    elif name == 'rdf':
        import load.rdf
        loader.add_process( load.feature.CStartProcess() )
        loader.add_process( load.feature.CEndProcess() )
        loader.add_feature( load.rdf.feat_category.CPoiCategory() )
        loader.add_feature( load.rdf.feat_place.CPlace( ) )
        loader.add_feature( load.rdf.feat_postcode.CPostcode( ) )
        loader.add_feature( load.rdf.feat_poi.CPoi( ) )
        loader.add_feature( load.rdf.feat_link.CLink( ) )
        loader.add_feature( load.rdf.feat_housenumber.CHouseNumber())
        
    elif name == 'gaode':
        import load.gaode
        loader.add_process( load.feature.CStartProcess() )
        loader.add_process( load.feature.CEndProcess() )
        loader.add_feature( load.gaode.feat_place.CPlace( ) )
        loader.add_feature( load.gaode.feat_poi.CPoi( ) )
        loader.add_feature( load.gaode.feat_link.CLink( ) )
    
    elif name == 'mmi':
        import load.mmi
        loader.add_process( load.feature.CStartProcess() )
        loader.add_process( load.feature.CEndProcess() ) 
        loader.add_feature( load.mmi.feat_category.CPoiCategory() )
        loader.add_feature( load.mmi.feat_place.CPlace( ) ) 
        loader.add_feature( load.mmi.feat_postcode.CPostcode( ) )
        loader.add_feature( load.mmi.feat_poi.CPoi( ) )
        loader.add_feature( load.mmi.feat_link.CLink( ) )  
    else:
        print '---- unkonw vendor %s' % name
        
