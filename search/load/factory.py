
import load.feature
import load.common_work
import load.dealer_data

def featureFactory( name, loader ):

    if name == 'tomtom':
        import load.tomtom
        loader.add_process( load.tomtom.start_work.CStartWork() )
        loader.add_process( load.common_work.CEndProcess() )
        loader.add_feature( load.tomtom.feat_category.CPoiCategory() )
        loader.add_feature( load.tomtom.feat_place.CPlace( ) )
        loader.add_feature( load.tomtom.feat_postcode.CPostcode( ) )
        loader.add_feature( load.tomtom.feat_link.CLink( ) )
        
        loader.add_feature( load.tomtom.feat_mnpoi.CMNPoi( ) )
        loader.add_feature( load.tomtom.feat_poi.CPoi( ) )
        loader.add_feature( load.tomtom.feat_housenumber.CHouseNumber())
        
    elif name == 'globetech':
        import  load.globetech 
        loader.add_process( load.common_work.CStartProcess() )
        loader.add_process( load.common_work.CEndProcess() )
        loader.add_feature( load.globetech.feat_category.CPoiCategory() )
        loader.add_feature( load.globetech.feat_place.CPlace( ) )
        loader.add_feature( load.globetech.feat_postcode.CPostcode( ) )
        loader.add_feature( load.globetech.feat_link.CLink( ) )
        
        loader.add_feature( load.globetech.feat_poi.CPoi( ) )
        loader.add_feature( load.globetech.feat_housenumber.CHouseNumber())
         
    elif name == 'rdf':
        import load.rdf
        loader.add_process( load.common_work.CStartProcess() )
        loader.add_process( load.common_work.CEndProcess() )
        loader.add_feature( load.rdf.feat_category.CPoiCategory() )
        loader.add_feature( load.rdf.feat_place.CPlace( ) )
        loader.add_feature( load.rdf.feat_postcode.CPostcode( ) )
        loader.add_feature( load.rdf.feat_node.CNode( ) )
        loader.add_feature( load.rdf.feat_link.CLink( ) )
        
        loader.add_feature( load.rdf.feat_extpoi.CExtPoi() )
        loader.add_feature( load.rdf.feat_poi.CPoi( ) )
        loader.add_feature( load.rdf.feat_housenumber.CHouseNumber())
        
    elif name == 'gaode':
        import load.gaode
        loader.add_process( load.common_work.CStartProcess() )
        loader.add_process( load.common_work.CEndProcess() )
        loader.add_feature( load.gaode.feat_category.CPoiCategory() )
        loader.add_feature( load.gaode.feat_place.CPlace( ) )
        loader.add_feature( load.gaode.feat_postcode.CPostcode( ) )
        loader.add_feature( load.gaode.feat_link.CLink( ) )
        
        loader.add_feature( load.gaode.feat_poi.CPoi( ) )
    
    elif name == 'mmi':
        import load.mmi
        loader.add_process( load.common_work.CStartProcess() )
        loader.add_process( load.common_work.CEndProcess() ) 
        loader.add_feature( load.mmi.feat_category.CPoiCategory() )
        loader.add_feature( load.mmi.feat_place.CPlace( ) ) 
        loader.add_feature( load.mmi.feat_postcode.CPostcode( ) )
        loader.add_feature( load.mmi.feat_link.CLink( ) )
        
        loader.add_feature( load.mmi.feat_poi.CPoi( ) )  
        loader.add_feature( load.mmi.feat_housenumber.CHouseNumber())
    else:
        print '---- unkonw vendor %s' % name
        
    loader.add_part3( load.dealer_data.CDealerData() )    
