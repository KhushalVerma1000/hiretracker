(()=>{const f=document.getElementById('lead-form');if(!f)return;
const t0=Date.now(),q=new URLSearchParams(location.search),st=f.querySelector('.status'),btn=f.querySelector('button[type=submit]');
const utm=k=>(q.get(k)||'').slice(0,100);
const say=(m,bad)=>{st.textContent=m;st.style.color=bad?'#C0392B':'inherit'};
f.addEventListener('submit',async e=>{e.preventDefault();
f.querySelectorAll('.err').forEach(x=>x.textContent='');say('');
const g=n=>f.elements[n].value;
const body={name:g('name'),email:g('email'),phone:g('phone'),company:g('company'),role:g('role'),companyType:g('companyType'),teamSize:g('teamSize'),challenge:g('challenge'),consent:f.elements.consent.checked,
utmSource:utm('utm_source'),utmMedium:utm('utm_medium'),utmCampaign:utm('utm_campaign'),ts:t0,hp:g('hp')};
btn.disabled=true;say('Sending...');
try{const r=await fetch('/api/lead',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
const j=await r.json().catch(()=>({}));
if(r.ok&&j.ok){const d=document.createElement('div');d.className='thanks';d.setAttribute('role','status');
const h=document.createElement('h3');h.textContent='You are in!';const p=document.createElement('p');p.textContent='Thanks for requesting your free trial. Check your email for a confirmation. We will be in touch shortly.';
d.append(h,p);f.replaceWith(d);return}
if(j.errors){for(const k in j.errors){const el=f.querySelector('[data-err="'+k+'"]');if(el)el.textContent=j.errors[k]}say(j.errors.form||'Please fix the highlighted fields.',true)}
else say(j.error||'Something went wrong. Please try again.',true)}
catch{say('Network error. Please try again.',true)}
btn.disabled=false})})();
