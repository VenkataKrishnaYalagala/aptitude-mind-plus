import {EXAMS,json,fail,backendReady,checkOrigin,text,validEmail,validUrl,parseJSON,rateLimit,handleError} from './_helpers.js';
const PUBLIC_FIELDS='id,exam,topic,question,answer,exam_year,source_url,verified_official,created_at';
export async function onRequestGet({request,env}){
 if(!env.DB)return json({items:[],more:false});
 try{
  const params=new URL(request.url).searchParams;const limit=Math.max(1,Math.min(Number(params.get('limit'))||12,30)),offset=Math.max(0,Math.min(Number(params.get('offset'))||0,3000));
  const exam=params.get('exam')||'all',type=params.get('type')||'all',q=text(params.get('q')||'',90);
  let where=' WHERE status=?',values=['approved'];
  if(EXAMS.has(exam)){where+=' AND exam=?';values.push(exam);}
  if(type==='official'||type==='community'){where+=' AND verified_official=?';values.push(type==='official'?1:0);}
  if(q){where+=" AND (question LIKE ? ESCAPE '\\' OR topic LIKE ? ESCAPE '\\')";const safe=q.replace(/[\\%_]/g,'\\$&');values.push('%'+safe+'%','%'+safe+'%');}
  const sql=`SELECT ${PUBLIC_FIELDS},EXISTS(SELECT 1 FROM question_images im WHERE im.question_id=questions.id) AS has_image FROM questions`+where+' ORDER BY created_at DESC,id DESC LIMIT ? OFFSET ?';
  const result=await env.DB.prepare(sql).bind(...values,limit+1,offset).all();const rows=result.results||[];
  return json({items:rows.slice(0,limit),more:rows.length>limit});
 }catch(err){return handleError(err);}
}
export async function onRequestPost({request,env}){
 if(!backendReady(env))return fail('Submissions are not enabled yet. The site owner must connect the database and admin secrets.',503);
 if(!checkOrigin(request))return fail('Invalid request origin.',403);
 try{
  const d=await parseJSON(request);if(!EXAMS.has(d.exam))return fail('Choose a valid exam.');
  const topic=text(d.topic,100),question=text(d.question,3000),answer=text(d.answer,1800),name=text(d.name,90),email=text(d.email,160),source=text(d.source_url,500);
  if(topic.length<2||topic.length>100||(!question&&!d.image_data))return fail('Provide a topic and question text or a clear image.');
  if(d.rights_confirmed!==true)return fail('Please confirm that you are authorised to share this question.');
  if(!validEmail(email))return fail('The email address is invalid.');if(!validUrl(source))return fail('Only valid HTTPS source links are accepted.');
  let year=null;if(d.exam_year!==null&&d.exam_year!==undefined&&d.exam_year!==''){year=Number(d.exam_year);if(!Number.isInteger(year)||year<1950||year>new Date().getUTCFullYear()+1)return fail('Choose a valid exam year.');}
  const data=d.image_data;
  let jpeg=null;
  if(data!==null&&data!==undefined&&data!==''){
   const prefix='data:image/jpeg;base64,';
   if(typeof data!=='string'||!data.startsWith(prefix)||data.length>780000||!/^[a-zA-Z0-9+/]+={0,2}$/.test(data.slice(prefix.length)))return fail('A compressed JPEG image is required.');
   try{jpeg=Uint8Array.from(atob(data.slice(prefix.length)),c=>c.charCodeAt(0));}catch{return fail('The image encoding is invalid.');}
   if(jpeg.length<4||jpeg.length>585000||jpeg[0]!==255||jpeg[1]!==216||jpeg[2]!==255||jpeg.at(-2)!==255||jpeg.at(-1)!==217)return fail('Only small, valid JPEG uploads are accepted.');
  }
  if(!(await rateLimit(env,request,'question',5)))return fail('Submission limit reached for today. Try again tomorrow.',429);
  const id=crypto.randomUUID();
  let objectKey=null;
  try{
   if(jpeg){
    objectKey=`submitted-questions/${id}.jpg`;
    await env.UPLOADS.put(objectKey,jpeg,{httpMetadata:{contentType:'image/jpeg'}});
   }
   const ops=[env.DB.prepare('INSERT INTO questions(id,exam,topic,question,answer,exam_year,source_url,contributor_name,contributor_email,status) VALUES(?,?,?,?,?,?,?,?,?,\'pending\')').bind(id,d.exam,topic,question||'(Question supplied as an image)',answer,year,source,name,email)];
   if(objectKey)ops.push(env.DB.prepare('INSERT INTO question_images(question_id,mime_type,object_key) VALUES(?,?,?)').bind(id,'image/jpeg',objectKey));
   await env.DB.batch(ops);
  }catch(err){
   if(objectKey){try{await env.UPLOADS.delete(objectKey);}catch{console.error('Failed to clean up orphaned upload');}}
   throw err;
  }
  return json({id,status:'pending'},201);
 }catch(err){return handleError(err);}
}
