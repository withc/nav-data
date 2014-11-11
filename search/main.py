#coding=utf-8
#import os
#import sys

import common.database
import common.logger
import config.config
import load.load_db
import convert.convert_db
import check.mid_check
import compiler.compile


if __name__ == "__main__":
    cfg = config.config.Config.get_instance()
    
    common.logger.init_log( cfg.getVendor() )
    logger = common.logger.sub_log()
    
    db_instance = common.database.CDB( "default", cfg.getDBPath() )
    db_instance.connect()
    
    logger.info( cfg.getDBPath() )
    
    logger.info( " ---- start load  data ---- " )
    loader = load.load_db.CLoader( db_instance, cfg.getVendor(), cfg.getDataPath() )
    loader.run()
    
    logger.info( " ---- start convert search data ---- " )
    #converter = convert.convert_db.CConverter( db_instance, cfg.getVendor() )
    #converter.run()
    
    logger.info( " ---- start check mid search data ---- " )
    #checker = check.mid_check.CMid_check( db_instance )
    #checker.run()
        
    logger.info( " ---- start compiler search data ---- " )
    #comp_er = compiler.compile.CCompiler( db_instance )
    #comp_er.run( )
    
    logger.info( " ---- finish ---- " )
    db_instance.close()
    common.logger.close_log()

