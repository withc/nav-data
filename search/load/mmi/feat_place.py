import load.feature

class CPlace(load.feature.CFeature):
    def __init__(self ):
        print "mmi's place"
        load.feature.CFeature.__init__(self, 'place')
 
    def _domake_key(self):
  
        sqlcmd = '''
                    insert into temp_admincode( kind, id, parent_id, org_id1, org_id2 )
                     select kind, id, parent_id, row_number() over( ), kind  from 
                     (
                       select distinct kind, id, parent_id
                         from org_area
                         order by kind DESC,  parent_id, id
                      ) as a
                 '''
        self.db.execute( sqlcmd )
        
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select case   org_id2
                             when 10 then 3001
                             when  9 then 3002
                             when  2 then 3009
                             when  1 then 3010
                             else  0
                            end,
                            org_id1,
                            org_id2
                       from temp_admincode
                 '''
        self.db.execute( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                 insert into  mid_place( key, type )
                      select  feat_key, feat_type 
                        from  mid_feat_key
                       where  3001 <= feat_type and feat_type <= 3010
                    order by  feat_type, feat_key
                 '''
        self.db.execute( sqlcmd )
    
    def _domake_geomtry(self):
        # get the city point
        sqlcmd = '''
                 insert into temp_feat_geom( key, type, code, geotype, geom ) 
                 select f.feat_key, f.feat_type, 7379, 'P', c.geom
                   from temp_admincode        as t 
                   join mid_feat_key          as f
                     on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                   join org_city_centre_point as c
                     on t.id        = c.id       and
                        t.parent_id = c.adminid
                 ''' 
        self.db.execute( sqlcmd )
        # get the state and country point
        # todo..
        
    def _domake_name(self):
        
        sqlcmd = '''
                 insert into temp_feat_name( key, type, nametype, langcode, name )
                 with ad ( key, type, name, alt ) as
                 (
                 select f.feat_key, f.feat_type, a.name, a.names
                   from org_area       as a
                   join temp_admincode as t
                     on a.kind      = t.kind       and
                        a.id        = t.id         and
                        a.parent_id = t.parent_id
                   join mid_feat_key   as f
                     on t.org_id1 = f.org_id1 and t.org_id2 = f.org_id2
                 )
                 select key, type, 'ON', 'ENG', name from ad 
                 union
                 select key, type, 'AN', 'ENG', regexp_split_to_table(alt, ';') from ad  
                 '''
        self.db.execute( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        sqlcmd = '''
                insert into mid_place_admin( key, type, a0, a1, a2, a7, a8, a9 )
                '''
        self.db.execute( sqlcmd )
        
        