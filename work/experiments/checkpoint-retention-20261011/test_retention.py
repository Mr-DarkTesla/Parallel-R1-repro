import importlib.util,json,pathlib,tempfile,unittest
p=pathlib.Path(__file__).parent/'runner/checkpoint_retention.py'
s=importlib.util.spec_from_file_location('retention',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class RetentionTests(unittest.TestCase):
 def ckpt(self,root,step,managed=True,complete=True):
  p=root/f'checkpoint-{step:04}';(p/'hf').mkdir(parents=True)
  (p/'hf/config.json').write_text('{}');(p/'hf/model.safetensors').write_bytes(b'weights')
  (p/'optimizer-rank-0.pt').write_bytes(b'adam');(p/'rng-0.pt').write_bytes(b'rng')
  if complete:(p/'complete.json').write_text(json.dumps(dict(step=step,world_size=1,model=True,optimizer=True,rng=True,retention_managed=managed)))
  return p
 def test_leases_anchors_resume_history_and_unmanaged(self):
  with tempfile.TemporaryDirectory() as td:
   r=pathlib.Path(td)
   for step in (4,8,16,32,64,128):self.ckpt(r,step)
   self.ckpt(r,2,managed=False);self.ckpt(r,144,complete=False)
   m.pin(r,16,'queued-math');m.pin(r,64,'resume-candidate')
   removed=m.prune(r,keep_steps=[32,128,256,500],keep_count=1)
   self.assertEqual([x['step'] for x in removed],[4,8])
   self.assertTrue((r/'checkpoint-history/checkpoint-0004.json').is_file())
   self.assertTrue(all((r/f'checkpoint-{x:04}').exists() for x in (2,16,32,64,128,144)))
   m.release(r,16,'queued-math');m.release(r,64,'resume-candidate')
   self.assertEqual([x['step'] for x in m.prune(r,keep_steps=[32,128],keep_count=1)],[16,64])
 def test_newest_complete_independent_of_incomplete(self):
  with tempfile.TemporaryDirectory() as td:
   r=pathlib.Path(td);self.ckpt(r,16);self.ckpt(r,32);self.ckpt(r,64,complete=False)
   self.assertEqual([x['step'] for x in m.prune(r,keep_steps=[],keep_count=1)],[16])
   self.assertTrue((r/'checkpoint-0032').exists())
 def test_fail_closed_registry(self):
  with tempfile.TemporaryDirectory() as td:
   r=pathlib.Path(td);self.ckpt(r,4);self.ckpt(r,8)
   (r/'artifact-leases.json').write_text('{"leases":{"4":{"bad":{"state":"unknown"}}}}')
   with self.assertRaises(ValueError):m.prune(r,keep_steps=[])
   self.assertTrue((r/'checkpoint-0004').exists())
 def test_save_schedule_and_zero_keep_rejected(self):
  self.assertFalse(m.should_save(4,500,{}));self.assertFalse(m.should_save(8,500,{}))
  self.assertTrue(all(m.should_save(s,500,{}) for s in (16,32,128,256,500)))
  with self.assertRaises(ValueError):m.should_save(1,500,{'keep_count':0})
if __name__=='__main__':unittest.main()
