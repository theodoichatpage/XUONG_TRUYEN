"""Xuong Truyen 0.1.0: local-only HTTP app, standard library, SQLite."""
import json, os, secrets, sqlite3, threading, webbrowser
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
DB_PATH = DATA / 'xuong-truyen.sqlite3'
TOKEN = secrets.token_urlsafe(32)
LOCK = threading.Lock()
PORT = int(os.environ.get('XUONG_TRUYEN_PORT', '7872'))

def connect():
    DATA.mkdir(exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute('CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY CHECK(id=1), revision INTEGER NOT NULL, body TEXT NOT NULL)')
    con.execute('INSERT OR IGNORE INTO state VALUES (1,0,?)', (json.dumps({'version':1,'books':[]}),))
    con.commit()
    return con

def validate(data):
    if not isinstance(data, dict) or data.get('version') != 1 or not isinstance(data.get('books'), list):
        raise ValueError('Sai định dạng dữ liệu')
    ids = set()
    for book in data['books']:
        if not isinstance(book, dict) or not isinstance(book.get('id'), str) or book['id'] in ids:
            raise ValueError('Mã bộ truyện bị trùng hoặc thiếu')
        ids.add(book['id'])
        for key in ('language','genre','style','premise','world'):
            if not isinstance(book.get(key),str): raise ValueError('Hồ sơ thiếu trường '+key)
        if not isinstance(book.get('length'),int) or book['length']<1: raise ValueError('Độ dài không hợp lệ')
        if not isinstance(book.get('title'), str) or not book['title'].strip():
            raise ValueError('Thiếu tên bộ truyện')
        for key in ('characters','plans','chapters','memories'):
            if not isinstance(book.get(key), list): raise ValueError('Thiếu danh sách '+key)
            row_ids = set()
            for row in book[key]:
                if not isinstance(row, dict) or not isinstance(row.get('id'),str) or row['id'] in row_ids:
                    raise ValueError('Mã bản ghi bị trùng hoặc thiếu')
                row_ids.add(row['id'])
                if not isinstance(row.get('title'),str) or not isinstance(row.get('body'),str): raise ValueError('Bản ghi thiếu tiêu đề hoặc nội dung')
                if key == 'chapters':
                    if not isinstance(row.get('number'),int) or row['number']<1: raise ValueError('Số chương không hợp lệ')
                    if not isinstance(row.get('summary'),str) or not isinstance(row.get('intent'),str): raise ValueError('Thiếu hồ sơ chương')
                    if row.get('status') not in ('draft','review','approved','live'): raise ValueError('Sai trạng thái chương')
                    if row['status'] != 'draft' and not str(row.get('body','')).strip(): raise ValueError('Chương chưa có nội dung')
                    if not isinstance(row.get('history'),list): raise ValueError('Thiếu lịch sử chương')
    return data

def save_state(data, revision):
    validate(data)
    body = json.dumps(data, ensure_ascii=False)
    with LOCK, connect() as con:
        result = con.execute('UPDATE state SET body=?, revision=revision+1 WHERE id=1 AND revision=?',(body,revision))
        if result.rowcount != 1: raise RuntimeError('Dữ liệu đã thay đổi ở tab khác. Sao chép phần đang sửa rồi tải lại trang.')
    return revision+1

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw): super().__init__(*a,directory=str(ROOT/'web'),**kw)
    def log_message(self,*a): pass
    def allowed(self):
        return self.headers.get('Host') in (f'127.0.0.1:{PORT}',f'localhost:{PORT}')
    def json_response(self, data, code=200):
        raw=json.dumps(data,ensure_ascii=False).encode()
        self.send_response(code); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        if not self.allowed(): return self.json_response({'error':'Host không được phép'},403)
        if self.path=='/api/state':
            with connect() as con: revision,body=con.execute('SELECT revision,body FROM state WHERE id=1').fetchone()
            return self.json_response({'data':json.loads(body),'revision':revision,'token':TOKEN})
        if self.path.startswith('/api/'): return self.json_response({'error':'Không tìm thấy'},404)
        return super().do_GET()
    def do_POST(self):
        if not self.allowed() or self.headers.get('X-Xuong-Token')!=TOKEN:
            return self.json_response({'error':'Yêu cầu không hợp lệ'},403)
        if self.path!='/api/state': return self.json_response({'error':'Không tìm thấy'},404)
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=20_000_000: return self.json_response({'error':'Dữ liệu tối đa 20MB'},413)
            payload=json.loads(self.rfile.read(size)); rev=save_state(payload['data'],payload['revision'])
            self.json_response({'revision':rev})
        except RuntimeError as e: self.json_response({'error':str(e)},409)
        except (ValueError,KeyError,TypeError) as e: self.json_response({'error':str(e)},400)

if __name__=='__main__':
    connect().close()
    url=f'http://127.0.0.1:{PORT}'
    server=ThreadingHTTPServer(('127.0.0.1',PORT),Handler)
    print('Xưởng Truyện 0.1.0 — '+url, flush=True)
    if '--no-browser' not in __import__('sys').argv: webbrowser.open(url)
    try: server.serve_forever()
    except KeyboardInterrupt: server.server_close()
