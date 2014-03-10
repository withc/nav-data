# -*- coding: UTF8 -*-
'''
Created on 2014.2

@author: zhangpeng
'''

import psycopg2

class CDB(object):
    
    def __init__( self, name, path ):
        self.connected = False
        if path == '':
            print "Doesn't exist host IP"
        else:
            self.dbname = name
            self.srv_path = path
            
    def connect(self):
        '''connect to DB'''
        self.conn  = psycopg2.connect(self.srv_path) 
        self.cur = self.conn.cursor()
        self.connected = True
        
    def do_big_insert(self, sqlcmd ): 
        self.execute( sqlcmd )
       
    def execute(self, sqlcmd, parameters = []):
        '''execute commands '''
        try:
            if parameters:
                self.cur.execute(sqlcmd, parameters)
            else:
                self.cur.execute(sqlcmd)
            self.conn.commit()
            return 0
        except Exception,ex:
            print '%s:%s' % (Exception, ex)
            print 'SQL execute error:' + sqlcmd 
            raise
        
    def close(self):
        if self.connected == True:
            self.cur.close()
            self.conn.close()
            self.connected = False    

        
        
        
        