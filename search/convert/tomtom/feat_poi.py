import convert.feature

class CPoi(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self,'poi')
        
    def _domake_key(self):
        sqlcmd = '''
                    insert into mid_feat_key( feat_type, org_id1, org_id2 )
                    select 1000, id, feattyp 
                      from org_pi as pi
                     where feattyp <> 9920 and name is not null
                     order by id
                 '''
        #if there is mnpoi, we should ignore the this poi .
        #the core product version will be overwritten by MultiNet POI
        
        #self.db.do_big_insert( sqlcmd )
        
    def _domake_feature(self):
        sqlcmd = '''
                    insert into mid_poi( key, type, gen_code, imp )
                    select fe.feat_key, fe.feat_type, COALESCE( cc.per_code, c.per_code), pi.import
                      from org_pi       as pi
                      join mid_feat_key as fe
                        on pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                      join temp_org_category as c
                        on pi.feattyp = c.org_code
                 left join temp_org_category as cc
                        on pi.subcat = cc.org_code
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        sqlcmd = '''
                    insert into temp_poi_geom( key, type, code, geotype, geom )
                    select fe.feat_key, fe.feat_type, 7000,'P', pi.the_geom
                      from org_pi       as pi
                      join mid_feat_key as fe
                        on pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
        # just get the first entry point
        sqlcmd = '''
              insert into temp_poi_geom( key, type, code, geotype, geom )
              select feat_key, feat_type, 9920,'P', the_geom
                from ( 
                  select fe.feat_key, fe.feat_type,  p1.the_geom, 
                         row_number() over (partition by pr.poiid, pr.belpoityp order by pr.entrytyp, pr.gid ) as seq
                    from org_pi       as pi
                    join mid_feat_key as fe
                      on pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    join org_pr       as pr
                      on pi.id = pr.poiid
                    join org_pi       as p1
                      on pr.belpoityp = 9920  and
                         pr.belpoiid  = p1.id 
                     ) as t
                where t.seq = 1
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_name(self):
        # poi name
        sqlcmd = '''
                  insert into temp_poi_name( key, type, nametype, langcode, name, tr_lang, tr_name, ph_lang, ph_name )
                  select feat_key, feat_type, nametyp, namelc, name, '', '', 
                         COALESCE(ph_lang, ''), COALESCE(ph_name,'')
                    from (
                          select fe.feat_key, fe.feat_type, p.nametyp, p.namelc, p.name,
                                 ph.ph_lang, ph.ph_name, 
                                 row_number() over (partition by fe.feat_key, fe.feat_type, p.namelc, p.name 
                                                    order by case 
                                                               when p.namelc = ph.ph_lang then 1
                                                               else 3
                                                             end, ph.ph_name
                                                    ) as seq
                            from org_pinm     as p
                            join mid_feat_key as fe
                              on p.nametyp in ('ON', 'AN', 'BN', '1Q', '8Y') and
                                 p.id      = fe.org_id1                      and
                                 p.feattyp = fe.org_id2
                       left join temp_phoneme as ph
                              on p.feattyp  = ph.featclass  and
                                 p.id       = ph.shapeid    and
                                 p.namelc   = ph.lang       and
                                 p.name     = ph.name
                        ) as t
                  where t.seq = 1  
                  order by feat_key
                    
                 '''
        self.db.do_big_insert( sqlcmd )
       
    
    def _domake_attribute(self):
        # poi street name
        sqlcmd = '''
                   insert into mid_poi_address( key, type, lang, name, tr_lang, tr_name, hno )
                   select fe.feat_key, fe.feat_type, pi.stnamelc, pi.stname, '','',
                          COALESCE( pi.hsnum, '' )
                     from org_pi       as pi
                     join mid_feat_key as fe
                       on pi.stname is not null    and
                          pi.id      = fe.org_id1  and
                          pi.feattyp = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
        sqlcmd = '''
                  insert into mid_poi_attr_value( key, type, attr_type, attr_value )
                     select fe.feat_key, fe.feat_type, 'TL', pi.telnum
                     from org_pi       as pi
                     join mid_feat_key as fe
                       on pi.telnum is not null and pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    union
                     select fe.feat_key, fe.feat_type, 'TX', pi.faxnum
                     from org_pi       as pi
                     join mid_feat_key as fe
                       on pi.faxnum is not null and pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    union
                     select fe.feat_key, fe.feat_type, '8M', pi.email
                     from org_pi       as pi
                     join mid_feat_key as fe
                       on pi.email is not null and pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    union
                     select fe.feat_key, fe.feat_type, '8L', pi.http
                     from org_pi       as pi
                     join mid_feat_key as fe
                       on pi.http is not null and pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_relation(self):
        
        # poi to a8,a9
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select fe.feat_key, fe.feat_type, 7001, f1.feat_key, f1.feat_type
                    from org_sa       as sa
                    join mid_feat_key as fe
                      on sa.aretyp in (1119,1120) and sa.id = fe.org_id1 and sa.feattyp = fe.org_id2
                    join mid_feat_key as f1
                      on sa.areid = f1.org_id1 and sa.aretyp = f1.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
        # poi to postcode
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select fe.feat_key, fe.feat_type, 7004, fz.feat_key, fz.feat_type
                    from org_pi       as pi
                    join mid_feat_key as fe
                      on pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    join temp_postcode as z
                      on pi.postcode = z.org_code 
                    join mid_feat_key  as fz
                      on z.id = fz.org_id1 and z.type = fz.org_id2  
                 '''
        self.db.do_big_insert( sqlcmd )
        
        # poi to link
        sqlcmd = '''
                  insert into mid_feature_to_feature( fkey, ftype, code, tkey, ttype )
                  select fe.feat_key, fe.feat_type, 7002, f1.feat_key, f1.feat_type
                    from org_pi       as pi
                    join mid_feat_key as fe
                      on pi.id = fe.org_id1 and pi.feattyp = fe.org_id2
                    join mid_feat_key as f1
                      on pi.cltrpelid = f1.org_id1 and f1.org_id2 in (4110,4130)
                 '''
        self.db.do_big_insert( sqlcmd )
        
        
    def _domake_name_geom(self): 
        self._gen_nameid( 'poi' )
        self._gen_geomid( 'poi' )
        