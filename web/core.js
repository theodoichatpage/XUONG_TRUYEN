(function(root){
'use strict';
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const planKinds={volume:'Tập',arc:'Tuyến truyện',chapter:'Kế hoạch chương',scene:'Cảnh',note:'Ghi chú chung'};
const threadStates={open:'Đã gợi mở',developing:'Đang phát triển',resolved:'Đã giải quyết',dropped:'Đã bỏ'};
function bodyVersion(c){return c.bodyRevision||1}
function summaryFresh(c){return !!c.summary&&c.summaryBody===c.body&&c.summaryRevision===bodyVersion(c)}
function selectedPlans(book,chapter){
 const plans=book.plans,chosen=new Set(plans.filter(p=>!p.kind||p.kind==='note').map(p=>p.id));
 const linked=plans.find(p=>p.id===chapter.planId);
 if(linked){let p=linked;while(p&&!chosen.has(p.id)){chosen.add(p.id);p=plans.find(x=>x.id===p.parentId)}
 for(const scene of plans.filter(p=>p.kind==='scene'&&p.parentId===linked.id))chosen.add(scene.id);
 }else for(const p of plans)if(p.kind&&p.kind!=='note'&&p.startChapter<=chapter.number&&p.endChapter>=chapter.number)chosen.add(p.id);
 return plans.filter(p=>chosen.has(p.id)).sort((a,b)=>({note:0,volume:1,arc:2,chapter:3,scene:4}[a.kind||'note']- {note:0,volume:1,arc:2,chapter:3,scene:4}[b.kind||'note'])||(a.order||0)-(b.order||0)||a.title.localeCompare(b.title));
}
function threadStateAt(m,number){
 if(m.chapter>=number)return null;
 if(m.threadStatus==='resolved'&&m.resolvedChapter>=number)return 'developing';
 return m.threadStatus||'open';
}
function threadAlerts(book,number){return book.memories.filter(m=>m.type==='Nút thắt'&&m.confirmed&&m.chapter<number&&!['resolved','dropped'].includes(threadStateAt(m,number))&&m.dueChapter>0&&m.dueChapter<=number).map(m=>({id:m.id,title:m.title,dueChapter:m.dueChapter,overdue:m.dueChapter<number}));}
function context(book, chapter){
 const previous=book.chapters.filter(c=>c.number<chapter.number&&['approved','live'].includes(c.status)).sort((a,b)=>a.number-b.number).slice(-3);
 const memories=book.memories.filter(m=>m.confirmed&&Number(m.chapter||0)<chapter.number).map(m=>{
 if(m.type!=='Nút thắt')return m.type+' / '+m.title+': '+m.body;
 const state=threadStateAt(m,chapter.number);
 return 'Nút thắt / '+m.title+': '+m.body+' | Trạng thái trước chương: '+threadStates[state]+(m.dueChapter?' | Mốc dự kiến chương '+m.dueChapter:'')+(state==='resolved'?' | Đã giải quyết ở chương '+m.resolvedChapter+': '+m.resolution:'');
 });
 const alerts=threadAlerts(book,chapter.number);
 return ['Bạn là biên tập viên và tác giả truyện dài kỳ. Đây là bản nháp để con người duyệt.',`TRUYỆN: ${book.title}\nNGÔN NGỮ: ${book.language}\nTHỂ LOẠI: ${book.genre}\nGIỌNG VĂN: ${book.style}`,`TIỀN ĐỀ:\n${book.premise}\nTHẾ GIỚI VÀ QUY TẮC:\n${book.world}`,`NHÂN VẬT:\n${book.characters.map(c=>c.title+': '+c.body).join('\n')}`,`DÀN Ý LIÊN QUAN CHƯƠNG HIỆN TẠI:\n${selectedPlans(book,chapter).map(p=>(planKinds[p.kind]||'Ghi chú chung')+' / '+p.title+': '+p.body).join('\n')}`,`TRÍ NHỚ ĐÃ XÁC NHẬN (chỉ trước chương hiện tại):\n${memories.join('\n')}`,`NÚT THẮT ĐẾN MỐC CẦN XEM XÉT (không bắt buộc tự giải quyết):\n${alerts.map(m=>m.title+' — chương '+m.dueChapter+(m.overdue?' (quá mốc)':' (đến mốc)')).join('\n')}`,`CÁC CHƯƠNG TRƯỚC ĐÃ DUYỆT:\n${previous.map(c=>'Chương '+c.number+' [nội dung v'+bodyVersion(c)+']: '+(summaryFresh(c)?c.summary:c.body)).join('\n\n')}`,`CHƯƠNG ${chapter.number}: ${chapter.title}\nÝ ĐỊNH CHƯƠNG: ${chapter.intent}\nĐỘ DÀI MỤC TIÊU: ${book.length} từ.`, 'Giữ nhất quán nguyên nhân–kết quả, mục tiêu nhân vật, thời gian và địa điểm. Không tự đổi sự kiện đã xác nhận. Dàn ý là dự định, không phải sự kiện đã xảy ra. Nút thắt quá mốc cần được tác giả quyết định, không tự kết luận đã giải quyết. Nếu thiếu thông tin thiết yếu, nêu câu hỏi thay vì tự khẳng định. Chỉ trả nội dung chương, không lời dẫn.'].join('\n\n');
}
function acceptChapter(chapter, body, at){
 if(!body.trim())throw Error('Kết quả trống');
 if(!['draft','review'].includes(chapter.status))throw Error('Chương đã duyệt. Tạo bản sửa và duyệt lại trước.');
 chapter.history.push({body:chapter.body,summary:chapter.summary,bodyRevision:bodyVersion(chapter),summaryRevision:chapter.summaryRevision||0,summaryBody:chapter.summaryBody||'',status:chapter.status,at});
 if(chapter.body!==body.trim())chapter.bodyRevision=bodyVersion(chapter)+1;
 chapter.body=body.trim(); chapter.summaryRevision=0; chapter.summary=''; chapter.summaryBody=''; chapter.status='review'; chapter.revision=(chapter.revision||0)+1;
 return chapter;
}
function translationFresh(book,chapter){const t=chapter.english;return !!t&&['approved','live'].includes(chapter.status)&&t.sourceBody===chapter.body&&t.sourceTitle===chapter.title&&t.glossary===(book.glossary||'')&&t.guide===(book.englishGuide||'')}
function canExportEnglish(book,chapter){return translationFresh(book,chapter)&&chapter.english.status==='approved'&&['meaning','terms','voice','natural','continuity'].every(k=>chapter.english.checks?.[k]===true)}
function resetEnglishReview(old,next){
 if(old&&(old.title!==next.title||old.body!==next.body||old.notes!==next.notes)){next.status='review';next.checks={};}
 return next;
}
const api={esc,context,acceptChapter,translationFresh,canExportEnglish,resetEnglishReview,planKinds,threadStates,selectedPlans,threadAlerts,summaryFresh,bodyVersion,threadStateAt}; if(typeof module!=='undefined')module.exports=api;else root.Story=api;
})(typeof window!=='undefined'?window:globalThis);
