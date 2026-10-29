import json, tempfile, threading, unittest, urllib.request, urllib.error
from pathlib import Path
from http.server import ThreadingHTTPServer
import server

class HTTPTest(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.old=(server.DATA,server.DB_PATH,server.PORT)
  server.DATA=Path(self.temp.name);server.DB_PATH=server.DATA/'state.db'
  self.http=ThreadingHTTPServer(('127.0.0.1',0),server.Handler);server.PORT=self.http.server_port
  self.url='http://127.0.0.1:'+str(server.PORT);self.thread=threading.Thread(target=self.http.serve_forever,daemon=True);self.thread.start()
 def tearDown(self):
  self.http.shutdown();self.http.server_close();self.thread.join();server.DATA,server.DB_PATH,server.PORT=self.old;self.temp.cleanup()
 def get(self,path):return json.load(urllib.request.urlopen(self.url+path))
 def post(self,path,data,token=server.TOKEN):
  req=urllib.request.Request(self.url+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json','X-Xuong-Token':token})
  return json.load(urllib.request.urlopen(req))
 def test_restore_endpoint_creates_downloadable_previous_snapshot(self):
  original=self.get('/api/state');self.assertEqual(original['revision'],0)
  result=self.post('/api/restore',{'data':{'version':1,'books':[]},'revision':0});self.assertEqual(result['revision'],1)
  items=self.get('/api/backups')['backups'];self.assertEqual(len(items),1)
  backup=self.get('/api/backups/'+items[0]['id']);self.assertEqual(backup['data'],original['data'])
  with self.assertRaises(urllib.error.HTTPError) as error:self.post('/api/restore',{'data':original['data'],'revision':0})
  self.assertEqual(error.exception.code,409);self.assertEqual(len(self.get('/api/backups')['backups']),1)
 def test_unauthorized_and_invalid_restore_are_rejected(self):
  with self.assertRaises(urllib.error.HTTPError) as error:self.post('/api/restore',{'data':{'version':1,'books':[]},'revision':0},token='wrong')
  self.assertEqual(error.exception.code,403)
  with self.assertRaises(urllib.error.HTTPError) as error:self.post('/api/restore',{'data':{'version':1,'books':[{}]},'revision':0})
  self.assertEqual(error.exception.code,400);self.assertEqual(self.get('/api/state')['revision'],0);self.assertEqual(self.get('/api/backups')['backups'],[])
if __name__=='__main__':unittest.main()
