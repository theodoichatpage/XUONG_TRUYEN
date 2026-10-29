"""Xuong Truyen 0.4.0: local-only HTTP app, standard library, SQLite."""
import json, os, secrets, sqlite3, threading, webbrowser, re
from datetime import datetime, timezone
import translation_data
import job_data
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

def require(ok, message):
    if not ok: raise ValueError(message)

def text(obj, key, optional=False):
    require((optional and key not in obj) or isinstance(obj.get(key), str), 'Trường văn bản không hợp lệ: '+key)

def history(rows, english=False):
    require(isinstance(rows,list), 'Lịch sử phải là danh sách')
    for row in rows:
        require(isinstance(row,dict), 'Bản lịch sử không hợp lệ')
        for key in ('body','summary','status','at'):
            text(row,key,optional=english or key in ('summary','at'))
        if english:
            for key in ('title','notes','sourceBody','sourceTitle','glossary','guide'):
                text(row,key)
            require(row.get('status') in ('review','approved'), 'Trạng thái lịch sử dịch không hợp lệ')
            require(isinstance(row.get('checks'),dict) and all(type(v) is bool for v in row['checks'].values()), 'Kiểm tra lịch sử dịch không hợp lệ')
        else:
            require(row.get('status') in ('draft','review','approved','live'), 'Trạng thái lịch sử không hợp lệ')

def safe_keys(value):
    if isinstance(value,dict):
        require(not any(k in ('__proto__','constructor','prototype') for k in value), 'Khóa dữ liệu không được phép')
        for v in value.values(): safe_keys(v)
    elif isinstance(value,list):
        for v in value: safe_keys(v)

def validate(data):
    safe_keys(data)
    require(isinstance(data,dict) and type(data.get('version')) is int and data['version']==1 and isinstance(data.get('books'),list), 'Sai định dạng dữ liệu')
    def valid_id(row, ids):
        require(isinstance(row,dict) and isinstance(row.get('id'),str) and re.fullmatch(r'[A-Za-z0-9_-]{1,100}',row['id']) is not None, 'Mã bản ghi không hợp lệ')
        require(row['id'] not in ids, 'Mã bản ghi bị trùng'); ids.add(row['id'])
    ids=set()
    for book in data['books']:
        valid_id(book,ids)
        for key in ('title','language','genre','style','premise','world'): text(book,key)
        require(bool(book['title'].strip()), 'Thiếu tên bộ truyện')
        for key in ('glossary','englishGuide','exclusivity'): text(book,key,True)
        require(type(book.get('length')) is int and 1<=book['length']<=100000, 'Độ dài không hợp lệ')
        for key in ('characters','plans','chapters','memories'):
            require(isinstance(book.get(key),list), 'Thiếu danh sách '+key)
            row_ids=set(); numbers=set()
            for row in book[key]:
                valid_id(row,row_ids)
                for field in ('title','body'): text(row,field)
                if key=='plans' and 'kind' in row:
                    require(row['kind'] in ('volume','arc','chapter','scene','note'), 'Loại dàn ý không hợp lệ')
                    text(row,'parentId',True)
                    if row['kind']!='note':
                        require(type(row.get('startChapter')) is int and type(row.get('endChapter')) is int and 1<=row['startChapter']<=row['endChapter']<=100000, 'Phạm vi chương dàn ý không hợp lệ')
                        require(row['kind'] not in ('chapter','scene') or row['startChapter']==row['endChapter'], 'Kế hoạch chương/cảnh chỉ thuộc một chương')
                    if 'order' in row: require(type(row['order']) is int and row['order']>=0,'Thứ tự dàn ý không hợp lệ')
                if key=='memories':
                    require(type(row.get('confirmed')) is bool, 'Ghi nhớ cần xác nhận đúng kiểu')
                    require(type(row.get('chapter')) is int and row['chapter']>=1, 'Chương ghi nhớ không hợp lệ')
                    require(row.get('type') in ('Sự kiện','Nút thắt','Dòng thời gian','Quy tắc'), 'Loại ghi nhớ không hợp lệ')
                    if row['type']=='Nút thắt':
                        require(row.get('threadStatus','open') in ('open','developing','resolved','dropped'),'Trạng thái nút thắt không hợp lệ')
                        for field in ('dueChapter','resolvedChapter'):
                            require(type(row.get(field,0)) is int and 0<=row.get(field,0)<=100000,'Mốc nút thắt không hợp lệ')
                        require(not row.get('dueChapter') or row['dueChapter']>=row['chapter'],'Mốc giải quyết phải sau chương gợi mở')
                        text(row,'resolution',True)
                        if row.get('threadStatus')=='resolved':
                            require(row.get('resolvedChapter',0)>=row['chapter'] and bool(row.get('resolution','').strip()),'Nút thắt đã giải quyết cần chương và ghi chú kết quả')
                if key!='chapters': continue
                require(type(row.get('number')) is int and 1<=row['number']<=100000 and row['number'] not in numbers, 'Số chương không hợp lệ hoặc bị trùng')
                numbers.add(row['number'])
                for field in ('summary','intent'): text(row,field)
                for field in ('summaryBody','link','planId'): text(row,field,True)
                for field in ('bodyRevision','summaryRevision'):
                    if field in row: require(type(row[field]) is int and row[field]>=(1 if field=='bodyRevision' else 0),'Phiên bản nội dung/tóm tắt không hợp lệ')
                require(row.get('status') in ('draft','review','approved','live'), 'Sai trạng thái chương')
                require(row['status']=='draft' or bool(row['body'].strip()), 'Chương chưa có nội dung')
                if 'revision' in row: require(type(row['revision']) is int and row['revision']>=0,'Phiên bản chương không hợp lệ')
                history(row.get('history'))
                if 'english' not in row: continue
                en=row['english'];require(isinstance(en,dict), 'Bản dịch không hợp lệ')
                for field in ('title','body','notes','sourceBody','sourceTitle','glossary','guide'): text(en,field)
                require(en.get('status') in ('review','approved'), 'Trạng thái bản dịch không hợp lệ')
                checks=en.get('checks');require(isinstance(checks,dict) and all(k in ('meaning','terms','voice','natural','continuity') and type(v) is bool for k,v in checks.items()), 'Checklist bản dịch không hợp lệ')
                if en['status']=='approved':
                    require(all(checks.get(k) is True for k in ('meaning','terms','voice','natural','continuity')), 'Bản dịch đã duyệt thiếu kiểm tra')
                    require(bool(en['body'].strip()) and bool(en['title'].strip()), 'Bản dịch đã duyệt bị trống')
                history(en.get('history'),True)
        translation_data.validate_book(book)
        plan_map={p['id']:p for p in book['plans']}
        expected={'arc':'volume','chapter':'arc','scene':'chapter'}
        for p in book['plans']:
            kind=p.get('kind','note'); parent=p.get('parentId','')
            if kind in ('volume','note'): require(not parent,'Tập/ghi chú chung không có cấp cha')
            else:
                require(parent in plan_map and plan_map[parent].get('kind')==expected[kind], 'Cấp cha dàn ý không hợp lệ')
                ancestor=plan_map[parent]
                require(ancestor['startChapter']<=p['startChapter']<=p['endChapter']<=ancestor['endChapter'],'Phạm vi dàn ý nằm ngoài cấp cha')
        for c in book['chapters']:
            if c.get('planId'):
                require(c['planId'] in plan_map and plan_map[c['planId']].get('kind')=='chapter','Chương phải liên kết kế hoạch chương của cùng bộ truyện')
                require(plan_map[c['planId']]['startChapter']==c['number'],'Số chương khác kế hoạch đã chọn')
    job_data.validate(data)
    return data

def save_state(data, revision, restore=False):
    require(type(revision) is int and revision>=0, 'Phiên bản dữ liệu không hợp lệ')
    validate(data)
    body=json.dumps(data,ensure_ascii=False)
    with LOCK, connect() as con:
        old_revision,old_body=con.execute('SELECT revision,body FROM state WHERE id=1').fetchone()
        if old_revision!=revision: raise RuntimeError('Dữ liệu đã thay đổi ở tab khác. Sao chép phần đang sửa rồi tải lại trang.')
        if not restore:
            previous=json.loads(old_body)
            old_books={b['id']:b for b in previous['books']}
            for b in data['books']:
                old_book=old_books.get(b['id'],{})
                old_chapters={c['id']:c for c in old_book.get('chapters',[])}
                for c in b['chapters']:
                    old=old_chapters.get(c['id'])
                    if not old:
                        c['bodyRevision']=1
                        if not c.get('summary') or c.get('summaryRevision')!=1 or c.get('summaryBody')!=c['body']: c['summaryRevision']=0
                        continue
                    c['bodyRevision']=old.get('bodyRevision',1)+(old['body']!=c['body'])
                    if old['body']!=c['body']:
                        if c['summary']==old['summary']: c['summary']='';c['summaryBody']=''
                    if not c.get('summary') or c.get('summaryBody')!=c['body'] or c.get('summaryRevision')!=c['bodyRevision']: c['summaryRevision']=0
                    for target,after_translation in c.get('translations',{}).items():
                        before_translation=old.get('translations',{}).get(target)
                        if before_translation and translation_data.basis(before_translation)!=translation_data.basis(after_translation):
                            after_translation['status']='review';after_translation['checks']={};after_translation['reviews']=[]
                    before=old.get('english'); after=c.get('english')
                    if before and after and any(before[k]!=after[k] for k in ('title','body','notes')):
                        after['status']='review';after['checks']={}
            body=json.dumps(data,ensure_ascii=False)
        if restore:
            con.execute('CREATE TABLE IF NOT EXISTS backups (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, revision INTEGER NOT NULL, body TEXT NOT NULL)')
            con.execute('INSERT INTO backups VALUES (?,?,?,?)',(secrets.token_hex(16),datetime.now(timezone.utc).isoformat(),revision,old_body))
        con.execute('UPDATE state SET body=?,revision=revision+1 WHERE id=1',(body,))
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
        if self.path=='/api/backups':
            with connect() as con:
                con.execute('CREATE TABLE IF NOT EXISTS backups (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, revision INTEGER NOT NULL, body TEXT NOT NULL)')
                rows=con.execute('SELECT id,created_at,revision FROM backups ORDER BY created_at DESC').fetchall()
            return self.json_response({'backups':[dict(zip(('id','createdAt','revision'),r)) for r in rows]})
        if self.path.startswith('/api/backups/'):
            backup_id=self.path.rsplit('/',1)[-1]
            if not re.fullmatch('[a-f0-9]{32}',backup_id): return self.json_response({'error':'Mã sao lưu không hợp lệ'},400)
            with connect() as con:
                con.execute('CREATE TABLE IF NOT EXISTS backups (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, revision INTEGER NOT NULL, body TEXT NOT NULL)')
                row=con.execute('SELECT body FROM backups WHERE id=?',(backup_id,)).fetchone()
            return self.json_response({'data':json.loads(row[0])}) if row else self.json_response({'error':'Không thấy sao lưu'},404)
        if self.path.startswith('/api/'): return self.json_response({'error':'Không tìm thấy'},404)
        return super().do_GET()
    def do_POST(self):
        if not self.allowed() or self.headers.get('X-Xuong-Token')!=TOKEN:
            return self.json_response({'error':'Yêu cầu không hợp lệ'},403)
        if self.path not in ('/api/state','/api/restore'): return self.json_response({'error':'Không tìm thấy'},404)
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=20_000_000: return self.json_response({'error':'Dữ liệu tối đa 20MB'},413)
            payload=json.loads(self.rfile.read(size)); rev=save_state(payload['data'],payload['revision'],restore=self.path=='/api/restore')
            self.json_response({'revision':rev,'data':payload['data']})
        except RuntimeError as e: self.json_response({'error':str(e)},409)
        except (ValueError,KeyError,TypeError,RecursionError) as e: self.json_response({'error':str(e)},400)
        except sqlite3.Error:
            self.json_response({'error':'Không ghi được cơ sở dữ liệu hoặc sao lưu an toàn. Dữ liệu chưa được thay thế.'},500)

if __name__=='__main__':
    connect().close()
    url=f'http://127.0.0.1:{PORT}'
    server=ThreadingHTTPServer(('127.0.0.1',PORT),Handler)
    print('Xưởng Truyện 0.4.0 — '+url, flush=True)
    if '--no-browser' not in __import__('sys').argv: webbrowser.open(url)
    try: server.serve_forever()
    except KeyboardInterrupt: server.server_close()
