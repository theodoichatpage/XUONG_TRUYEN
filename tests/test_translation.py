import copy,json,unittest
from pathlib import Path
import server,translation_data
import test_storage as fixtures
CASES=json.loads((Path(__file__).parent/'translation-fixtures.json').read_text())
class TranslationValidationTest(unittest.TestCase):
 def test_six_direction_browser_fixtures_match_server(self):
  for data in CASES:
   server.validate(data);b=data['books'][0];target=b['translationConfig']['targetLang'];t=b['chapters'][0]['translations'][target]
   self.assertEqual(t['settings'],translation_data.settings(b,target));self.assertTrue(translation_data.eligible(t))
 def test_missing_duplicate_or_changed_source_segments_rejected(self):
  for op in ('remove','duplicate','source','body'):
   data=copy.deepcopy(CASES[0]);t=next(iter(data['books'][0]['chapters'][0]['translations'].values()))
   if op=='remove':t['segments'].pop()
   if op=='duplicate':t['segments'][1]['id']=t['segments'][0]['id']
   if op=='source':t['segments'][0]['source']='wrong source'
   if op=='body':t['body']='not aligned'
   with self.assertRaises(ValueError):server.validate(data)
 def test_approval_requires_current_reviews_and_all_checks(self):
  for op in ('reviews','checks','stale'):
   data=copy.deepcopy(CASES[0]);t=next(iter(data['books'][0]['chapters'][0]['translations'].values()))
   if op=='reviews':t['reviews']=[]
   if op=='checks':t['checks']={}
   if op=='stale':t['reviews'][0]['basis']['title']='older title'
   with self.assertRaises(ValueError):server.validate(data)
 def test_report_issue_requires_explicit_resolution(self):
  data=copy.deepcopy(CASES[0]);t=next(iter(data['books'][0]['chapters'][0]['translations'].values()))
  x={'id':'i0','pid':'p0001','severity':'major','explanation':'Check meaning','suggestion':'Correction','resolved':False,'resolution':''};t['reviews'][0]['issues']=[x]
  with self.assertRaises(ValueError):server.validate(data)
  x['resolved']=True
  with self.assertRaises(ValueError):server.validate(data)
  x['resolution']='Checked against source';server.validate(data)
 def test_duplicate_terms_and_same_language_config_rejected(self):
  data=copy.deepcopy(CASES[0]);cfg=data['books'][0]['translationConfig'];cfg['targetLang']=cfg['sourceLang']
  with self.assertRaises(ValueError):server.validate(data)
  cfg['targetLang']='zh';term={'sourceLang':'en','targetLang':'zh','source':'Lan','target':'兰','note':''};cfg['terms']=[term,term.copy()]
  with self.assertRaises(ValueError):server.validate(data)
 def test_emoji_batch_length_matches_browser_character_count(self):
  segments=[{'source':'😀'*3500},{'source':'😀'*2000},{'source':'word'*200}]
  self.assertEqual([len(x) for x in translation_data.batches(segments)],[2,1])
class TranslationSaveTest(unittest.TestCase):
 setUp=fixtures.StorageTest.setUp
 tearDown=fixtures.StorageTest.tearDown
 def test_edit_after_review_invalidates_approval_server_side(self):
  data=copy.deepcopy(CASES[0]);server.save_state(data,0);t=next(iter(data['books'][0]['chapters'][0]['translations'].values()));t['status']='review';t['segments'][0]['target']='Changed';t['body']='\n\n'.join(s['target'] for s in t['segments']);server.save_state(data,1)
  self.assertEqual(t['checks'],{});self.assertEqual(t['reviews'],[]);self.assertEqual(t['status'],'review')
if __name__=='__main__':unittest.main()
