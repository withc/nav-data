
def sql_all_name( tbl, id, feat ):
    sql = '''
              join rdf_<f>_name        as n
                on <in>.<id> = n.<id>
         left join rdf_<f>_name_trans  as tr
                on <in>.<id> = tr.<id>
         left join vce_<f>_name        as vc
                on <in>.<id> = vc.<id> and
                   vc.preferred = 'Y'
         left join vce_phonetic_text   as  ph
                on vc.phonetic_id = ph.phonetic_id
         '''
    sql = sql.replace( '<in>', tbl)
    sql = sql.replace( '<id>', id)
    sql = sql.replace( '<f>',  feat)
    return sql