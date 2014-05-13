import load.feature

class CLink(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'link')
 
    def _domake_key(self):
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 2000, routeid, 2000 
                    from org_l_tran as tr
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_link( key, type )
                    select fe.feat_key, fe.feat_type
                      from org_l_tran   as tr
                      join mid_feat_key as fe
                        on tr.routeid = fe.org_id1 and 2000 = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert into temp_street_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7000,'L', ST_LineMerge(tr.the_geom)
                      from org_l_tran   as tr
                      join mid_feat_key as fe
                        on tr.routeid = fe.org_id1 and 2000 = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
                    insert into temp_street_name( key, type, nametype, langcode, name, tr_lang, tr_name )
                    with tr ( key, type, nav_namt, nav_name, alt_namt, alt_name, brdnamt, brdname )
                    as ( select fe.feat_key, fe.feat_type, nav_namt, nav_name, alt_namt, alt_name, brdnamt, brdname
                           from org_l_tran   as l
                           join mid_feat_key as fe
                             on l.routeid = fe.org_id1 and 2000 = fe.org_id2
                       )
                    select *
                      from (
                            select key, type, 'ON', 'THA', srch_adjust_name(nav_namt) as nt, 
                                   'ENG', srch_adjust_name(nav_name) as ne
                              from tr where nav_namt is not null
                            union
                            select key, type, 'AN', 'THA', srch_adjust_name(alt_namt) as nt, 
                                   'ENG', srch_adjust_name(alt_name) as ne
                              from tr where alt_namt is not null
                            union
                            select key, type, 'BU', 'THA', srch_adjust_name(brdnamt) as nt,  
                                   'ENG', srch_adjust_name(brdname) as ne
                              from tr where brdnamt is not null
                      ) as t1 where ne <> ''
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select f0.feat_key, f0.feat_type, 7001, f1.feat_key, f1.feat_type
                    from org_l_tran      as tr
                    join mid_feat_key    as f0
                      on tr.routeid  = f0.org_id1 and f0.org_id2 = 2000
                    join temp_admincode  as ta
                      on 3            = ta.type       and
                         tr.prov_code = ta.prov_code  and
                         tr.amp_code  = ta.amp_code   and
                         tr.tam_code  = ta.tam_code
                    join mid_feat_key     as f1
                      on ta.org_id1 = f1.org_id1 and ta.org_id2 = f1.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name_geom(self): 
        self._gen_nameid( 'street' )
        self._gen_geomid( 'street' )
        
        
        