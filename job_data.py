"""Validate durable local extension jobs; no external requests."""
import re
import translation_data

def validate(data):
 if 'aiJobs' not in data:return
 jobs=data['aiJobs']
 def require(ok,message):
  if not ok:raise ValueError(message)
 require(isinstance(jobs,list),'Danh sách công việc AI không hợp lệ');ids=set()
 for job in jobs:
  require(isinstance(job,dict) and isinstance(job.get('id'),str) and re.fullmatch('xt_[A-Za-z0-9_-]{1,100}',job['id']) is not None and job['id'] not in ids,'Mã công việc AI không hợp lệ/trùng');ids.add(job['id'])
  for key in ('bookId','chapterId','prompt','baseChapter','createdAt','resultText'):
   require(isinstance(job.get(key),str),'Công việc AI thiếu trường '+key)
  for key in ('error','appliedAt','receivedAt'):
   if key in job:require(isinstance(job[key],str),'Trường công việc AI không hợp lệ: '+key)
  require(job.get('status') in ('queued','waiting_send','ready','applied','stopped','error'),'Trạng thái công việc AI không hợp lệ')
  require(job.get('mode') in ('write','translate','review'),'Loại công việc AI không hợp lệ')
  require(len(job['prompt'])<=150000 and len(job['resultText'])<=600000,'Yêu cầu/kết quả AI quá lớn')
  if job['mode']!='write':
   checkpoint=job.get('checkpoint');require(isinstance(checkpoint,dict),'Thiếu checkpoint dịch')
   require(checkpoint.get('mode')==job['mode'] and checkpoint.get('bookId')==job['bookId'] and checkpoint.get('chapterId')==job['chapterId'],'Checkpoint công việc không khớp')
   require(checkpoint.get('target') in translation_data.LANGS and type(checkpoint.get('index')) is int,'Ngôn ngữ/nhóm dịch không hợp lệ')
   require(isinstance(checkpoint.get('baseTranslation'),str),'Thiếu phiên bản bản dịch đích')
   translation_data.validate_translation(checkpoint.get('draft'),checkpoint['target'])
   require(0<=checkpoint['index']<len(translation_data.batches(checkpoint['draft']['segments'])),'Nhóm dịch nằm ngoài nguồn')
