import common.logger

class CFeature(object):

    def __init__(self, name='feature'):
        self.db     = None
        self.name   = name
        self.logger = common.logger.sub_log( self.name )
        self.logger.info('init')
   
    def attach_db(self, database, vendor=''):
        self.db = database
        self.vendor = vendor
        
    def run(self):
        self.make_key()
        self.make_feature()
        self.make_attribute()
        self.make_relation()
            
    def make_key(self):
        self.logger.info('make key')
        self._domake_key()
        
    def make_feature(self):
        self.logger.info('make feature')
        self._domake_feature()
    
    def make_geomtry(self):
        self.logger.info('make geomtry')
        self._domake_geomtry()
        
    def make_name(self):
        self.logger.info('make name')
        self._domake_name()
    
    def make_attribute(self):
        self.logger.info('make attribute')
        self._domake_attribute()
        
    def make_relation(self):
        self.logger.info('make relation')
        self._domake_relation()
        
    def gen_name_geom(self):
        self._domake_name_geom()
        pass
                
    def _domake_key(self):
        pass
        
    def _domake_feature(self):
        pass
    
    def _domake_geomtry(self):
        pass
        
    def _domake_name(self):
        pass
    
    def _domake_name_geom(self):
        pass
    
    def _domake_attribute(self):
        pass
        
    def _domake_relation(self):
        pass
    
    def _domake_common_category(self):
        sqlcmd = '''
                 insert into mid_poi_category(per_code, gen1, gen2, gen3, level, imp, name, tr_name)
                 select per_code, gen1, gen2, gen3, level, imp, name, tr_name
                   from temp_org_category
                   order by level, case level 
                                      when 1 then  0
                                      when 2 then  gen1
                                      else   (gen1<<8) + gen2
                                    end,
                              name
                 '''
        self.db.do_big_insert( sqlcmd )
        
    def _domake_common_postcode(self):
        sqlcmd = '''
                 insert into mid_postcode( key, type, sub, pocode )
                 select f.feat_key, f.feat_type, 
                        case p.type
                          when 3136 then 0
                          else 1
                        end, p.org_code
                   from temp_postcode as p
                   join mid_feat_key  as f
                     on p.id = f.org_id1 and p.type = f.org_id2
                 '''
        self.db.do_big_insert( sqlcmd )
            
    def _gen_nameid( self, feat = None ):
        if not feat:
            return 0
        
        self.logger.info('generate %s name id' % feat) 
       
        sqlcmd = '''
                   insert into temp_<f>_name_gen_id( gid, key, grp, namesetid, nameid )
                   with t 
                    as  (
                           select gid, key, grp, dense_rank() over ( order by <order> ) as nameid
                             from temp_<f>_name
                        )
                    select t.gid, t.key, t.grp, t3.setid, t.nameid
                      from t
                      join (
                            select distinct key, grp, dense_rank() over ( order by nameset ) as setid
                              from (
                                     select key, grp, array_agg( nameid ) as nameset
                                       from ( select * from t order by key, grp, nameid ) as t1
                                      group by key, grp
                                   ) t2
                            ) as t3
                         on t.key = t3.key and t.grp = t3.grp
                 '''  
        
        if feat == 'street':
            # gen id according to name, we will adjust the tr_name to same spelling.
            sqlcmd = sqlcmd.replace( '<order>', 'langcode, (name)::bytea' )
        else:
            sqlcmd = sqlcmd.replace( '<order>', 'langcode, (name)::bytea, tr_lang, tr_name' )
            
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
        
        sqlcmd = '''
                   insert into mid_<f>_name( id, langcode, name, tr_lang, tr_name, ph_lang, ph_name )
                   with p as (
                   select distinct nameid, langcode, name, tr_lang, tr_name, ph_lang, ph_name, 
                          count( tr_name ) over ( partition by nameid, tr_name ) as cnt
                     from temp_<f>_name         as n
                     join temp_<f>_name_gen_id  as g
                       on n.gid = g.gid
                    )
                   select t1.*, t2.ph_lang, t2.ph_name
                     from (
                            select nameid, langcode, name, tr_lang, tr_name 
                             from (
                                   select nameid, langcode, name, tr_lang, tr_name,
                                          row_number() over ( partition by nameid order by cnt desc, tr_name desc ) as seq
                                     from p
                                   ) as t
                            where seq = 1
                          ) as t1
                     join (
                            select nameid, ph_lang, ph_name
                             from (
                                   select nameid, ph_lang, ph_name,
                                          row_number() over ( partition by nameid order by ph_name desc ) as seq
                                     from p
                                  ) as t
                            where seq = 1

                          ) as t2
                       on t1.nameid = t2.nameid
                    order by nameid
                 ''' 
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
        
        sqlcmd = '''
                   insert into mid_<f>_nameset( id, nameid)
                   select distinct  namesetid, nameid
                     from temp_<f>_name         as n
                     join temp_<f>_name_gen_id  as g
                       on n.gid = g.gid
                 '''
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
        
        sqlcmd = '''
                   insert into mid_<f>_to_name( key, type, nametype, namesetid)
                   select distinct n.key, n.type, nametype, namesetid
                     from temp_<f>_name         as n
                     join temp_<f>_name_gen_id  as g
                       on n.gid = g.gid
                    order by n.key
                 '''
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
    
    def _gen_geomid(self,feat = None):
        if not feat:
            return 0
        
        self.logger.info('generate %s geometry id'%feat)
        sqlcmd = '''
                   insert into temp_<f>_geom_gen_id( gid, geomid )
                   select gid, dense_rank() over (order by geotype, geom ) 
                     from temp_<f>_geom
                 '''
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
        
        # when geom is so close,the geomid will be same, so ,we need select only one geom in that case.
        sqlcmd = '''
                   insert into mid_<f>_geometry( id, type, geom)
                   select geomid, geotype, geom
                     from (
                           select geomid, geotype, geom, row_number() over ( partition by geomid ) as seq
                             from temp_<f>_geom         as e
                             join temp_<f>_geom_gen_id  as g
                               on e.gid = g.gid
                          ) as t
                     where seq = 1
                 '''
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
        
        sqlcmd = '''
                   insert into mid_<f>_to_geometry( key, type, code, geomid)
                   select key, type, code, geomid
                     from temp_<f>_geom         as e
                     join temp_<f>_geom_gen_id  as g
                       on e.gid = g.gid
                    order by key
                 '''
        self.db.do_big_insert( sqlcmd.replace( '<f>', feat ) )
        
class CWork(object):
    def __init__(self, name='work'):
        self.logger = common.logger.sub_log( name )
        
    def attach_db(self, database,vendor):
        self.db   = database
        self.name = vendor
        
    def do(self):
        pass
              
        
       
        

        
        
        