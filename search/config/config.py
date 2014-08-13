
class Config( object ):
    __instance = None
    _vendor  ='rdf'
    _host    ='172.26.179.187'
    _dbname  ='test_sgp_rdf'
    _user    ='postgres'
    _password=''

    @staticmethod
    def get_instance():
        if Config.__instance is None:
            Config.__instance = Config()
        return Config.__instance
    
    def __init__(self):
        pass

    def set_vendor(self, value):
        Config._vendor = value
    def set_host(self, value):
        Config._host = value
    def set_dbname(self, value):
        Config._dbname = value
    def set_user(self, value):
        Config._user = value
    def set_password(self, value):
        Config._password = value 
        
    def getVendor(self):
        return Config._vendor
    
    def get_dbname(self):
        return Config._dbname

    def getDBPath(self):
        return 'host=%s dbname=%s user=%s password=%s' % (Config._host, Config._dbname, Config._user, Config._password )
    