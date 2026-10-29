import copy, json, tempfile, unittest
from pathlib import Path
import server

def sample():
 return {'version':1,'books':[{'id':'book_1','title':'Test','language':'English','genre':'Fantasy','style':'','premise':'','world':'','length':1500,'characters':[],'plans':[],'chapters':[{'id':'chapter_1','title':'One','body':'old','number':1,'intent':'','summary':'old summary','summaryBody':'old','status':'review','history':[]}],'memories':[]}]}
def translation():
 return {'title':'English','body':'translation','notes':'','sourceBody':'old','sourceTitle':'One','glossary':'','guide':'','status':'approved','checks':{k:True for k in ('meaning','terms','voice','natural','continuity')},'history':[]}
class StorageTest(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.old_data=server.DATA;self.old_db=server.DB_PATH;server.DATA=Path(self.temp.name);server.DB_PATH=server.DATA/'test.db'
 def tearDown(self):
  self.temp.cleanup();server.DATA=self.old_data;server.DB_PATH=self.old_db
 def test_restart_persistence_and_conflict(self):
  data=sample();self.assertEqual(server.save_state(data,0),1)
  with server.connect() as con:self.assertEqual(con.execute('SELECT revision FROM state').fetchone()[0],1)
  with self.assertRaises(RuntimeError):server.save_state(data,0)
 def test_bad_backup_rejected_without_write(self):
  with self.assertRaises(ValueError):server.save_state({'version':1,'books':[{'id':'a','title':'bad'}]},0)
 def test_unsafe_ids_and_duplicate_chapters_rejected(self):
  for value in ['bad" onclick="x','<img>','',None]:
   data=sample();data['books'][0]['id']=value
   with self.assertRaises(ValueError):server.validate(data)
  data=sample();other=copy.deepcopy(data['books'][0]['chapters'][0]);other['id']='chapter_2';data['books'][0]['chapters'].append(other)
  with self.assertRaises(ValueError):server.validate(data)
 def test_invalid_translation_and_history_rejected(self):
  for key,val in [('history',4),('history',[{'body':42}]),('checks',{'meaning':'true'}),('body',None),('status','live')]:
   data=sample();en=translation();en[key]=val;data['books'][0]['chapters'][0]['english']=en
   with self.assertRaises(ValueError):server.validate(data)
 def test_prototype_keys_and_truthy_memory_rejected(self):
  data=sample();data['books'][0]['__proto__']={}
  with self.assertRaises(ValueError):server.validate(data)
  data=sample();data['books'][0]['memories']=[{'id':'m','title':'T','body':'B','chapter':1,'type':'Sự kiện','confirmed':'false'}]
  with self.assertRaises(ValueError):server.validate(data)
 def test_restore_keeps_previous_data_in_transaction(self):
  data=sample();server.save_state(data,0);server.save_state({'version':1,'books':[]},1,restore=True)
  with server.connect() as con:
   body=con.execute('SELECT body FROM backups').fetchone()[0];self.assertEqual(json.loads(body),data)
   self.assertEqual(con.execute('SELECT revision FROM state').fetchone()[0],2)
 def test_invalid_or_conflicting_restore_never_replaces_data(self):
  data=sample();server.save_state(data,0)
  with self.assertRaises(ValueError):server.save_state({},1,restore=True)
  with self.assertRaises(RuntimeError):server.save_state({'version':1,'books':[]},0,restore=True)
  with server.connect() as con:self.assertEqual(json.loads(con.execute('SELECT body FROM state').fetchone()[0]),data)
 def test_backup_failure_rolls_back_restore(self):
  data=sample();server.save_state(data,0)
  with server.connect() as con:
   con.execute('CREATE TABLE backups (id TEXT PRIMARY KEY,created_at TEXT,revision INTEGER,body TEXT)')
   con.execute("CREATE TRIGGER reject_backup BEFORE INSERT ON backups BEGIN SELECT RAISE(ABORT,'disk failure simulation'); END")
  with self.assertRaises(Exception):server.save_state({'version':1,'books':[]},1,restore=True)
  with server.connect() as con:self.assertEqual(json.loads(con.execute('SELECT body FROM state').fetchone()[0]),data)
 def test_server_invalidates_summary_and_english_on_change(self):
  data=sample();data['books'][0]['chapters'][0]['english']=translation();server.save_state(data,0)
  changed=copy.deepcopy(data);c=changed['books'][0]['chapters'][0];c['body']='rewritten';c['english']['body']='edited translation';server.save_state(changed,1)
  with server.connect() as con:saved=json.loads(con.execute('SELECT body FROM state').fetchone()[0])['books'][0]['chapters'][0]
  self.assertEqual(saved['summary'],'');self.assertEqual(saved['english']['status'],'review');self.assertEqual(saved['english']['checks'],{})
if __name__=='__main__':unittest.main()
