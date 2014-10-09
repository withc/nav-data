
import convert.feature
import convert.common_work

def featureFactory( name, converter ):

    if name == 'tomtom':
        import convert.tomtom
        converter.add_process( convert.tomtom.start_work.CStartWork() )
        converter.add_process( convert.common_work.CEndProcess() )
        converter.add_feature( convert.tomtom.feat_category.CPoiCategory() )
        converter.add_feature( convert.tomtom.feat_place.CPlace( ) )
        converter.add_feature( convert.tomtom.feat_postcode.CPostcode( ) )
        converter.add_feature( convert.tomtom.feat_link.CLink( ) )
        
        converter.add_feature( convert.tomtom.feat_mnpoi.CMNPoi( ) )
        converter.add_feature( convert.tomtom.feat_poi.CPoi( ) )
        converter.add_feature( convert.tomtom.feat_housenumber.CHouseNumber())
        
    elif name == 'globetech':
        import convert.globetech
        converter.add_process( convert.common_work.CStartProcess() )
        converter.add_process( convert.common_work.CEndProcess() )
        converter.add_feature( convert.globetech.feat_category.CPoiCategory() )
        converter.add_feature( convert.globetech.feat_place.CPlace( ) )
        converter.add_feature( convert.globetech.feat_postcode.CPostcode( ) )
        converter.add_feature( convert.globetech.feat_link.CLink( ) )
        
        #converter.add_feature( convert.globetech.feat_poi_dealer.CPoiDealer( ) )
        converter.add_feature( convert.globetech.feat_poi.CPoi( ) )
        converter.add_feature( convert.globetech.feat_housenumber.CHouseNumber())
         
    elif name == 'rdf':
        import convert.rdf
        converter.add_process( convert.common_work.CStartProcess() )
        converter.add_process( convert.common_work.CEndProcess() )
        converter.add_feature( convert.rdf.feat_category.CPoiCategory() )
        converter.add_feature( convert.rdf.feat_place.CPlace( ) )
        converter.add_feature( convert.rdf.feat_postcode.CPostcode( ) )
        converter.add_feature( convert.rdf.feat_node.CNode( ) )
        converter.add_feature( convert.rdf.feat_link.CLink( ) )
        
        converter.add_feature( convert.rdf.feat_extpoi.CExtPoi() )
        #converter.add_feature( convert.rdf.feat_poi_dealer.CPoiDealer( ) )
        converter.add_feature( convert.rdf.feat_poi.CPoi( ) )
        converter.add_feature( convert.rdf.feat_housenumber.CHouseNumber())
        
    elif name == 'gaode':
        import convert.gaode
        converter.add_process( convert.common_work.CStartProcess() )
        converter.add_process( convert.common_work.CEndProcess() )
        converter.add_feature( convert.gaode.feat_category.CPoiCategory() )
        converter.add_feature( convert.gaode.feat_place.CPlace( ) )
        converter.add_feature( convert.gaode.feat_postcode.CPostcode( ) )
        converter.add_feature( convert.gaode.feat_link.CLink( ) )
        
        converter.add_feature( convert.gaode.feat_poi.CPoi( ) )
    
    elif name == 'mmi':
        import convert.mmi
        converter.add_process( convert.common_work.CStartProcess() )
        converter.add_process( convert.common_work.CEndProcess() ) 
        converter.add_feature( convert.mmi.feat_category.CPoiCategory() )
        converter.add_feature( convert.mmi.feat_place.CPlace( ) ) 
        converter.add_feature( convert.mmi.feat_postcode.CPostcode( ) )
        converter.add_feature( convert.mmi.feat_link.CLink( ) )
        
        converter.add_feature( convert.mmi.feat_poi.CPoi( ) )  
        converter.add_feature( convert.mmi.feat_housenumber.CHouseNumber())
    else:
        print '---- unkonw vendor %s' % name
        

    #loader.add_part3( convert.CDealerData() )
