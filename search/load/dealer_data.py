import load.feature

class CDealerData(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'dealer data')
 
    def _domake_key(self):
        fp = open(r'.\config\dealer_sgp_idn_20140416.txt','r')
        for line in fp:
            line = line.strip()
            if line[0] == '#':
                continue
            fields = line.split(';')
            vals = fields[0:9]
            if not vals[7] :
                vals[7] = 0
            if not vals[8]:
                vals[8] = 0
                
            sqlcmd = '''
                      insert into temp_dealer values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                     '''
            self.db.execute( sqlcmd, vals )
        self.db.commit()
        fp.close()
       
    def _domake_feature(self):
        if self.vendor == 'globetech' :
            sqlcmd = '''
                     insert into mid_poi_dealer( id, iso, lang, name, tr_name, postcode, 
                                             full_addr, tr_addr, tel, 
                                             x, y, entry_x, entry_y )
                     select t.gid, 'THA', 'THA',
                            case 
                               when branch_t is not null then nav_namt||' '||branch_t
                               else nav_namt
                            end,
                            case 
                              when branch_e is not null then nav_name||' '||branch_e
                              else nav_name
                            end, 
                            postcode,
                            address_t||', '||t, 
                            address_e||', '||e, 
                            tel, st_x(the_geom), st_y(the_geom), 0, 0
                       from  org_toyota as t
                       join (
                               select distinct prov_code,amp_code,tam_code, 
                                      tam_namt || ', ' || amp_namt || ', ' || prov_namt as t,
                                      tam_name || ', ' || amp_name || ', ' || prov_name as e  
                                 from org_admin_poly   
                            ) as a
                         on t.prov_code = a.prov_code and
                            t.amp_code  = a.amp_code  and
                            t.tam_code  = a.tam_code
                     '''
            self.db.do_big_insert( sqlcmd )
        else:
            sqlcmd = '''
                 insert into mid_poi_dealer( id, iso, lang, name, tr_name, postcode, 
                                             full_addr, tr_addr, tel, 
                                             x, y, entry_x, entry_y )
                 select d.id, d.iso, d.lang, d.name, '', d.postcode, d.full_addr, '', d.tel, 
                        x, y, entry_x, entry_y
                   from temp_dealer          as d
                   join mid_country_profile  as c
                     on d.iso = c.iso
                 '''
            self.db.do_big_insert( sqlcmd )
    
    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass