
def sql_all_name( tbl, feat ):
    sql = '''
              join rdf_<f>_name        as n
                on <i>.name_id = n.name_id
         left join rdf_<f>_name_trans  as tr
                on ns.name_id = tr.name_id
         left join vce_<f>_name        as vc
                on ns.name_id = vc.name_id and
                   ph.preferred = 'Y'
              join vce_phonetic_text       as  ph
                on vc.phonetic_id = ph.phonetic_id
         '''
    sql = sql.replace('<i>', tbl)
    sql = sql.replace( '<f>', feat)
    return sql