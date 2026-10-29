import copy, unittest, json, subprocess
import server
from test_storage import sample
import test_storage as fixtures

def writing():return {'id':'xt_test','bookId':'book_1','chapterId':'chapter_1','mode':'write','prompt':'Write','baseChapter':'{}','createdAt':'now','status':'queued','resultText':''}
class JobValidationTest(unittest.TestCase):
 def test_durable_job_is_valid_and_wrong_types_rejected(self):
  d=sample();d['aiJobs']=[writing()];server.validate(d)
  for key,value in [('id','bad'),('mode','image'),('status','approved'),('resultText',12),('prompt','x'*150001)]:
   bad=copy.deepcopy(d);bad['aiJobs'][0][key]=value
   with self.assertRaises(ValueError):server.validate(bad)
 def test_browser_translation_checkpoint_can_be_stored(self):
  # Generate an actual unfilled browser checkpoint, not a manually mirrored schema.
  script="""const B=require('./web/bridge-core.js'),T=require('./web/translation.js');const data=JSON.parse(process.argv[1]),b=data.books[0],c=b.chapters[0];c.status='approved';const draft=T.create(b,c,'en'),en={bookId:b.id,chapterId:c.id,target:'en',mode:'translate',index:0,draft,baseTranslation:'null'};data.aiJobs=[B.prepare(data,null,en,T.prompt(b,c,draft,0),'xt_translate')];process.stdout.write(JSON.stringify(data));"""
  d=sample();d['books'][0]['language']='Tiếng Việt';result=subprocess.check_output(['node','-e',script,json.dumps(d)]);server.validate(json.loads(result))
class JobStorageTest(unittest.TestCase):
 setUp=fixtures.StorageTest.setUp
 tearDown=fixtures.StorageTest.tearDown
 def test_received_job_survives_storage_reload(self):
  d=sample();d['aiJobs']=[writing()];server.save_state(d,0);d['aiJobs'][0]['status']='ready';d['aiJobs'][0]['resultText']='Received text';server.save_state(d,1)
  with server.connect() as con:saved=json.loads(con.execute('SELECT body FROM state').fetchone()[0])
  self.assertEqual(saved['aiJobs'][0]['resultText'],'Received text');self.assertEqual(saved['aiJobs'][0]['status'],'ready')
if __name__=='__main__':unittest.main()
