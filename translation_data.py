"""Deterministic validation for bilingual manuscript structures; no translation service."""
import re, unicodedata
LANGS={'en','zh','vi'}
DEFAULTS={
'en':'Contemporary American English. Preserve POV, tense, names, character voice and all plot facts. Use natural literary English.',
'zh':'使用自然、流畅的简体中文小说文风。保留原文视角、语气、人物关系和所有情节。人名、称谓、修炼等级以术语表为准，不擅自改写。',
'vi':'Tiếng Việt tự nhiên, rõ nghĩa. Giữ ngôi kể, sắc thái thoại, quan hệ nhân vật. Thống nhất xưng hô và tên riêng theo bảng thuật ngữ; không tự thêm tình tiết.'}
CHECKS=('meaning','terms','voice','natural','continuity')

def require(ok,message):
 if not ok:raise ValueError(message)
def text(o,k):require(isinstance(o.get(k),str),'Dữ liệu dịch thiếu trường văn bản: '+k)
def split(body):return [{'id':'p'+str(i+1).zfill(4),'source':s} for i,s in enumerate(p for p in re.split(r'\n[\t ]*\n+',body.replace('\r\n','\n').replace('\r','\n')) if p.strip())]
def batches(segments):
 result=[];batch=[];size=0
 for s in segments:
  if batch and (len(batch)>=8 or size+len(s['source'])>6000):result.append(batch);batch=[];size=0
  batch.append(s);size+=len(s['source'])
 if batch:result.append(batch)
 return result

def validate_terms(terms):
 require(isinstance(terms,list),'Bảng thuật ngữ phải là danh sách');seen=set()
 for term in terms:
  require(isinstance(term,dict),'Thuật ngữ không hợp lệ')
  require(term.get('sourceLang') in LANGS and term.get('targetLang') in LANGS and term['sourceLang']!=term['targetLang'],'Cặp ngôn ngữ thuật ngữ không hợp lệ')
  for k in ('source','target','note'):text(term,k)
  require(bool(term['source'].strip()) and bool(term['target'].strip()),'Thuật ngữ không được trống')
  key=(term['sourceLang'],term['targetLang'],unicodedata.normalize('NFC',term['source']).lower());require(key not in seen,'Thuật ngữ nguồn bị trùng');seen.add(key)
def validate_config(b):
 if 'translationConfig' not in b:return
 cfg=b['translationConfig'];require(isinstance(cfg,dict),'Cấu hình dịch không hợp lệ')
 require(cfg.get('sourceLang') in LANGS and cfg.get('targetLang') in LANGS and cfg['sourceLang']!=cfg['targetLang'],'Nguồn và đích dịch không hợp lệ')
 styles=cfg.get('styles');require(isinstance(styles,dict) and set(styles)==LANGS and all(isinstance(v,str) for v in styles.values()),'Cần quy chuẩn cho ba ngôn ngữ')
 validate_terms(cfg.get('terms'))
def settings(b,target):
 cfg=b.get('translationConfig',{});source=cfg.get('sourceLang') or ('en' if re.search('english|tiếng anh',b['language'],re.I) else 'zh' if re.search('chinese|中文|tiếng trung',b['language'],re.I) else 'vi')
 style=cfg.get('styles',{}).get(target) or (b.get('englishGuide') if target=='en' else None) or DEFAULTS[target]
 # Explicit empty styles must be kept, matching the browser's object spread.
 if target in cfg.get('styles',{}):style=cfg['styles'][target]
 return {'sourceLang':source,'targetLang':target,'guide':style,'legacyGlossary':b.get('glossary','') if target=='en' else '', 'terms':[{'source':t['source'],'target':t['target'],'note':t.get('note','')} for t in cfg.get('terms',[]) if t['sourceLang']==source and t['targetLang']==target]}
def basis(t):return {k:t[k] for k in ('title','body','notes','sourceBody','sourceTitle','settings')}
def validate_settings(st):
 require(isinstance(st,dict) and st.get('sourceLang') in LANGS and st.get('targetLang') in LANGS and st['sourceLang']!=st['targetLang'],'Snapshot ngôn ngữ không hợp lệ')
 for k in ('guide','legacyGlossary'):text(st,k)
 require(isinstance(st.get('terms'),list),'Snapshot thuật ngữ không hợp lệ')
 for term in st['terms']:
  require(isinstance(term,dict),'Snapshot thuật ngữ sai')
  for k in ('source','target','note'):text(term,k)
def eligible(t):
 bs=batches(t['segments'])
 return bool(t['title'].strip()) and bool(bs) and all(s['target'].strip() for s in t['segments']) and all(t['checks'].get(k) is True for k in CHECKS) and all(any(r['batch']==i and r['complete'] and r['basis']==basis(t) and all(x['resolved'] and x['resolution'].strip() for x in r['issues']) for r in t['reviews']) for i in range(len(bs)))
def validate_translation(t,target,historical=False):
 require(isinstance(t,dict),'Bản dịch phải là đối tượng')
 for k in ('title','body','notes','sourceBody','sourceTitle','sourceLang','targetLang'):text(t,k)
 require(t['sourceLang'] in LANGS and t['targetLang']==target and target!=t['sourceLang'],'Ngôn ngữ bản dịch không khớp')
 validate_settings(t.get('settings'));require(t['settings']['sourceLang']==t['sourceLang'] and t['settings']['targetLang']==target,'Snapshot không khớp hướng dịch')
 segments=t.get('segments');require(isinstance(segments,list),'Thiếu danh sách đoạn dịch');expected=split(t['sourceBody']);require(len(segments)==len(expected),'Số đoạn không khớp nguồn')
 for s,original in zip(segments,expected):
  require(isinstance(s,dict) and s.get('id')==original['id'] and s.get('source')==original['source'],'Mã/nội dung đoạn nguồn không khớp')
  for k in ('target','notes'):text(s,k)
 require(t['body']=='\n\n'.join(s['target'] for s in segments),'Toàn văn dịch không khớp các đoạn')
 require(t.get('status') in ('review','approved'),'Trạng thái bản dịch sai');checks=t.get('checks');require(isinstance(checks,dict) and all(k in CHECKS and type(v) is bool for k,v in checks.items()),'Checklist dịch sai kiểu')
 reviews=t.get('reviews');require(isinstance(reviews,list),'Thiếu danh sách rà soát');bs=batches(segments);seen=set()
 for r in reviews:
  require(isinstance(r,dict) and type(r.get('batch')) is int and 0<=r['batch']<len(bs) and r['batch'] not in seen,'Nhóm rà soát không hợp lệ hoặc trùng');seen.add(r['batch'])
  require(type(r.get('complete')) is bool,'Báo cáo thiếu xác nhận hoàn tất');rb=r.get('basis');require(isinstance(rb,dict),'Thiếu nguồn báo cáo')
  for k in ('title','body','notes','sourceBody','sourceTitle'):text(rb,k)
  validate_settings(rb.get('settings'))
  require(isinstance(r.get('issues'),list),'Danh sách lỗi sai');ids=set()
  for x in r['issues']:
   require(isinstance(x,dict) and isinstance(x.get('id'),str) and re.fullmatch('[A-Za-z0-9_-]{1,100}',x['id']) is not None and x['id'] not in ids,'Mã lỗi sai/trùng');ids.add(x['id'])
   require(x.get('pid') in {s['id'] for s in bs[r['batch']]} and x.get('severity') in ('critical','major','minor'),'Mã đoạn/mức độ lỗi sai')
   for k in ('explanation','suggestion','resolution'):text(x,k)
   require(type(x.get('resolved')) is bool,'Trạng thái xử lý lỗi sai')
 if t['status']=='approved':require(eligible(t),'Bản dịch chưa đủ đoạn/rà soát/xử lý lỗi để duyệt')
 if not historical:
  require(isinstance(t.get('history'),list),'Thiếu lịch sử dịch')
  for old in t['history']:validate_translation(old,target,True)
def validate_book(b):
 validate_config(b)
 for c in b['chapters']:
  if 'translations' not in c:continue
  require(isinstance(c['translations'],dict) and all(k in LANGS for k in c['translations']),'Kho bản dịch sai')
  for target,t in c['translations'].items():validate_translation(t,target)
