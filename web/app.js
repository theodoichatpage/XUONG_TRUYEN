'use strict';
const $=s=>document.querySelector(s), esc=Story.esc, id=()=>crypto.randomUUID();
let state,revision,token,currentId=localStorage.getItem('xt-current'),view='library',editing=null,job=null,busy=false;
const pages={library:'Thư viện truyện',bible:'Hồ sơ truyện',characters:'Nhân vật',plans:'Dàn ý',chapters:'Viết chương',memories:'Trí nhớ & nút thắt',publish:'Duyệt & xuất bản'};
const labels={draft:'Bản nháp',review:'Chờ duyệt',approved:'Đã duyệt',live:'Đã đăng'};
const book=()=>state.books.find(b=>b.id===currentId);
function toast(s){$('#toast').textContent=s;$('#toast').classList.add('show');setTimeout(()=>$('#toast').classList.remove('show'),5000)}
async function persist(next){
 if(busy)throw Error('Đang lưu, hãy chờ một chút.');busy=true;
 try{const r=await fetch('/api/state',{method:'POST',headers:{'Content-Type':'application/json','X-Xuong-Token':token},body:JSON.stringify({data:next,revision})}),d=await r.json();if(!r.ok)throw Error(d.error);state=next;revision=d.revision;render()}finally{busy=false}
}
const field=(name,title,value='',type='text')=>`<label>${title}${type==='textarea'?`<textarea name="${name}" rows="5">${esc(value)}</textarea>`:`<input name="${name}" type="${type}" value="${esc(value)}" ${type==='number'?'min="1" max="100000"':''}>`}</label>`;
function select(name,title,values,value){return `<label>${title}<select name="${name}">${values.map(([k,v])=>`<option value="${esc(k)}" ${k===value?'selected':''}>${esc(v)}</option>`).join('')}</select></label>`}
function title(text,sub,action=''){return `<div class="page-head"><div><p class="eyebrow">KHÔNG GIAN SÁNG TÁC</p><h1>${text}</h1><p>${sub}</p></div>${action}</div>`}
function empty(text){return `<section class="empty"><h2>${text}</h2><p>Bắt đầu bằng một ý tưởng, rồi xây từng bước.</p></section>`}
function render(){
 if(!state)return;const b=book();$('#bookSelect').innerHTML='<option value="">Chọn bộ truyện</option>'+state.books.map(x=>`<option value="${x.id}" ${x.id===currentId?'selected':''}>${esc(x.title)}</option>`).join('');
 $('#nav').innerHTML=Object.entries(pages).map(([k,v])=>`<button data-view="${k}" class="${view===k?'active':''}">${v}</button>`).join('');
 if(view==='library'){
 $('#main').innerHTML=title('Thư viện truyện','Một nơi cho ý tưởng, bản thảo và những chương tiếp theo.','<button class="primary" data-new="book">+ Tạo bộ truyện</button>')+`<div class="cards">${state.books.map(x=>`<article class="card"><div class="cover">${esc(x.title.slice(0,1))}</div><div><span class="badge">${esc(x.genre||'Chưa chọn thể loại')}</span><h2>${esc(x.title)}</h2><p>${esc(x.premise||'Chưa có tiền đề')}</p><small>${x.chapters.length} chương · ${x.chapters.filter(c=>c.status==='review').length} chờ duyệt</small><div class="actions"><button class="primary" data-open="${x.id}">Vào bàn viết →</button></div></div></article>`).join('')}</div>`+(state.books.length?'':empty('Tạo bộ truyện đầu tiên'));return;
 }
 if(!b){$('#main').innerHTML=title(pages[view],'Chọn một bộ truyện trong danh sách bên trái.')+empty('Chưa chọn bộ truyện');return}
 let html=title(pages[view],b.title,view==='bible'?'<button class="primary" data-edit-book>Chỉnh hồ sơ</button>':['characters','plans','chapters','memories'].includes(view)?`<button class="primary" data-new="${view}">+ Thêm ${ {characters:'nhân vật',plans:'dàn ý',chapters:'chương',memories:'ghi nhớ'}[view]}</button>`:'');
 if(view==='bible')html+=`<div class="stats"><div><strong>${b.chapters.length}</strong> chương</div><div><strong>${b.characters.length}</strong> nhân vật</div><div><strong>${b.chapters.filter(c=>c.status==='review').length}</strong> chờ duyệt</div></div><div class="two"><section class="panel"><h2>Ý tưởng & định hướng</h2><p class="prose">${esc(b.premise||'Chưa điền')}</p><dl><dt>Thể loại</dt><dd>${esc(b.genre)}</dd><dt>Ngôn ngữ</dt><dd>${esc(b.language)}</dd><dt>Giọng văn</dt><dd>${esc(b.style)}</dd><dt>Độ dài mỗi chương</dt><dd>${b.length} từ</dd><dt>Độc quyền</dt><dd>${esc(b.exclusivity||'Chưa xác nhận')}</dd></dl></section><section class="panel"><h2>Thế giới & quy tắc</h2><p class="prose">${esc(b.world||'Ghi những quy tắc không được tự thay đổi.')}</p></section></div><section class="panel"><h2>Quy trình đề xuất</h2><p>Hồ sơ → Nhân vật → Dàn ý → Viết chương → Kiểm tra → Duyệt → Đăng thủ công.</p><p class="hint">Trí nhớ chỉ được đưa vào yêu cầu viết khi bạn xác nhận. Bản trả về từ AI luôn cần duyệt.</p></section>`;
 if(['characters','plans','memories'].includes(view))html+=b[view].length?`<div class="cards">${b[view].map(r=>`<article class="panel"><span class="badge">${esc(r.type|| (view==='plans'?'Dàn ý':'Nhân vật'))}${view==='memories'?' · '+(r.confirmed?'Đã xác nhận':'Chưa xác nhận'):''}</span><h2>${esc(r.title)}</h2><p class="prose">${esc(r.body)}</p>${view==='memories'?`<small>Ghi nhận ở chương ${esc(r.chapter||0)}</small>`:''}<div class="actions"><button data-edit="${r.id}" data-kind="${view}">Chỉnh sửa</button></div></article>`).join('')}</div>`:empty('Chưa có dữ liệu');
 if(view==='chapters')html+=b.chapters.length?b.chapters.slice().sort((a,z)=>a.number-z.number).map(c=>`<article class="panel chapter"><div><span class="badge ${c.status}">${labels[c.status]}</span><h2>Chương ${c.number} · ${esc(c.title)}</h2><p>${esc(c.intent||'Chưa có ý định chương')}</p><small>${c.body.length.toLocaleString('vi-VN')} ký tự · ${c.history.length} bản lịch sử</small></div><div class="actions"><button data-edit="${c.id}" data-kind="chapters">Mở bản thảo</button><button data-ai="${c.id}">Soạn yêu cầu ChatGPT</button></div></article>`).join(''):empty('Thêm chương đầu tiên');
 if(view==='publish')html+='<p class="notice">Đăng thủ công trên Inkstone. Xưởng không tự đăng, không lưu mật khẩu hay thông tin ngân hàng.</p>'+b.chapters.map(c=>`<article class="panel chapter"><div><span class="badge ${c.status}">${labels[c.status]}</span><h2>Chương ${c.number} · ${esc(c.title)}</h2><p>${esc(c.summary||'Chưa có tóm tắt')}</p></div><div class="actions"><button data-edit="${c.id}" data-kind="chapters">Xem & duyệt</button>${['approved','live'].includes(c.status)?`<button data-export="${c.id}">Xuất TXT</button><a href="https://inkstone.webnovel.com/" target="_blank" rel="noopener">Mở Inkstone ↗</a>`:''}</div></article>`).join('');
 $('#main').innerHTML=html;
}
function openEditor(kind,rowId){
 const b=book(),row=kind==='book'?(rowId?b:undefined):b?.[kind]?.find(x=>x.id===rowId),o=row||{};editing={kind,id:row?.id};$('#dialogTitle').textContent=(row?'Chỉnh sửa ':'Tạo mới ')+({book:'bộ truyện',characters:'nhân vật',plans:'dàn ý',chapters:'chương',memories:'ghi nhớ'}[kind]);$('#formError').textContent='';
 let h=field('title',kind==='book'?'Tên bộ truyện':'Tiêu đề',o.title);
 if(kind==='book')h+=field('genre','Thể loại',o.genre)+field('language','Ngôn ngữ',o.language||'English')+field('length','Số từ mục tiêu / chương',o.length||1500,'number')+field('premise','Tiền đề & mục tiêu truyện',o.premise,'textarea')+field('world','Thế giới & quy tắc',o.world,'textarea')+field('style','Giọng văn',o.style,'textarea')+field('exclusivity','Trạng thái độc quyền',o.exclusivity||'Chưa xác nhận');
 else if(kind==='chapters')h+=field('number','Số chương',o.number||Math.max(0,...b.chapters.map(c=>c.number))+1,'number')+field('intent','Ý định chương / những sự kiện cần xảy ra',o.intent,'textarea')+field('body','Nội dung chương',o.body,'textarea')+field('summary','Tóm tắt đã kiểm tra để nối chương',o.summary,'textarea')+select('status','Trạng thái',Object.entries(labels),o.status||'draft')+field('link','Link chương đã đăng',o.link,'url')+(o.history?.length?`<details><summary>Lịch sử (${o.history.length} bản) — sao chép để khôi phục</summary>${o.history.slice().reverse().map(v=>`<h3>${esc(v.at)}</h3><pre>${esc(v.body)}</pre>`).join('')}</details>`:'');
 else {if(kind==='memories')h+=select('type','Loại ghi nhớ',[['Sự kiện','Sự kiện'],['Nút thắt','Nút thắt'],['Dòng thời gian','Dòng thời gian'],['Quy tắc','Quy tắc']],o.type||'Sự kiện')+field('chapter','Chương ghi nhận',o.chapter||1,'number')+select('confirmed','Xác nhận để dùng khi viết',[['no','Chưa xác nhận'],['yes','Đã xác nhận']],o.confirmed?'yes':'no');h+=field('body',kind==='characters'?'Vai trò, mục tiêu, tính cách, quan hệ':'Nội dung',o.body,'textarea')}
 $('#fields').innerHTML=h;$('#editor').showModal();
}
$('#form').onsubmit=async e=>{e.preventDefault();const v=Object.fromEntries(new FormData(e.target)),next=structuredClone(state),b=next.books.find(b=>b.id===currentId),{kind}=editing;try{
 if(!v.title.trim())throw Error('Nhập tiêu đề.');let old=kind==='book'?(editing.id?b:undefined):b[kind].find(r=>r.id===editing.id),row={...old,...v,id:editing.id||id()};
 if(kind==='book'){row.length=Number(v.length);if(!Number.isInteger(row.length)||row.length<1)throw Error('Độ dài không hợp lệ');for(const k of ['characters','plans','chapters','memories'])row[k]=old?.[k]||[];if(editing.id)next.books=next.books.map(r=>r.id===row.id?row:r);else next.books.push(row)}
 else {if(kind==='chapters'){
 row.number=Number(v.number);if(!Number.isInteger(row.number)||row.number<1||b.chapters.some(c=>c.number===row.number&&c.id!==row.id))throw Error('Số chương phải là số nguyên dương, không trùng.');
 if(row.status!=='draft'&&!row.body.trim())throw Error('Cần có nội dung chương.');
 if(row.status==='live'&&(!old||!['approved','live'].includes(old.status)))throw Error('Lưu Đã duyệt trước, rồi đăng và xác nhận.');
 if(row.status==='live'&&!/^https:\/\/([\w-]+\.)*(webnovel\.com)\//i.test(row.link))throw Error('Nhập link chương HTTPS trên Webnovel.');
 if(old&&old.body!==row.body&&['approved','live'].includes(row.status))throw Error('Nội dung thay đổi: chuyển Chờ duyệt trước khi duyệt lại.');
 row.history=old?.history||[];row.revision=(old?.revision||0)+1;if(old&&(old.body!==row.body||old.summary!==row.summary))row.history.push({body:old.body,summary:old.summary,status:old.status,at:new Date().toISOString()});
 }if(kind==='memories'){row.confirmed=v.confirmed==='yes';row.chapter=Number(v.chapter)}
 if(editing.id)b[kind]=b[kind].map(r=>r.id===row.id?row:r);else b[kind].push(row)}
 await persist(next);if(kind==='book'){currentId=row.id;localStorage.setItem('xt-current',currentId);view='bible';render()}$('#editor').close();toast('Đã lưu')
 }catch(e){$('#formError').textContent=e.message}};
function closeEditor(){if($('#form').matches(':focus-within')&&!confirm('Đóng cửa sổ? Các thay đổi chưa lưu sẽ không được giữ.'))return;$('#editor').close()}
$('#close').onclick=$('#cancel').onclick=closeEditor;$('#editor').oncancel=e=>{e.preventDefault();closeEditor()};$('#closeAI').onclick=()=>$('#ai').close();
$('#bookSelect').onchange=e=>{currentId=e.target.value;localStorage.setItem('xt-current',currentId);render()};
document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
 if(b.dataset.view){view=b.dataset.view;render()}
 if(b.dataset.new)openEditor(b.dataset.new);
 if(b.hasAttribute('data-edit-book'))openEditor('book',currentId);
 if(b.dataset.open){currentId=b.dataset.open;localStorage.setItem('xt-current',currentId);view='bible';render()}
 if(b.dataset.edit)openEditor(b.dataset.kind,b.dataset.edit);
 if(b.dataset.ai){const c=book().chapters.find(c=>c.id===b.dataset.ai);job={bookId:book().id,chapterId:c.id,revision:c.revision||0};$('#prompt').value=Story.context(book(),c);$('#result').value='';$('#ai').showModal()}
 if(b.dataset.export){const c=book().chapters.find(c=>c.id===b.dataset.export);download('chuong-'+c.number+'.txt',c.title+'\n\n'+c.body,'text/plain')}
});
$('#copy').onclick=async()=>{try{await navigator.clipboard.writeText($('#prompt').value);toast('Đã sao chép')}catch{$('#prompt').select();toast('Bấm Ctrl+C để sao chép')}};
$('#receive').onclick=async()=>{try{const next=structuredClone(state),b=next.books.find(b=>b.id===job.bookId),c=b?.chapters.find(c=>c.id===job.chapterId);if(!c||(c.revision||0)!==job.revision)throw Error('Chương đã thay đổi. Sao chép kết quả rồi mở bản thảo để kiểm tra.');Story.acceptChapter(c,$('#result').value,new Date().toISOString());await persist(next);$('#ai').close();toast('Đã nhận kết quả, chờ bạn duyệt')}catch(e){toast(e.message)}};
function download(name,text,type){const u=URL.createObjectURL(new Blob([text],{type})),a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000)}
$('#backup').onclick=()=>download('xuong-truyen-'+new Date().toISOString().slice(0,10)+'.json',JSON.stringify(state,null,2),'application/json');$('#restore').onclick=()=>$('#file').click();$('#file').onchange=async e=>{try{const f=e.target.files[0];if(!f)return;if(f.size>20_000_000)throw Error('Tệp quá lớn');const next=JSON.parse(await f.text());if(!confirm('Thay dữ liệu hiện tại bằng bản sao lưu? Hãy xuất sao lưu hiện tại trước.'))return;await persist(next);currentId=state.books[0]?.id;view='library';render();toast('Đã nhập sao lưu')}catch(e){toast(e.message)}finally{e.target.value=''}};
fetch('/api/state').then(async r=>{if(!r.ok)throw Error('Không đọc được dữ liệu');return r.json()}).then(d=>{state=d.data;revision=d.revision;token=d.token;render()}).catch(e=>{$('#main').textContent=e.message});
