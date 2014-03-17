import load.feature

class CPlace(load.feature.CFeature):
    def __init__(self ):
        print "rdf's place"
        load.feature.CFeature.__init__(self, 'place')
 
    def _domake_key(self):
  
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 1110+admin_order, admin_place_id, admin_order
                      from rdf_admin_hierarchy
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

        sqlcmd = '''
             insert into temp_feat_geom( key, type, code, geotype, geom ) 
                 ''' 
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        
        sqlcmd = '''
                 insert into temp_feat_name( key, type, nametype, langcode, name )
                 select p.key, p.type, 
                        case  
                          when ns.name_type = 'B' and ns.is_exonym = 'N' then 'ON'
                          else 'AN'
                        end,
                        m.language_code, m.name
                   from mid_place         as p
                   join mid_feat_key      as f
                     on p.key = f.feat_key and p.type = f.feat_type
                   join rdf_feature_names as ns
                     on f.org_id1  = ns.feature_id
                   join rdf_feature_name as m
                     on ns.name_id = m.name_id
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        sqlcmd = '''
                insert into mid_place_admin( key, type, a0, a1, a2, a7, a8, a9 )
                select fe.feat_key, fe.feat_type, 
                       f0.f_key, 
                       COALESCE( f1.feat_key, 0 ),
                       COALESCE( f2.feat_key, 0 ),
                       0,
                       COALESCE( f8.feat_key, 0 ),
                       COALESCE( f8.feat_key, 0 )
                  from rdf_admin_hierarchy as a
             left join mid_feat_key        as fe
                    on a.admin_place_id = fe.org_id1
             left join mid_feat_key        as f0
                    on a.country_id = f0.org_id1
             left join mid_feat_key        as f1
                    on a.order1_id = f1.org_id1
             left join mid_feat_key        as f2
                    on a.order2_id = f2.org_id1
             left join mid_feat_key        as f8
                    on a.order8_id = f8.org_id1
             left join mid_feat_key        as f9
                    on a.builtup_id = f9.org_id1
                '''
        self.db.do_big_insert( sqlcmd )
        
        