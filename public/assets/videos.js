/* Free video lesson library. Videos load only after the learner clicks Play. */
(()=>{
 'use strict';
 const cards=[...document.querySelectorAll('[data-lesson-exam]')];
 if(!cards.length)return;
 const filters=[...document.querySelectorAll('[data-video-filter]')];
 const search=document.querySelector('[data-video-search]');
 const noResults=document.querySelector('[data-video-none]');
 const allowed=['all','upsc','gate','ssc','bank','state','rail'];
 const params=new URLSearchParams(window.location.search);
 let exam=allowed.includes(params.get('exam'))?params.get('exam'):'all';
 if(search)search.value=(params.get('q')||'').slice(0,90);
 const render=()=>{
   const q=(search?.value||'').trim().toLocaleLowerCase();
   let matches=0;
   cards.forEach(card=>{
     const inExam=exam==='all'||card.dataset.lessonExam==='all'||card.dataset.lessonExam===exam;
     const found=inExam&&(!q||card.dataset.lessonSearch?.includes(q));
     card.hidden=!found;
     if(found)matches++;
   });
   filters.forEach(btn=>{
     const active=btn.dataset.videoFilter===exam;
     btn.classList.toggle('active',active);
     btn.setAttribute('aria-pressed',String(active));
   });
   if(noResults)noResults.hidden=matches!==0;
 };
 filters.forEach(btn=>btn.addEventListener('click',()=>{exam=btn.dataset.videoFilter;render();}));
 search?.addEventListener('input',render);
 render();
 document.querySelectorAll('[data-play-video]').forEach(btn=>btn.addEventListener('click',()=>{
   const videoId=btn.dataset.playVideo;
   if(!/^[a-zA-Z0-9_-]{11}$/.test(videoId))return;
   const frame=btn.closest('[data-video-frame]');
   if(!frame)return;
   const player=document.createElement('iframe');
   player.title='YouTube video player';
   player.src='https://www.youtube-nocookie.com/embed/'+videoId+'?autoplay=1&rel=0&playsinline=1';
   player.width='640';player.height='360';
   player.loading='lazy';
   player.setAttribute('referrerpolicy','strict-origin-when-cross-origin');
   player.allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share';
   player.allowFullscreen=true;
   frame.replaceChildren(player);
 }));
})();
