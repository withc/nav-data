import time
import logging

PROJECT='search'

def sub_log( name='' ):
    if name:
        return logging.getLogger( PROJECT+'.'+name )
    else:
        return logging.getLogger( PROJECT )
    
def init_log( file='' ):
    logger = logging.getLogger(PROJECT)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('log\\test_'+file+'_'+time.strftime('%Y-%m-%d %H_%M_%S',time.localtime(time.time()))+'.log')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter( "%(asctime)s - %(levelname)s: %(name)-20s >> %(message)s" )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

def close_log():
    logging.shutdown()