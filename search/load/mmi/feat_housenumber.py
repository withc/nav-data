import load.feature

class CHouseNumber(load.feature.CFeature):
    def __init__(self ):
        load.feature.CFeature.__init__(self, 'house_num')
 
    def _domake_key(self):
        pass
    
    def _domake_feature(self):
        sqlcmd = '''
                 insert into mid_bldg_point( id, pkey, ptype, lkey, ltype, side, num, x, y, entry_x, entry_y )
                 select row_number() over (order by  b.stt_id, b.city_id, b.loc_id ),
                       fp.feat_key, fp.feat_type, fl.feat_key, fl.feat_type, 
                        case b.edge_side
                           when 'L' then 1
                           when 'R' then 2
                        end, b.bldg_num, b.lon*100000, b.lat*100000, b.lon_1*100000, b.lat_1*100000
                   from (
                           select bldg_num, stt_id, city_id, loc_id, edge_id, edge_side, lon, lat, lon_1, lat_1
                             from org_bldg_numeric_point where bldg_num is not null
                           union all
                           select bldg_num, stt_id, city_id, loc_id, edge_id, edge_side, lon, lat, lon_1, lat_1
                             from org_bldg_alphanumeric_point where bldg_num is not null
                           order by stt_id, city_id, loc_id, bldg_num
                        ) as b
                   join temp_admincode          as a
                     on b.loc_id = a.id and b.city_id::int = a.parent_id::int
                   join mid_feat_key            as fp
                     on a.org_id1 = fp.org_id1 and a.org_id2 = fp.org_id2
                   join mid_feat_key            as fl
                     on b.edge_id = fl.org_id1 and 4110 = fl.org_id2
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
        pass
        