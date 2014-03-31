import entity

class CVoiceData(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'voice_data')
          
    def _do(self):
        self.db.run( r'.\config\voice_db.sql' )
        self._do_temp_table()
        self._do_table()
        
    def _do_temp_table(self):
        sqlcmd = '''
                 insert into voice_tmp_full_place( level, area0, area1, area2, area3, country, state, city, district )
                 with an (level, area0, area1, area2, area3, type, lang, name )
                  as (
                       select * from tbl_city_name
                       where lang in ( select off_lang from mid_country_profile )
                     )
                 select a.level, a.area0, a.area1, a.area2, a.area3, a0.name, a1.name, a2.name, a3.name
                   from tbl_city_info as a
                   join an as a0
                     on a.area0 = a0.area0 and 
                        a0.level = 0  
              left join an as a1
                     on a.area0 = a1.area0 and 
                        a.area1 = a1.area1 and 
                        a1.level = 1  
              left join an as a2
                     on a.area0 = a2.area0 and
                        a.area1 = a2.area1 and
                        a.area2 = a2.area2 and
                        a2.level = 2  
              left join an as a3
                     on a.area0 = a3.area0 and
                        a.area1 = a3.area1 and
                        a.area2 = a3.area2 and
                        a.area3 = a3.area3 and
                        a3.level = 3  
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _do_table(self):
        sqlcmd = '''
                 insert into voice_state( country_id, state_id, country, state )
                 select area0, area1, country, state
                   from voice_tmp_full_place
                  where level = 1
                 '''
        self.db.do_big_insert(sqlcmd)
        
        sqlcmd = '''
                 insert into voice_poi( country_id, state_id, poi_id, gen_code, country, state, city, district, poi_name, poi_phonetic )
                 select p.area0, p.area1, p.id, (p.gen1<<24)+(p.gen2<<16)+p.gen3,
                        t.country, t.state, t.city, t.district, pn.name, ''
                   from tbl_poi_info         as p
                   join tbl_poi_name         as pn
                     on p.id = pn.id
                   join voice_tmp_full_place as t
                     on p.area0 = t.area0  and
                        p.area1 = t.area1  and
                        p.area2 = t.area2  and
                        p.area3 = t.area3
                 '''
        self.db.do_big_insert(sqlcmd)
        
        sqlcmd = '''
                 insert into voice_street( country_id, state_id, country, state, city, district, name_type, street_name, street_phonetic )
                 select s.area0, s.area1,
                        t.country, t.state, t.city, t.district, 
                        n.type, n.name, ''
                   from tbl_street_info as s
                   join tbl_street_name as n
                     on s.id = n.id
                   join voice_tmp_full_place as t
                     on s.area0 = t.area0  and
                        s.area1 = t.area1  and
                        s.area2 = t.area2  and
                        s.area3 = t.area3
                 '''
        self.db.do_big_insert(sqlcmd)
        
        sqlcmd = '''
                 insert into voice_street_hno_rang( country_id, state_id, country, state, city, district, 
                                                    name_type, street_name, street_phonetic,
                                                    scheme, f_hno, l_hno )
                 select s.area0, s.area1, t.country, t.state, t.city, t.district, 
                        n.type, n.name, '', h.scheme, h.f_hno, h.l_hno
                   from tbl_street_hno_range as h
                   join tbl_street_info      as s
                     on h.id = s.id
                   join tbl_street_name      as n
                     on s.id = n.id
                   join voice_tmp_full_place as t
                     on s.area0 = t.area0  and
                        s.area1 = t.area1  and
                        s.area2 = t.area2  and
                        s.area3 = t.area3
                 '''
        self.db.do_big_insert(sqlcmd)
        
        sqlcmd = '''
                  insert into voice_street_hno_point( country_id, state_id, country, state, city, district, 
                                                    name_type, street_name, street_phonetic, hno )
                 select s.area0, s.area1, t.country, t.state, t.city, t.district, 
                        n.type, n.name, '', h.hno
                   from tbl_street_hno_point as h
                   join tbl_street_info      as s
                     on h.id = s.id
                   join tbl_street_name      as n
                     on s.id = n.id
                   join voice_tmp_full_place as t
                     on s.area0 = t.area0  and
                        s.area1 = t.area1  and
                        s.area2 = t.area2  and
                        s.area3 = t.area3
                 '''
        self.db.do_big_insert(sqlcmd)       
        