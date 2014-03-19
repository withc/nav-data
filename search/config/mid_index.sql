CREATE INDEX mid_feature_to_feature_fkey
  ON mid_feature_to_feature
  USING btree
  (fkey);

CREATE INDEX mid_feature_to_feature_tkey
  ON mid_feature_to_feature
  USING btree
  (tkey);
  
CREATE INDEX mid_feature_to_name_key
  ON mid_feature_to_name
  USING btree
  (key);

CREATE INDEX mid_feature_to_geometry_key
  ON mid_feature_to_geometry
  USING btree
  (key); 
  
CREATE INDEX mid_house_number_road_id
  ON mid_house_number_road
  USING btree
  (id);

CREATE INDEX mid_house_number_road_key
  ON mid_house_number_road
  USING btree
  (key);
    
CREATE INDEX mid_address_range_id
  ON mid_address_range
  USING btree
  (id); 
  
CREATE INDEX mid_address_point_id
  ON mid_address_point
  USING btree
  (id);  