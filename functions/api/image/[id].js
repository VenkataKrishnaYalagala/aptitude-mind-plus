import {fail,isAdmin,handleError} from '../_helpers.js';
export async function onRequestGet({request,env,params}){
 if(!env.DB||!env.UPLOADS)return fail('Not configured',503);
 const id=params.id;if(!/^[0-9a-f-]{36}$/.test(id))return fail('Invalid image ID',400);
 try{
  const row=await env.DB.prepare('SELECT im.object_key, q.status FROM question_images im JOIN questions q ON q.id=im.question_id WHERE im.question_id=?').bind(id).first();
  if(!row||(row.status!=='approved'&&!(await isAdmin(request,env))))return fail('Image unavailable',404);
  const object=await env.UPLOADS.get(row.object_key);
  if(!object)return fail('Image unavailable',404);
  return new Response(object.body,{status:200,headers:{'Content-Type':'image/jpeg','Cache-Control':row.status==='approved'?'public, max-age=300':'private, no-store','X-Content-Type-Options':'nosniff','Content-Security-Policy':"default-src 'none'; sandbox"}});
 }catch(err){return handleError(err);}
}
