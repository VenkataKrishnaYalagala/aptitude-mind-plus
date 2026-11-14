import React, { useCallback, useEffect, useMemo, useState } from 'react';
import {createRoot} from 'react-dom/client';
import {Puck} from '@puckeditor/core';
import '@puckeditor/core/no-external.css';
import {config} from './config.jsx';
import initialData from '../../content/homepage.visual.json';
import './editor.css';

const DRAFT_KEY = 'amp-homepage-draft-v1';
function restoreDraft() {
  try {
    const text=window.localStorage.getItem(DRAFT_KEY);
    if (text && text.length < 110000) return JSON.parse(text);
  } catch {/* Storage may be disabled; the editor still works. */}
  return initialData;
}

function saveFile(data) {
  const bytes=new Blob([JSON.stringify(data,null,2)+'\n'],{type:'application/json'});
  const url=URL.createObjectURL(bytes);
  const a=document.createElement('a');a.href=url;a.download='aptitude-mind-plus-homepage-draft.json';a.click();
  window.setTimeout(()=>URL.revokeObjectURL(url),1000);
}

function App() {
  const [layout,setLayout]=useState(restoreDraft);
  const [editorKey,setEditorKey]=useState(0);
  const [saved,setSaved]=useState(initialData);
  const [baseSha,setBaseSha]=useState(null);
  const [authorized,setAuthorized]=useState(false);
  const [backendConnected,setBackendConnected]=useState(false);
  const [status,setStatus]=useState('Local draft mode. Sign in to publish changes.');
  const [busy,setBusy]=useState(false);
  const isLocal=useMemo(()=>location.hostname==='localhost'||location.hostname==='127.0.0.1',[]);
  useEffect(()=>{
    if(isLocal)return;
    let active=true;
    (async()=>{
      try {
        const session=await fetch('/api/admin/session',{credentials:'same-origin',cache:'no-store'});
        if(!session.ok)return;
        const auth=await session.json();
        if(!auth.authenticated)return;
        const response=await fetch('/api/editor/home',{credentials:'same-origin',cache:'no-store'});
        if(!response.ok)return;
        const page=await response.json();
        if(active && page.data && page.sha){
          setSaved(page.data);setBaseSha(page.sha);setAuthorized(true);setBackendConnected(true);
          if(!localStorage.getItem(DRAFT_KEY)){setLayout(page.data);setEditorKey(key=>key+1);}
          setStatus('Signed in. Review your changes before publishing.');
        }
      } catch { if(active)setStatus('Secure publishing is unavailable. Your edits remain local drafts.'); }
    })();
    return()=>{active=false};
  },[isLocal]);
  const onChange=useCallback((data)=>{
    setLayout(data);
    try{localStorage.setItem(DRAFT_KEY,JSON.stringify(data))}catch{}
  },[]);
  const publish=useCallback(async (data)=>{
    setLayout(data);
    try{localStorage.setItem(DRAFT_KEY,JSON.stringify(data))}catch{}
    if(!authorized||!backendConnected||!baseSha){
      setStatus('Not published. This is a local draft: sign in as the site administrator and configure the secure publishing API first.');
      return;
    }
    if(!window.confirm('Publish these homepage changes to the public site?'))return;
    setBusy(true);setStatus('Saving reviewed homepage to GitHub...');
    try{
      const response=await fetch('/api/editor/home',{
        method:'PUT',credentials:'same-origin',cache:'no-store',
        headers:{'Content-Type':'application/json','X-AMP-Editor':'1'},
        body:JSON.stringify({data,sha:baseSha})
      });
      const result=await response.json().catch(()=>({error:'Invalid server response'}));
      if(!response.ok)throw new Error(result.error||'Unable to publish');
      setBaseSha(result.sha);setSaved(data);
      localStorage.removeItem(DRAFT_KEY);
      setStatus('Saved to GitHub. Publishing runs automatically; check Actions and Cloudflare for confirmation.');
    }catch(error){setStatus('Not published: '+error.message+' Your draft is still saved locally.');}
    finally{setBusy(false)}
  },[authorized,backendConnected,baseSha]);
  const reset=()=>{
    if(!window.confirm('Discard your local draft and restore the last loaded homepage?'))return;
    localStorage.removeItem(DRAFT_KEY);setLayout(saved);setEditorKey(x=>x+1);
    setStatus('Local draft reset. The public website was not changed.');
  };
  return <div className="amp-editor-shell">
    <header className="amp-editor-banner">
      <div className="amp-editor-brand"><span className="amp-editor-mark">A+</span><span><strong>Aptitude Mind Plus</strong><small>Visual homepage editor — pilot</small></span></div>
      <div className="amp-editor-info" role="status" aria-live="polite">{status}</div>
      <div className="amp-editor-buttons">
        <button type="button" onClick={()=>saveFile(layout)} title="Download a backup of your current draft">Export draft</button>
        <button type="button" onClick={reset}>Reset draft</button>
        <a href="/index.html" target="_blank" rel="noopener noreferrer">View website ↗</a>
      </div>
    </header>
    <div className="amp-editor-note"><span className="amp-editor-dot"/>
      {busy?'Publishing in progress…':authorized?'Private publishing enabled. Puck Publish commits to GitHub after confirmation.':'Preview and draft editing are available. Publishing stays disabled until administrator authentication is configured.'}
    </div>
    <Puck key={editorKey} config={config} data={layout} onChange={onChange} onPublish={publish} headerTitle="Aptitude Mind Plus / Homepage" headerPath="/index.html" dnd={{enableDragHandle:true}} viewports={[{width:1360},{width:768},{width:390}]} />
  </div>;
}

createRoot(document.getElementById('root')).render(<App/>);
