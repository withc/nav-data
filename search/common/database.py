# -*- coding: UTF8 -*-
'''
Created on 2014.2

@author: zhangpeng
'''
import re
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
        if self.connected == True:
            return -1
        
        self.conn  = psycopg2.connect(self.srv_path) 
        self.cur = self.conn.cursor()
        self.connected = True
        
    def fetchone(self):
        '''读一条记录'''
        return self.cur.fetchone()  
     
    def fetchall(self):
        return self.cur.fetchall()
     
    def do_big_insert(self, sqlcmd ): 
        self.execute( sqlcmd )
        self.commit()
        m=re.match( '\s*?(insert)\s+?(into)\s+?(.*?)\s*?\(', sqlcmd,  re.IGNORECASE )
        if m:
            self.analyze( m.group(3) )
            
    def do_execute(self, sqlcmd):
        self.execute( sqlcmd )
        self.commit()
    
    def existTable(self, table ):
        sql = '''
              select * from pg_tables where tablename = '%s'
              ''' % table
        count = self.getResultCount(sql)
        
        return (0 != count)
    
    def existTableColumn(self, table, column ):
        sql = '''
              select * 
                from information_schema.columns  
               where table_name   = '%s' and 
                     column_name = '%s'
              ''' % (table, column)
        count = self.getResultCount(sql)
        
        return (0 != count)
     
    def execute(self, sqlcmd, parameters = []):
        '''execute commands '''
        try:
            if parameters:
                self.cur.execute(sqlcmd, parameters)
            else:
                self.cur.execute(sqlcmd)
            #self.conn.commit()
            return 0
        except Exception,ex:
            print '%s:%s' % (Exception, ex)
            print 'SQL execute error:' + sqlcmd 
            raise
        
    def commit(self):
        self.conn.commit()
        return 0
    def dropTable(self, table):
        sqlcmd = "DROP TABLE IF EXISTS %s CASCADE;" % table
        self.execute( sqlcmd )
                
    def createIndex(self, table, column ):
        if isinstance( column, str ):
            sqlcmd = '''
                  CREATE INDEX idx_%s_%s
                  ON %s
                  USING btree
                  (%s);
              ''' % (table, column, table, column )
        else:
            sqlcmd = '''
                  CREATE INDEX idx_%s_%s
                  ON %s
                  USING btree
                  (%s);
              ''' % (table, '_'.join(column), table, ','.join(column) )

        self.do_execute(sqlcmd)
        self.analyze( table )
        
    def createGist(self, table, column ):
        sqlcmd = '''
                 create index gist_%s_%s
                 on %s
                 using gist
                 (%s);
                 ''' % (table, column, table, column )
        self.do_execute(sqlcmd)
           
    def analyze(self, table):
        self.cur.execute( 'ANALYZE %s' % table )
        
    def run(self, filename ):  
        fp = open(filename,'r')
        self.execute( fp.read() )
        fp.close()
      
    def getResultCount(self, sqlcmd):
        sql = 'select count(*) from ( ' + sqlcmd + ' ) as zz'
        self.execute(sql)
        rows = self.cur.fetchone()
        if rows:
            return rows[0]
        return 0
    
    def getOneResult(self, sqlcmd):
        sqlcmd = sqlcmd + '  limit 1'
        self.execute(sqlcmd)
        rows = self.cur.fetchone()
        if rows:
            return rows
        return 0
        
    def close(self):
        if self.connected == True:
            self.cur.close()
            self.conn.close()
            self.connected = False    

        
        
        
        