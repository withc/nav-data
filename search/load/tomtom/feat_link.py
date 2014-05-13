import load.feature

class CLink(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self,'link')

    def _domake_key(self):
        # copy all link, even it has no name.
        # some link that has no name is the closest road poi was located.
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 2000, id, feattyp 
                      from org_nw as nw
                     where feattyp in ( 4110, 4130 )
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_link( key, type )
                    select fe.feat_key, fe.feat_type
                      from org_nw       as nw
                      join mid_feat_key as fe
                        on nw.id = fe.org_id1 and nw.feattyp = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert into temp_street_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7000,'L', ST_LineMerge(nw.the_geom) as the_geom 
                      from org_nw       as nw
                      join mid_feat_key as fe
                        on nw.id = fe.org_id1 and nw.feattyp = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        sqlcmd = '''
                    insert into temp_street_name( key, type, nametype, langcode, name, tr_lang, tr_name, ph_lang, ph_name )
                    select feat_key, feat_type, nametyp, namelc, name, '', '', 
                           COALESCE(ph_lang, ''), COALESCE(ph_name,'')
                      from (
                            select fe.feat_key, fe.feat_type,  
                                    CASE  
                                      WHEN gc.nametyp&1 <> 0 THEN 'ON'
                                      WHEN gc.nametyp&4 <> 0 THEN 'RN'
                                      WHEN gc.nametyp&8 <> 0 THEN 'BU'
                                      ELSE 'AN'
                                    END as nametyp,
                                    gc.namelc, gc.fullname as name,
                                    ph.ph_lang, ph.ph_name, 
                                    row_number() over (partition by fe.feat_key, fe.feat_type, gc.namelc, gc.fullname 
                                                       order by case 
                                                                 when gc.namelc    = ph.ph_lang then 1
                                                                 when gc.l_laxonlc = ph.ph_lang then 2
                                                                 else 3
                                                                end, ph.ph_name
                                                        ) as seq
                            from org_gc       as gc
                            join mid_feat_key as fe
                              on gc.id = fe.org_id1 and gc.feattyp = fe.org_id2
                       left join temp_phoneme as ph
                              on gc.feattyp  = ph.featclass  and
                                 gc.id       = ph.shapeid    and
                                 gc.namelc   = ph.lang       and
                                 gc.fullname = ph.name
                            ) as t
                      where t.seq = 1  
                      order by feat_key
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select  fe.feat_key, fe.feat_type, 7001, f1.feat_key, f1.feat_type
                    from org_ta       as ta
                    join mid_feat_key as fe
                      on ta.aretyp   in (1119,1120) and
                         ta.id       = fe.org_id1   and
                         ta.trpeltyp = fe.org_id2
                    join mid_feat_key as f1
                      on ta.areid = f1.org_id1 and ta.aretyp = f1.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name_geom(self): 
        self._gen_nameid( 'street' )
        self._gen_geomid( 'street' )