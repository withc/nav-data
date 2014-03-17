#import os
#import sys

import common.logger
import load.load_base

if __name__ == "__main__":
    common.logger.init_log()
    
    print " ---- start search data load ----"
    config_path = "config\\config.ini"
    loader = load.load_base.CLoader()
    loader.load(config_path)
    
    common.logger.close_log()

