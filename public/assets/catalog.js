/* Local-only catalog filtering. No tracking, accounts or external services. */
(() => {
  'use strict';
  const root=document.querySelector('[data-catalog]');
  if(!root)return;
  const input=document.querySelector('[data-course-search]');
  const grid=root.querySelector('[data-course-grid]');
  const cards=[...root.querySelectorAll('[data-market-course]')];
  const buttons=[...root.querySelectorAll('[data-course-filter]')];
  const count=root.querySelector('[data-course-count]');
  const empty=root.querySelector('[data-course-empty]');
  const sort=root.querySelector('[data-course-sort]');
  const params=new URLSearchParams(location.search);
  const allowed=['all',...cards.map(card=>card.dataset.exam)];
  let exam=allowed.includes(params.get('exam'))?params.get('exam'):'all';
  if(input)input.value=(params.get('q')||'').slice(0,90);

  function render(){
    const query=(input?.value||'').trim().toLocaleLowerCase();
    const matches=cards.filter(card=>(exam==='all'||card.dataset.exam===exam)&&(!query||card.dataset.search.includes(query)));
    const visible=new Set(matches);
    cards.forEach(card=>{card.hidden=!visible.has(card);});
    buttons.forEach(button=>{
      const selected=button.dataset.courseFilter===exam;
      button.classList.toggle('active',selected);
      button.setAttribute('aria-pressed',String(selected));
    });
    if(sort?.value==='az')cards.slice().sort((a,b)=>a.querySelector('h3').textContent.localeCompare(b.querySelector('h3').textContent)).forEach(card=>grid.append(card));
    else cards.forEach(card=>grid.append(card));
    count.textContent=`${matches.length} ${matches.length===1?'course':'courses'}`;
    empty.hidden=matches.length!==0;
    const share=new URL(location.href);
    if(exam==='all')share.searchParams.delete('exam');else share.searchParams.set('exam',exam);
    if(query)share.searchParams.set('q',query);else share.searchParams.delete('q');
    if(location.protocol==='http:'||location.protocol==='https:')history.replaceState(null,'',share.pathname+share.search+share.hash);
  }
  buttons.forEach(button=>button.addEventListener('click',()=>{exam=button.dataset.courseFilter;render();}));
  input?.addEventListener('input',render);
  sort?.addEventListener('change',render);
  document.querySelectorAll('[data-course-clear]').forEach(button=>button.addEventListener('click',()=>{exam='all';if(input)input.value='';if(sort)sort.value='default';render();input?.focus();}));
  document.querySelector('.catalog-search')?.addEventListener('submit',event=>{event.preventDefault();render();});
  render();
})();
