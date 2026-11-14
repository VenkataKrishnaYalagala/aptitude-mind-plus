/* Static past-paper search. No external requests, analytics or personal data. */
(()=>{
 'use strict';
 const records=[...document.querySelectorAll('[data-pyq-record]')];if(!records.length)return;
 const input=document.querySelector('[data-pyq-search]');
 const get=type=>document.querySelector('[data-pyq-'+type+']');
 const exam=get('exam'),year=get('year'),topic=get('topic'),concept=get('concept');
 const count=get('count'),empty=get('empty');
 const params=new URLSearchParams(location.search);
 if(['upsc','gate','ssc','bank','state','rail'].includes(params.get('exam')))exam.value=params.get('exam');
 if(/^\d{4}$/.test(params.get('year')||'')&&[...year.options].some(o=>o.value===params.get('year')))year.value=params.get('year');
 function refresh(){
  const q=(input?.value||'').trim().toLowerCase();let n=0;
  records.forEach(card=>{
   const visible=(exam.value==='all'||card.dataset.exam===exam.value)
    &&(year.value==='all'||card.dataset.year===year.value)
    &&(topic.value==='all'||card.dataset.topic===topic.value)
    &&(concept.value==='all'||card.dataset.concept===concept.value)
    &&(!q||(card.dataset.search||'').includes(q));
   card.hidden=!visible;if(visible)n++;
  });
  count.textContent=n+' record'+(n===1?'':'s')+' found';empty.hidden=n!==0;
 }
 [input,exam,year,topic,concept].forEach(el=>el?.addEventListener(el===input?'input':'change',refresh));
 document.querySelectorAll('[data-pyq-clear]').forEach(b=>b.addEventListener('click',()=>{
  if(input)input.value='';exam.value=year.value=topic.value=concept.value='all';refresh();input?.focus();
 }));
 refresh();
})();
