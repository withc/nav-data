import entity

class CPlace(entity.CEntity):
    def __init__(self, database ):
        entity.CEntity.__init__(self, database, 'place')
          
    def _do(self):
        self._make_name_id()
        self._make_a0()
        self._make_a1()
        
    def _make_name_id(self):
        sqlcmd = '''
                 insert into tmp_place_name_id( name_id, key, type )
                 select row_number() over( order by langcode, name), id, 5001
                   from (
                           select distinct id, langcode, name
                             from mid_name as n
                            where exists (
                                   select nameid 
                                     from mid_feature_to_name  as f
                                    where f.nameid = n.id and  ( f.type between 3001 and 3110 )
                                  )
                           ) as t
                 '''
        self.db.do_big_insert(sqlcmd)
        
        sqlcmd = '''
                 insert into rdb_place_name( id, lang, name )
                 select ni.name_id, n.langcode, n.name
                   from tmp_place_name_id as ni
                   join mid_name          as n
                     on ni.key = n.id
                 '''
        self.db.do_big_insert(sqlcmd)
    
    def _make_a0(self):
        sqlcmd = '''
                 insert into tmp_place_id( place_id, key, type )
                 select row_number() over (order by nid), key, type
                   from (
                       select p.key, p.type,  min(n.name_id) as nid
                         from mid_place           as p
                         join mid_feature_to_name as f
                           on p.type = 3001 and p.key = f.key and f.nametype = 'ON'
                         join tmp_place_name_id   as n
                           on f.nameid = n.key
                        group by p.key, p.type
                        ) as t
                 '''
        self.db.do_big_insert(sqlcmd)
        
    def _make_a1(self):
        sqlcmd = '''
                 insert into tmp_place_id( place_id, key, type )
                 select ( select max(place_id) from tmp_place_id ) + row_number() over (order by nid), 
                        key, type
                   from (
                       select p.key, p.type, a0.place_id,  min(n.name_id) as nid
                         from mid_place_admin     as p
                         join mid_feature_to_name as f
                           on p.type = 3002 and p.key = f.key and f.nametype = 'ON'
                         join tmp_place_name_id   as n
                           on f.nameid = n.key
                         join tmp_place_id        as a0
                           on p.a0 = a0.key
                        group by p.key, p.type, a0.place_id
                        ) as t
                 '''
        self.db.do_big_insert(sqlcmd)
        
        
        
        
        
        
        
        
        