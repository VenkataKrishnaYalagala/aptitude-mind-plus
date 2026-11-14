import {json,fail,isAdmin,checkOrigin,text,parseJSON,handleError} from '../_helpers.js';
export async function onRequestPost({request,env}){
 if(!(await isAdmin(request,env)))return fail('Administrator sign-in required.',401);
 if(!checkOrigin(request))return fail('Invalid request origin.',403);
 try{
  const data=await parseJSON(request,3500);
  const id=text(data.id,60),status=text(data.status,20),note=text(data.private_notes,1000);
  if(!/^[a-f0-9-]{36}$/i.test(id)||!['answered','archived','new'].includes(status))return fail('Invalid reference or status.');
  const result=await env.DB.prepare("UPDATE student_doubts SET status=?,private_notes=?,reviewed_at=datetime('now') WHERE id=?")
   .bind(status,note,id).run();
  if(!result.meta?.changes)return fail('Student doubt not found.',404);
  return json({id,status});
 }catch(e){return handleError(e);}
}
