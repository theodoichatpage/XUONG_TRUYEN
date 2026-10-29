'use strict';
// Drafts are isolated per browser tab; no manuscript is sent outside localhost.
const draftKey='xt-unsaved-v1',draftConflicts=new Set();
const draftTargets={editor:{dialog:$('#editor'),form:$('#form')},english:{dialog:enDialog,form:$('#enForm')},ai:{dialog:$('#ai'),form:$('#ai')}};
let savedDrafts={};try{savedDrafts=JSON.parse(sessionStorage.getItem(draftKey)||'{}')}catch{}
if(!savedDrafts||typeof savedDrafts!=='object'||Array.isArray(savedDrafts))savedDrafts={};
function writeDrafts(){try{sessionStorage.setItem(draftKey,JSON.stringify(savedDrafts));draftButton.textContent='Bản đang soạn ('+Object.keys(savedDrafts).length+')'}catch{toast('Không giữ được bản tạm. Hãy sao chép nội dung trước khi đóng.');return false}return true}
function captureDraft(kind){
 const target=draftTargets[kind];if(!target?.dialog.open||!state)return true;
 const values={};target.form.querySelectorAll('input[name],textarea[name],select[name]').forEach(el=>{values[el.name]=el.type==='checkbox'?el.checked:el.value});
 if(kind==='ai'){values.prompt=$('#prompt').value;values.result=$('#result').value}
 savedDrafts[kind]={kind,bookId:currentId,revision:savedDrafts[kind]?.restoredRevision??revision,values,editing:kind==='editor'?editing:undefined,enEditing:kind==='english'?enEditing:undefined,job:kind==='ai'?job:undefined,enJob:kind==='ai'?enJob:undefined};
 return writeDrafts();
}
function clearDraft(kind){delete savedDrafts[kind];draftConflicts.delete(kind);writeDrafts()}
function draftCanSave(kind){if(!draftConflicts.has(kind))return true;toast('Dữ liệu đã đổi từ lúc giữ bản tạm. Sao chép nội dung, mở bản hiện tại rồi đối chiếu trước khi lưu.');return false}
const draftButton=document.createElement('button');draftButton.id='drafts';$('header>div').append(draftButton);
const backupButton=document.createElement('button');backupButton.id='safeBackups';backupButton.textContent='Sao lưu an toàn';$('header>div').append(backupButton);
const recoveryDialog=document.createElement('dialog');recoveryDialog.innerHTML='<div class="head"><h2>Khôi phục công việc</h2><button id="closeRecovery">×</button></div><div id="recoveryRows"></div>';document.body.append(recoveryDialog);$('#closeRecovery').onclick=()=>recoveryDialog.close();
draftButton.onclick=()=>{$('#recoveryRows').innerHTML=Object.keys(savedDrafts).map(k=>`<section class="panel"><h3>${esc({editor:'Bản thảo / hồ sơ',english:'Biên tập tiếng Anh',ai:'Yêu cầu và kết quả AI'}[k]||k)}</h3><button data-resume-draft="${esc(k)}">Mở lại</button><button data-export-draft="${esc(k)}">Tải bản tạm JSON</button></section>`).join('')||'<p>Không có bản đang soạn.</p>';recoveryDialog.showModal()};
backupButton.onclick=async()=>{try{const r=await fetch('/api/backups');if(!r.ok)throw Error('Không đọc được sao lưu');const data=await r.json();$('#recoveryRows').innerHTML='<p>Các bản được giữ tự động trước mỗi lần nhập dữ liệu. Tải JSON rồi dùng Nhập sao lưu nếu muốn khôi phục.</p>'+data.backups.map(b=>`<section class="panel"><p>${esc(new Date(b.createdAt).toLocaleString('vi-VN'))} · phiên bản ${esc(b.revision)}</p><button data-safe-backup="${esc(b.id)}">Tải bản trước khôi phục</button></section>`).join('');recoveryDialog.showModal()}catch(e){toast(e.message)}};
document.addEventListener('click',async e=>{const btn=e.target.closest('button');if(!btn)return;
 if(btn.dataset.exportDraft){const d=savedDrafts[btn.dataset.exportDraft];if(d)download('xuong-ban-tam.json',JSON.stringify(d,null,2),'application/json')}
 if(btn.dataset.safeBackup){try{const r=await fetch('/api/backups/'+encodeURIComponent(btn.dataset.safeBackup));if(!r.ok)throw Error('Không tải được sao lưu');const d=await r.json();download('xuong-truoc-khoi-phuc.json',JSON.stringify(d.data,null,2),'application/json')}catch(e){toast(e.message)}}
 if(btn.dataset.resumeDraft){const k=btn.dataset.resumeDraft,d=savedDrafts[k];if(!d||!draftTargets[k])return;try{
 if(d.bookId&&!state.books.some(b=>b.id===d.bookId))throw Error('Bộ truyện không còn tồn tại. Tải bản tạm JSON để giữ nội dung.');
 currentId=d.bookId;recoveryDialog.close();
 if(k==='editor'){view=d.editing.kind==='book'?'library':d.editing.kind;render();openEditor(d.editing.kind,d.editing.id)}
 if(k==='english'){view='english';render();if(d.enEditing.config)openTranslationConfig();else openTranslationEditor(d.enEditing.chapterId,d.enEditing.target);enEditing=d.enEditing}
 if(k==='ai'){job=d.job;enJob=d.enJob;$('#prompt').value=d.values.prompt||'';$('#result').value=d.values.result||'';$('#ai').showModal()}
 if(k==='english'&&d.enEditing.config)ensureTermRows(d.values);
 for(const el of draftTargets[k].form.querySelectorAll('input[name],textarea[name],select[name]'))if(Object.hasOwn(d.values,el.name)){if(el.type==='checkbox')el.checked=d.values[el.name]===true;else el.value=d.values[el.name]}
 if(k==='editor'&&d.editing.kind==='plans')updatePlanParent(d.values.parentId||'');
 if(d.revision!==revision){draftConflicts.add(k);toast('Đã mở bản tạm để sao chép; dữ liệu đã đổi nên cần đối chiếu với bản hiện tại.')}else draftConflicts.delete(k);
 d.restoredRevision=d.revision;
 }catch(e){toast(e.message)}}
});
for(const [kind,target] of Object.entries(draftTargets)){
 target.form.addEventListener('input',()=>captureDraft(kind));target.form.addEventListener('change',()=>captureDraft(kind));
 target.dialog.addEventListener('cancel',e=>{if(!captureDraft(kind))e.preventDefault()});
}
window.addEventListener('beforeunload',()=>{for(const kind of Object.keys(draftTargets))captureDraft(kind)});
writeDrafts();
