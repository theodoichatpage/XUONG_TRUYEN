import tempfile, unittest
from pathlib import Path
import server
class StorageTest(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();server.DATA=Path(self.temp.name);server.DB_PATH=server.DATA/'test.db'
 def tearDown(self): self.temp.cleanup()
 def test_restart_persistence_and_conflict(self):
  data={'version':1,'books':[]};self.assertEqual(server.save_state(data,0),1)
  with server.connect() as con: self.assertEqual(con.execute('SELECT revision FROM state').fetchone()[0],1)
  with self.assertRaises(RuntimeError): server.save_state(data,0)
 def test_bad_backup_rejected_without_write(self):
  with self.assertRaises(ValueError): server.save_state({'version':1,'books':[{'id':'a','title':'bad'}]},0)
if __name__=='__main__':unittest.main()
