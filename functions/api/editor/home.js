// Only the signed-in site owner may publish to a single GitHub content file.
// GITHUB_CONTENT_TOKEN must be an ENCRYPTED Cloudflare Pages secret with
// Contents: read/write for this repository only. It must never reach the browser.
import {fail,json,isAdmin,checkOrigin,parseJSON} from '../_helpers.js';
import {validateLayout} from './_schema.js';
const PATH='content/homepage.visual.json';
const API=`https://api.github.com/repos/VenkataKrishnaYalagala/aptitude-mind-plus/contents/${PATH}`;
const headers=env=>({
  'Authorization':`Bearer ${env.GITHUB_CONTENT_TOKEN}`,
  'Accept':'application/vnd.github+json',
  'X-GitHub-Api-Version':'2022-11-28',
  'User-Agent':'AptitudeMindPlus-PrivateEditor',
  'Content-Type':'application/json'
});
function utf8FromBase64(encoded){
 const raw=atob(encoded.replace(/\s/g,''));
 return new TextDecoder().decode(Uint8Array.from(raw,c=>c.charCodeAt(0)));
}
function base64Utf8(source){
 const bytes=new TextEncoder().encode(source);let out='';
 for(let i=0;i<bytes.length;i+=8192)out+=String.fromCharCode(...bytes.slice(i,i+8192));
 return btoa(out);
}
function configured(env){return typeof env.GITHUB_CONTENT_TOKEN==='string'&&env.GITHUB_CONTENT_TOKEN.length>=24;}
async function readGithub(env){
 const response=await fetch(API+'?ref=main',{headers:headers(env),redirect:'error',signal:AbortSignal.timeout(9000)});
 if(!response.ok)throw new Error(response.status===401?'GitHub token is unauthorized.':`GitHub read failed (${response.status}).`);
 const body=await response.json();
 return {sha:body.sha,data:JSON.parse(utf8FromBase64(body.content))};
}
export async function onRequestGet({request,env}){
 if(!(await isAdmin(request,env)))return fail('Sign in as the site administrator.',401);
 if(!configured(env))return fail('Secure GitHub publishing is not configured.',503);
 try{
  const page=await readGithub(env);
  if(validateLayout(page.data))return fail('Published homepage file needs repair.',503);
  return json(page);
 }catch(err){console.error('Editor read failed:',err.message);return fail('Could not load the latest published homepage.',502);}
}
export async function onRequestPut({request,env}){
 if(!(await isAdmin(request,env)))return fail('Sign in as the site administrator.',401);
 if(!configured(env))return fail('Secure GitHub publishing is not configured.',503);
 if(!checkOrigin(request)||request.headers.get('X-AMP-Editor')!=='1')return fail('Request not allowed.',403);
 try{
  const body=await parseJSON(request,110000);
  const error=validateLayout(body?.data);
  if(error)return fail(error,400);
  if(typeof body.sha!=='string'||!/^[a-f0-9]{40}$/.test(body.sha))return fail('Missing saved revision. Reload the editor.',409);
  const latest=await readGithub(env);
  if(latest.sha!==body.sha)return fail('Someone updated this page. Download your draft, reload, and review the newer version before publishing.',409);
  const content=base64Utf8(JSON.stringify(body.data,null,2)+'\n');
  const response=await fetch(API,{
   method:'PUT',headers:headers(env),redirect:'error',signal:AbortSignal.timeout(12000),
   body:JSON.stringify({message:'content: publish visual homepage editor changes',content,sha:latest.sha,branch:'main'})
  });
  if(!response.ok){console.error('GitHub publisher rejected update:',response.status);return fail(response.status===409?'The page changed while saving. Reload and review before trying again.':'GitHub rejected this publish request.',response.status===409?409:502);}
  const result=await response.json();
  return json({saved:true,sha:result.content?.sha||'',status:'pending-build'},202);
 }catch(error){console.error('Editor publish error:',error?.name||'Error');return fail('Publishing failed safely. Your draft was not changed on the website.',502);}
}
