
class Config( object ):
    __instance = None
    _vendor  ='tomtom'
    _host    ='172.26.179.184'
    _dbname  ='14tmai_sea_tomtom_1312_ci'
    _user    ='postgres'
    _password=''

    @staticmethod
    def get_instance():
        if Config.__instance is None:
            Config.__instance = Config()
        return Config.__instance
    
    def __init__(self):
        pass

    def getVendor(self):
        return Config._vendor

    def getDBPath(self):
        return 'host=%s dbname=%s user=%s password=%s' % (Config._host, Config._dbname, Config._user, Config._password )