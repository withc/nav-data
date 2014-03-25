import load.feature

class CPlace(load.feature.CFeature):
    def __init__(self ):
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
        self.db.do_big_insert( sqlcmd )
        
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
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                 insert into  mid_place( key, type )
                      select  feat_key, feat_type 
                        from  mid_feat_key
                       where  3001 <= feat_type and feat_type <= 3010
                    order by  feat_type, feat_key
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        # get the country point for india
        sqlcmd = '''
                 insert into temp_feat_geom( key, type, code, geotype, geom ) 
                 select f.feat_key, f.feat_type, 7379, 'P', st_geometryn(c.the_geom,1)
                   from temp_admincode        as t 
                   join mid_feat_key          as f
                     on t.org_id1   = f.org_id1 and 
                        t.org_id2   = f.org_id2 and
                        t.kind      = 10
                   join org_city_centre_point as c
                     on c.name = 'New Delhi'
                 '''
        self.db.do_big_insert( sqlcmd )
        # get the state point
        sqlcmd = '''
                 insert into temp_feat_geom( key, type, code, geotype, geom ) 
                 select f.feat_key, f.feat_type, 7379, 'P', st_geometryn(c.the_geom,1)
                   from org_capital_indicator as ca
                   join temp_admincode        as t
                     on ca.stt_id  = t.id and t.kind = 9 
                   join mid_feat_key          as f
                     on t.org_id1   = f.org_id1 and 
                        t.org_id2   = f.org_id2
                   join org_city_centre_point as c
                     on ca.capital_id  = c.id      
                        -- t.parent_id = c.adminid
                 ''' 
        self.db.do_big_insert( sqlcmd )
        
        # get the city point
        sqlcmd = '''
                 insert into temp_feat_geom( key, type, code, geotype, geom ) 
                 select f.feat_key, f.feat_type, 7379, 'P', st_geometryn(c.the_geom,1)
                   from temp_admincode        as t 
                   join mid_feat_key          as f
                     on t.org_id1   = f.org_id1 and 
                        t.org_id2   = f.org_id2
                   join org_city_centre_point as c
                     on t.id        = c.id       and
                        t.parent_id = c.adminid
                 ''' 
        self.db.do_big_insert( sqlcmd )
           
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
                 select * 
                 from (
                      select key, type, 'ON', 'ENG', name from ad 
                       union
                      select key, type, 'AN', 'ENG', regexp_split_to_table(alt, ';') as name from ad
                      ) as aa
                 where aa.name <> ''
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        sqlcmd = '''
                 insert into mid_full_area()
                 select 
                   from 
                 '''
        
    def _domake_relation(self):
        sqlcmd = '''
             insert into mid_place_admin( key, type, a0, a1, a2, a7, a8, a9 )
               with ad ( f_key, f_type, kind, id, parent_id )
                    as (
                         select f.feat_key, f.feat_type, t.kind, t.id, t.parent_id
                           from temp_admincode    as t 
                           join mid_feat_key      as f
                             on t.org_id1   = f.org_id1 and 
                                t.org_id2   = f.org_id2
                        )
              select a0.f_key, a0.f_type, a0.f_key, 0, 0, 0, 0, 0
                from ad       as a0
               where a0.kind = 10
              union
              select a1.f_key, a1.f_type, a0.f_key, a1.f_key, 0, 0, 0, 0
                from ad       as a1
                join ad       as a0
                  on a1.parent_id = a0.id 
               where a1.kind = 9
              union 
              select a8.f_key, a8.f_type, a0.f_key, a1.f_key, 0, 0, a8.f_key, 0
                from ad       as a8
                join ad       as a1
                  on a8.parent_id = a1.id
                join ad       as a0
                  on a1.parent_id = a0.id
               where a8.kind = 2
              union
              select a9.f_key, a9.f_type, a0.f_key, a1.f_key, 0, 0, a8.f_key, a9.f_key
                from ad       as a9 
                join ad       as a8
                  on a9.parent_id = a8.id
                join ad       as a1
                  on a8.parent_id = a1.id
                join ad       as a0
                  on a1.parent_id = a0.id
               where a9.kind = 1
               order by 1
                '''
        self.db.do_big_insert( sqlcmd )
        
        