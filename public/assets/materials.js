/* Fast client-side filtering; no analytics, requests or tracking. */
(()=>{
 'use strict';
 const items=[...document.querySelectorAll('[data-material]')];
 if(!items.length)return;
 const input=document.querySelector('[data-material-search]');
 const controls=[...document.querySelectorAll('[data-material-filter]')];
 const count=document.querySelector('[data-material-count]');
 const empty=document.querySelector('[data-material-empty]');
 let access='all';
 const render=()=>{
  const q=(input?.value||'').trim().toLocaleLowerCase();
  let shown=0;
  for(const item of items){
    const visible=(access==='all'||item.dataset.access===access)&&(!q||item.dataset.search.includes(q));
    item.hidden=!visible;if(visible)shown++;
  }
  controls.forEach(btn=>{const active=btn.dataset.materialFilter===access;btn.classList.toggle('is-active',active);btn.setAttribute('aria-pressed',String(active));});
  if(count)count.textContent=`${shown} ${shown===1?'resource':'resources'} found`;
  if(empty)empty.hidden=shown>0;
 };
 input?.addEventListener('input',render);
 controls.forEach(btn=>btn.addEventListener('click',()=>{access=btn.dataset.materialFilter;render();}));
 render();
})();
