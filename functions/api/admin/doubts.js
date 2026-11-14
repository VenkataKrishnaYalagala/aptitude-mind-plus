import {json,fail,isAdmin,handleError} from '../_helpers.js';
export async function onRequestGet({request,env}){
 if(!(await isAdmin(request,env)))return fail('Administrator sign-in required.',401);
 try{
  const filter=new URL(request.url).searchParams.get('status');
  const status=filter==='new'?'new':filter==='handled'?'handled':'all';
  const where=status==='new'?" WHERE status='new'":status==='handled'?" WHERE status!='new'":'';
  const items=await env.DB.prepare('SELECT id,exam,topic,question,student_name,student_email,status,created_at,reviewed_at,private_notes FROM student_doubts'+where+' ORDER BY created_at DESC,id DESC LIMIT 100').all();
  const pending=await env.DB.prepare("SELECT COUNT(*) AS n FROM student_doubts WHERE status='new'").first();
  return json({items:items.results||[],pending_count:pending?.n||0});
 }catch(e){return handleError(e);}
}
