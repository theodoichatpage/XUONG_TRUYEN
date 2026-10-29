import copy, unittest, json
import server
import test_storage as fixtures
from test_storage import sample

def planned():
 d=sample();d['books'][0]['plans']=[
 {'id':'v','title':'V','body':'','kind':'volume','parentId':'','startChapter':1,'endChapter':20,'order':0},
 {'id':'a','title':'A','body':'','kind':'arc','parentId':'v','startChapter':1,'endChapter':10,'order':0},
 {'id':'p','title':'P','body':'','kind':'chapter','parentId':'a','startChapter':1,'endChapter':1,'order':0},
 {'id':'s','title':'S','body':'','kind':'scene','parentId':'p','startChapter':1,'endChapter':1,'order':1}]
 d['books'][0]['chapters'][0]['planId']='p';return d
class StructureTest(unittest.TestCase):
 def test_valid_tree_and_legacy_data(self):
  server.validate(planned());d=sample();d['books'][0]['plans']=[{'id':'old','title':'Old','body':'legacy note'}];server.validate(d)
 def test_wrong_parent_and_cycles_rejected(self):
  for index,parent in [(1,'missing'),(0,'s'),(2,'v'),(3,'s')]:
   d=planned();d['books'][0]['plans'][index]['parentId']=parent
   with self.assertRaises(ValueError):server.validate(d)
 def test_outside_parent_range_and_wrong_chapter_link_rejected(self):
  d=planned();d['books'][0]['plans'][1]['endChapter']=30
  with self.assertRaises(ValueError):server.validate(d)
  for value in ['s','missing','v']:
   d=planned();d['books'][0]['chapters'][0]['planId']=value
   with self.assertRaises(ValueError):server.validate(d)
  d=planned();d['books'][0]['chapters'][0]['number']=2
  with self.assertRaises(ValueError):server.validate(d)
 def test_resolved_threads_require_chapter_and_explanation(self):
  d=sample();m={'id':'m','title':'Key','body':'Missing','chapter':2,'confirmed':True,'type':'Nút thắt','threadStatus':'resolved','dueChapter':5,'resolvedChapter':4,'resolution':'Found'};d['books'][0]['memories']=[m];server.validate(d)
  for key,value in [('resolvedChapter',0),('resolution',''),('dueChapter',1),('threadStatus','fake')]:
   bad=copy.deepcopy(d);bad['books'][0]['memories'][0][key]=value
   with self.assertRaises(ValueError):server.validate(bad)
class SummaryVersionTest(unittest.TestCase):
 setUp=fixtures.StorageTest.setUp
 tearDown=fixtures.StorageTest.tearDown
 # Inherit isolated temporary database setup; only new tests are reported here.
 def test_body_revision_changes_only_with_body_and_invalidates_stale_summary(self):
  d=sample();c=d['books'][0]['chapters'][0];c['summaryRevision']=1;server.save_state(d,0)
  self.assertEqual(c['bodyRevision'],1);self.assertEqual(c['summaryRevision'],1)
  c['intent']='metadata edit';server.save_state(d,1);self.assertEqual(c['bodyRevision'],1)
  c['body']='new';server.save_state(d,2);self.assertEqual(c['bodyRevision'],2);self.assertEqual(c['summaryRevision'],0)
  c['summary']='new summary';c['summaryBody']='new';c['summaryRevision']=2;server.save_state(d,3);self.assertEqual(c['summaryRevision'],2)
if __name__=='__main__':unittest.main()
