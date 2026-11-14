import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {validateLayout} from '../functions/api/editor/_schema.js';
import {onRequestPut,onRequestGet} from '../functions/api/editor/home.js';
import {makeSession} from '../functions/api/_helpers.js';

const seed=JSON.parse(readFileSync(new URL('../content/homepage.visual.json',import.meta.url),'utf8'));
const clone=x=>structuredClone(x);
const env={
  DB:{prepare:()=>({bind:()=>({run:async()=>{},first:async()=>({hits:1})})})},
  UPLOADS:{get:async()=>null,put:async()=>{},delete:async()=>{}},
  ADMIN_PASSWORD:'some-very-long-not-real-test-password',
  SESSION_SECRET:'testing-secret-with-more-than-thirty-two-characters',
  GITHUB_CONTENT_TOKEN:'fake-token-for-secure-test-only-nonworking'
};

test('valid visual page passes schema checks',()=>assert.equal(validateLayout(seed),null));
test('all supported block types are in the sample schema',()=>assert.deepEqual(seed.content.map(x=>x.type),['Hero','QuickLinks','CourseShelf','FreeLesson','MaterialsShelf','CommunitySpotlight','TutorCTA']));
test('rejects HTML tags only when used as dangerous link targets',()=>{
 const x=clone(seed);x.content[0].props.primaryHref='javascript:alert(1)';assert.match(validateLayout(x),/destination/);
});
test('rejects new page types',()=>{const x=clone(seed);x.content[0].type='ScriptInjection';assert.ok(validateLayout(x));});
test('rejects remote uploaded image URLs',()=>{const x=clone(seed);x.content.push({type:'ImageSection',props:{id:'test',src:'https://evil.example/x.png'}});assert.match(validateLayout(x),/media/)});
test('allows approved local image references',()=>{const x=clone(seed);x.content.push({type:'ImageSection',props:{id:'test',src:'/media/official-logo.png',alt:'Brand logo'}});assert.equal(validateLayout(x),null)});
test('rejects traversal even with local media path',()=>{const x=clone(seed);x.content.push({type:'ImageSection',props:{id:'test',src:'/media/../private.png'}});assert.ok(validateLayout(x))});
test('rejects duplicate ids',()=>{const x=clone(seed);x.content[1].props.id=x.content[0].props.id;assert.ok(validateLayout(x));});
test('rejects too many sections',()=>{const x=clone(seed);for(let i=0;i<24;i++)x.content.push({type:'Spacer',props:{id:'x'+i,size:'small'}});assert.ok(validateLayout(x))});
test('rejects raw HTML as new component property',()=>{const x=clone(seed);x.content[0].props.dangerouslySetInnerHTML={__html:'<script>x</script>'};assert.ok(validateLayout(x))});
test('rejects invalid global fonts',()=>{const x=clone(seed);x.root.props.fontStyle='url(https://evil.example/)';assert.ok(validateLayout(x))});

test('public users cannot GET the editor content',async()=>{
 const req=new Request('https://example.pages.dev/api/editor/home');const resp=await onRequestGet({request:req,env});assert.equal(resp.status,401)
});
test('public users cannot publish',async()=>{
 const req=new Request('https://example.pages.dev/api/editor/home',{method:'PUT',headers:{Origin:'https://example.pages.dev','content-type':'application/json','X-AMP-Editor':'1'},body:JSON.stringify({data:seed,sha:'a'.repeat(40)})});
 const resp=await onRequestPut({request:req,env});assert.equal(resp.status,401)
});
test('authenticated user cannot publish cross-origin requests',async()=>{
 const token=await makeSession(env.SESSION_SECRET);
 const req=new Request('https://example.pages.dev/api/editor/home',{method:'PUT',headers:{Origin:'https://bad.example','Cookie':`amp_admin=${token}`,'content-type':'application/json','X-AMP-Editor':'1'},body:JSON.stringify({data:seed,sha:'a'.repeat(40)})});
 const resp=await onRequestPut({request:req,env});assert.equal(resp.status,403)
});
test('fails closed without encrypted GitHub token',async()=>{
 const token=await makeSession(env.SESSION_SECRET);
 const req=new Request('https://example.pages.dev/api/editor/home',{headers:{Cookie:`amp_admin=${token}`}});
 const resp=await onRequestGet({request:req,env:{...env,GITHUB_CONTENT_TOKEN:undefined}});assert.equal(resp.status,503)
});
