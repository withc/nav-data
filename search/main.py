#import os
#import sys

import common.database
import common.logger
import config.config
import load.load_base
import check.mid_check
import compiler.compile

if __name__ == "__main__":
    common.logger.init_log()
    cfg = config.config.Config.get_instance()
    
    db_instance = common.database.CDB( "default", cfg.getDBPath() )
    db_instance.connect()
    
    print " ---- start load search data ----"
    #loader = load.load_base.CLoader( db_instance, cfg.getVendor() )
    #loader.load()
    
    print " ---- start check mid search data ----"
    checker = check.mid_check.CMid_check( db_instance )
    checker.run()
        
    print " ---- start compiler search data ----"
    comp_er = compiler.compile.CCompiler( db_instance )
    comp_er.run( )
    
    db_instance.close()
    common.logger.close_log()

