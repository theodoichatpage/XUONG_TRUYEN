(function(root){'use strict';
const Story=typeof module!=='undefined'?require('./core.js'):root.Story,T=typeof module!=='undefined'?require('./translation.js'):root.Translation;
function fingerprint(c){const {bodyRevision,summaryRevision,...record}=c;return JSON.stringify(record)}
function prepare(state,chapterJob,translationJob,prompt,id){
 if(!prompt.trim())throw Error('Yêu cầu trống.');const checkpoint=translationJob||chapterJob;if(!checkpoint)throw Error('Mở yêu cầu từ một chương hoặc nhóm dịch trước.');const b=state.books.find(b=>b.id===checkpoint.bookId),c=b?.chapters.find(c=>c.id===checkpoint.chapterId);if(!c)throw Error('Không còn chương đích.');
 if(!translationJob&&!['draft','review'].includes(c.status))throw Error('Chương đã duyệt. Chuyển về bản nháp/chờ duyệt trước khi viết lại.');
 if(translationJob&&!T.fresh(b,c,translationJob.draft))throw Error('Nguồn hoặc quy chuẩn dịch đã đổi.');
 const enJob=translationJob?structuredClone(translationJob):null;if(enJob)enJob.draft.body=T.body(enJob.draft);
 return {id,bookId:b.id,chapterId:c.id,mode:enJob?.mode||'write',prompt,baseChapter:fingerprint(c),checkpoint:enJob,createdAt:new Date().toISOString(),status:'queued',resultText:''};
}
function apply(state,j){if(j.status!=='ready')throw Error('Công việc chưa có kết quả chờ áp dụng.');const b=state.books.find(b=>b.id===j.bookId),c=b?.chapters.find(c=>c.id===j.chapterId);if(!c||fingerprint(c)!==j.baseChapter)throw Error('Chương/bản dịch đã đổi. Kết quả được giữ để xem và sao chép, không ghi đè.');if(!j.resultText?.trim())throw Error('Kết quả trống.');if(j.mode==='write'){if(Story.context(b,c)!==j.prompt)throw Error('Ngữ cảnh bộ truyện đã đổi. Hãy đối chiếu kết quả thủ công.');Story.acceptChapter(c,j.resultText,new Date().toISOString())}else{const en=j.checkpoint,t=structuredClone(en.draft);if(!T.fresh(b,c,t)||JSON.stringify(T.current(b,c,en.target))!==en.baseTranslation||T.prompt(b,c,t,en.index,en.mode==='review')!==j.prompt)throw Error('Nguồn, thuật ngữ, ngữ cảnh hoặc bản dịch đã đổi. Không tự ghi đè.');if(j.mode==='review')T.applyReview(t,en.index,j.resultText);else T.applyBatch(t,en.index,j.resultText);c.translations??={};c.translations[en.target]=t}j.status='applied';j.appliedAt=new Date().toISOString();j.error='';return j}
const api={prepare,apply,fingerprint};if(typeof module!=='undefined')module.exports=api;else root.BridgeCore=api;
})(typeof window!=='undefined'?window:globalThis);
