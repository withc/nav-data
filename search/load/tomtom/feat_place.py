import load.feature

class CPlace(load.feature.CFeature):
    def __init__(self ):
        print "tomtom's place feature"
        load.feature.CFeature.__init__(self,'place')

    def _domake_key(self):
        # delete the place which has no-name or is a dummy area
        # in usa/can, one state set to one a0 place,
        # but, we always insist that a0 is country. must do something...
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select distinct 3001, id, feattyp  from org_a0 where name is not null
                    union
                    select distinct 3002, id, feattyp  from org_a1 where name is not null
                    union
                    select distinct 3003, id, feattyp  from org_a2 where name is not null
                    union
                    select distinct 3008, id, feattyp  from org_a7 where name is not null
                    union
                    select distinct 3009, id, feattyp  from org_a8 where name is not null
                    union
                    select distinct 3010, id, feattyp  from org_a9 where name is not null
                    order by feattyp, id
                 '''
        self.db.execute( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                 insert into mid_place( key, type )
                 select feat_key, feat_type 
                   from mid_feat_key
                  where 3001 <= feat_type and feat_type <= 3010
                  order by feat_type, feat_key
                 '''
        self.db.execute( sqlcmd )
         
    def _domake_geomtry(self):
        tbs = ['org_a0','org_a1','org_a2','org_a8','org_a9']
        for tb in tbs:
            self._geomtry(tb)
        
    def _domake_name(self):
        sqlcmd = '''
                    insert into temp_feat_name( key, type, nametype, langcode, name )
                    select fe.feat_key, fe.feat_type, an.nametyp, an.namelc, an.name
                      from org_an       as an
                      join mid_feat_key as fe
                        on an.id = fe.org_id1 and an.feattyp = fe.org_id2
                 '''
        self.db.execute( sqlcmd )
        
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        self.db.execute( self._gen_admin_sql(0) )
        self.db.execute( self._gen_admin_sql(1) )
        self.db.execute( self._gen_admin_sql(2) )
        self.db.execute( self._gen_admin_sql(7) )
        self.db.execute( self._gen_admin_sql(8) )
        self.db.execute( self._gen_admin_sql(9) )
      
    def _geomtry(self, tb):
        sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7000,'A', a.geom
                     from (
                           select id, feattyp, st_multi (st_union(the_geom)) as geom
                             from  %s  
                            group by id, feattyp
                          ) as a
                     join mid_feat_key as fe
                       on a.id = fe.org_id1 and a.feattyp = fe.org_id2
                 ''' % tb
        self.db.execute( sqlcmd )
        
        if tb.find('a8') >= 0 or tb.find('a9') >= 0:
            sqlcmd = '''
                    insert into temp_feat_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7379, 'P', sm.the_geom
                      from %s           as a
                      join mid_feat_key as fe
                        on a.id = fe.org_id1 and a.feattyp = fe.org_id2
                      join org_sm       as sm
                        on a.citycenter = sm.id
                    ''' % tb
            self.db.execute( sqlcmd )
    def _gen_admin_sql(self, s):
        if s == 0:
            sqlcmd = self._select_admin(0)
        elif s == 1:
            sqlcmd = self._select_admin(1)+self._join_admin(1, 0)
        elif s == 2:
            sqlcmd = self._select_admin(2)+self._join_admin(2, 1)+self._join_admin(2, 0)
        elif s == 7:
            sqlcmd = self._select_admin(7)+self._join_admin(7, 2)+self._join_admin(7, 1)+self._join_admin(7, 0)
        elif s == 8:
            sqlcmd = self._select_admin(8)+self._join_admin(8, 7)+self._join_admin(8, 2)+self._join_admin(8, 1)+self._join_admin(8, 0)
        elif s == 9:
            sqlcmd = self._select_admin(9)+self._join_admin(9, 8)+self._join_admin(9, 7)+self._join_admin(9, 2)+self._join_admin(9, 1)+self._join_admin(9, 0)
            
        return sqlcmd.replace(' org_a0 ', ' ( select distinct id, order00 from org_a0 ) ' )
    
    def _join_admin(self, s, d):
        sql ='''
                left join org_a<d>      a<d>
                       on a<s>.order0<d> = a<d>.order0<d>
                left join mid_feat_key  f<d>
                       on a<d>.id = f<d>.org_id1 and f<d>.org_id2 = <c>
            '''
        sql = sql.replace('<s>', str(s))
        sql = sql.replace('<d>', str(d))
        sql = sql.replace('<c>', str(1111+d))
        return sql
    def _select_admin(self, s):
        if s == 9:
            field = '''f1.feat_key, 
                       COALESCE( f2.feat_key, 0 ), 
                       COALESCE( f7.feat_key, 0 ), 
                       f8.feat_key, f9.feat_key'''
        elif s == 8:
            field = '''f1.feat_key, 
                       COALESCE( f2.feat_key, 0 ), 
                       COALESCE( f7.feat_key, 0 ), 
                       f8.feat_key, 0'''
        elif s == 7:
            field = '''f1.feat_key, 
                       COALESCE( f2.feat_key, 0 ), 
                       f7.feat_key, 0, 0'''
        elif s == 2:
            field = '''f1.feat_key, f2.feat_key, 0, 0, 0'''
        elif s == 1:
            field = '''f1.feat_key, 0, 0, 0, 0'''
        elif s == 0:
            field = '0, 0, 0, 0, 0'
        else:
            field = ''
         
        sql = '''insert into mid_place_admin( key, type, a0, a1, a2, a7, a8, a9 )
                 select  f<s>.feat_key, f<s>.feat_type, f0.feat_key, ''' + field + '''
                   from org_a<s>      a<s>
                   join mid_feat_key  f<s>
                     on a<s>.id = f<s>.org_id1 and f<s>.org_id2 = <c>
              '''
        sql = sql.replace('<s>', str(s))
        sql = sql.replace('<c>', str(s+1111))
        return sql

        
        
        
        
        