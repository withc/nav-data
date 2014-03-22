#import os
#import sys

import common.database
import common.logger
import config.config
import load.load_base
import check.mid_check
import compiler.compile
import dataprocess.compile

if __name__ == "__main__":
    common.logger.init_log()
    logger = common.logger.sub_log()
    
    cfg = config.config.Config.get_instance()
    
    db_instance = common.database.CDB( "default", cfg.getDBPath() )
    db_instance.connect()
    
    logger.info( cfg.getDBPath() )
    logger.info( " ---- start load search data ---- " )
    #loader = load.load_base.CLoader( db_instance, cfg.getVendor() )
    #loader.load()
    
    logger.info( " ---- start check mid search data ---- " )
    checker = check.mid_check.CMid_check( db_instance )
    checker.run()
        
    logger.info( " ---- start compiler search data ---- " )
    comp_er = dataprocess.compile.CCompiler( db_instance )
    comp_er.run( )
    
    logger.info( " ---- finish ---- " )
    db_instance.close()
    common.logger.close_log()

