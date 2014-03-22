import logging

PROJECT='search'

def sub_log( name='' ):
    if name:
        return logging.getLogger( PROJECT+'.'+name )
    else:
        return logging.getLogger( PROJECT )
    
def init_log():
    logger = logging.getLogger(PROJECT)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter( "%(asctime)s - %(levelname)s: %(name)-16s >> %(message)s" )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

def close_log():
    logging.shutdown()