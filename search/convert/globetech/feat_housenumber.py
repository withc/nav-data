import convert.feature

class CHouseNumber(convert.feature.CFeature):
    def __init__(self ):
        convert.feature.CFeature.__init__(self, 'house_num')
 
    def _domake_key(self):
        sqlcmd = '''
                 insert into temp_address_point( id, pkey, ptype, lang, name, hno, x, y )
                 select dense_rank() over ( order by feat_key,  feat_type, languageco, (fullname)::bytea ), *
                   from (
                         select f.feat_key, f.feat_type, p.languageco, p.fullname, 
                                p.hno, x, y
                           from (
                                  select hno, prov_code, amp_code, tam_code, fullname, languageco, 
                                        (st_x(the_geom)*100000)::int as x, 
                                        (st_y(the_geom)*100000)::int as y
                                    from org_pointaddress_1 
                                   where fullname is not null
                                  union
                                  select hno, prov_code, amp_code, tam_code, fullname, languageco,
                                         (st_x(the_geom)*100000)::int as x, 
                                         (st_y(the_geom)*100000)::int as y
                                    from org_pointaddress_2 
                                   where fullname is not null
                                )  as p
                           join temp_admincode        as a
                             on p.prov_code = a.prov_code  and
                                p.amp_code  = a.amp_code   and
                                p.tam_code  = a.tam_code   and
                                a.type = 3
                           join mid_feat_key          as f
                             on a.org_id1 = f.org_id1 and a.org_id2 = f.org_id2
                        ) as t
                 '''
        self.db.do_big_insert( sqlcmd )
    
    def _domake_feature(self):
        sqlcmd = '''
                 insert into mid_place_road( id, pkey, ptype, lang, name )
                 select distinct id, pkey, ptype, 
                        case lang 
                          when 'THE' then 'ENG'
                          else lang
                        end, name
                   from temp_address_point
                 '''
        self.db.do_big_insert( sqlcmd )

    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        self._make_hn_by_link()
        self._make_hn_by_point()
        
    def _domake_relation(self):
        pass
    
    def _make_hn_by_link(self):
        pass

    def _make_hn_by_point(self):
        sqlcmd = '''
                insert into mid_address_point( id, side, num, x, y, entry_x, entry_y )
                select id, 1, hno, x, y, 0, 0
                  from temp_address_point
                '''
        self.db.do_big_insert( sqlcmd )
        