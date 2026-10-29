(function(root){
'use strict';
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function context(book, chapter){
 const previous=book.chapters.filter(c=>c.number<chapter.number&&['approved','live'].includes(c.status)).sort((a,b)=>a.number-b.number).slice(-3);
 return ['Bạn là biên tập viên và tác giả truyện dài kỳ. Đây là bản nháp để con người duyệt.',`TRUYỆN: ${book.title}\nNGÔN NGỮ: ${book.language}\nTHỂ LOẠI: ${book.genre}\nGIỌNG VĂN: ${book.style}`,`TIỀN ĐỀ:\n${book.premise}\nTHẾ GIỚI VÀ QUY TẮC:\n${book.world}`,`NHÂN VẬT:\n${book.characters.map(c=>c.title+': '+c.body).join('\n')}`,`DÀN Ý:\n${book.plans.map(p=>p.title+': '+p.body).join('\n')}`,`TRÍ NHỚ ĐÃ XÁC NHẬN (chỉ trước chương hiện tại):\n${book.memories.filter(m=>m.confirmed&&Number(m.chapter||0)<chapter.number).map(m=>m.type+' / '+m.title+': '+m.body).join('\n')}`,`CÁC CHƯƠNG TRƯỚC ĐÃ DUYỆT:\n${previous.map(c=>'Chương '+c.number+': '+(c.summary||c.body)).join('\n\n')}`,`CHƯƠNG ${chapter.number}: ${chapter.title}\nÝ ĐỊNH CHƯƠNG: ${chapter.intent}\nĐỘ DÀI MỤC TIÊU: ${book.length} từ.`, 'Giữ nhất quán nguyên nhân–kết quả, mục tiêu nhân vật, thời gian và địa điểm. Không tự đổi sự kiện đã xác nhận. Nếu thiếu thông tin thiết yếu, nêu câu hỏi thay vì tự khẳng định. Chỉ trả nội dung chương, không lời dẫn.'].join('\n\n');
}
function acceptChapter(chapter, body, at){
 if(!body.trim())throw Error('Kết quả trống');
 if(!['draft','review'].includes(chapter.status))throw Error('Chương đã duyệt. Tạo bản sửa và duyệt lại trước.');
 chapter.history.push({body:chapter.body,summary:chapter.summary,status:chapter.status,at});
 chapter.body=body.trim(); chapter.status='review'; chapter.revision=(chapter.revision||0)+1;
 return chapter;
}
function translationFresh(book,chapter){const t=chapter.english;return !!t&&['approved','live'].includes(chapter.status)&&t.sourceBody===chapter.body&&t.sourceTitle===chapter.title&&t.glossary===(book.glossary||'')&&t.guide===(book.englishGuide||'')}
function canExportEnglish(book,chapter){return translationFresh(book,chapter)&&chapter.english.status==='approved'&&['meaning','terms','voice','natural','continuity'].every(k=>chapter.english.checks?.[k]===true)}
const api={esc,context,acceptChapter,translationFresh,canExportEnglish}; if(typeof module!=='undefined')module.exports=api;else root.Story=api;
})(typeof window!=='undefined'?window:globalThis);
