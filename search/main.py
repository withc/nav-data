import os
import sys

import load.load_base

if __name__ == "__main__":
    print " ---- start search data compiler ----"
    config_path = "config\\config.ini"
    loader = load.load_base.CLoader()
    loader.load(config_path)

