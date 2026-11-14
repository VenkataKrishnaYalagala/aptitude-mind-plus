import {EXAMS,json,fail,backendReady,checkOrigin,text,validEmail,parseJSON,rateLimit,handleError} from './_helpers.js';

// A private student enquiry; never returned through a public read endpoint.
export async function onRequestPost({request,env}){
 if(!backendReady(env))return fail('Student doubts are not available until the private backend is configured.',503);
 if(!checkOrigin(request))return fail('Invalid request origin.',403);
 try{
  const data=await parseJSON(request,9000);
  if(text(data.website,200))return fail('Request could not be accepted.',400);
  const exam=text(data.exam,20),topic=text(data.topic,90),question=text(data.question,3000);
  const email=text(data.email,160),name=text(data.name,90);
  if(!EXAMS.has(exam)||topic.length<2||question.length<20||name.length<2||!email||!validEmail(email))return fail('Enter your name, a valid email address, exam, topic and a question with at least 20 characters.');
  if(data.consent!==true)return fail('Permission to contact you is required.');
  if(!(await rateLimit(env,request,'student_doubt',3)))return fail('Too many questions sent today. Please try again tomorrow.',429);
  const id=crypto.randomUUID();
  await env.DB.prepare('INSERT INTO student_doubts(id,exam,topic,question,student_name,student_email) VALUES(?,?,?,?,?,?)')
   .bind(id,exam,topic,question,name,email).run();
  return json({id,status:'received',published:false},201);
 }catch(e){return handleError(e);}
}
