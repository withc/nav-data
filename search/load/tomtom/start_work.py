import load.common_work

class CStartWork(load.common_work.CStartProcess):
    def __init__(self ):
        load.common_work.CStartProcess.__init__(self)
        
    def _do_my(self):
        sqlcmd = '''
          insert into temp_phoneme( featclass, shapeid, nametype, lang, name, normname, ptid, ph_lang, ph_name )
          select distinct f.featclass, f.shapeid, nf.nametype, n.langcode, n.name, n.normname, p.ptid, p.lanphonset, p.transcription 
            from org_vm_foa   as f
            join org_vm_nefa  as nf
              on f.featdsetid  = nf.featdsetid   and
                 f.featsectid  = nf.featsectid   and
                 f.featlayerid = nf.featlayerid  and
                 f.featitemid  = nf.featitemid
            join org_vm_ne    as n
              on nf.nameitemid = n.nameitemid  and
                 nf.featdsetid = n.namedsetid  and
                 nf.featsectid = n.namesectid
            join (
                  SELECT distinct ptid, pt_label, alphabet, transcription, lanphonset, preference, lanpron
                    FROM org_vm_pt  where preference = 1
                 )  as p
              on n.ptid = p.ptid
                 '''
        self.db.do_big_insert( sqlcmd )
        sqlcmd = '''
                  CREATE INDEX idx_temp_phoneme_key
                  ON temp_phoneme
                  USING btree
                  (featclass, shapeid, lang, name);
                  '''
        self.db.execute( sqlcmd )
        self.db.analyze( 'temp_phoneme' )
        
        
        
        
        
        
        