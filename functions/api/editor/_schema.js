// The same limited block catalogue is rendered server-side by visual_home.py.
// Treat the user editable JSON as untrusted even after an admin logs in.
const SPECS={
 Hero:{eyebrow:100,title:220,description:1400,primaryText:90,primaryHref:90,secondaryText:90,secondaryHref:90,theme:16},
 ExamPaths:{eyebrow:100,heading:220,description:1400},
 CourseShelf:{eyebrow:100,heading:220,description:1400,count:3},
 TextSection:{eyebrow:100,heading:220,body:2500,align:10},
 ImageSection:{eyebrow:100,heading:220,body:1200,src:320,alt:220},
 TutorCTA:{eyebrow:100,heading:220,description:1400,buttonText:90},
 Spacer:{size:10}
};
const PAGES=new Set(['courses.html','lessons.html','concepts.html','practice.html','pyqs.html','tutoring.html','submit.html']);
const image=/^\/media\/[a-zA-Z0-9_./-]+\.(?:png|jpg|jpeg|webp|svg)$/;
const id=/^[a-zA-Z0-9_-]{1,80}$/;
const subsets=(v,values)=>values.includes(v);
export function validateLayout(data){
 if(!data||typeof data!=='object'||Array.isArray(data)||!data.root||typeof data.root!=='object'||!Array.isArray(data.content))return 'Invalid homepage structure.';
 const root=data.root.props;
 if(!root||typeof root!=='object'||Array.isArray(root)||Object.keys(root).some(k=>!['title','fontStyle'].includes(k)))return 'Invalid page settings.';
 if(typeof root.title!=='string'||root.title.length>160||!subsets(root.fontStyle||'system',['system','modern','readable','editorial']))return 'Invalid homepage title or font.';
 if(data.content.length>24)return 'Too many sections (24 maximum).';
 const ids=new Set();
 for(const block of data.content){
  if(!block||typeof block!=='object'||Array.isArray(block)||!(block.type in SPECS)||!block.props||typeof block.props!=='object'||Array.isArray(block.props))return 'Invalid homepage section.';
  const rules=SPECS[block.type],p=block.props;
  if(typeof p.id!=='string'||!id.test(p.id)||ids.has(p.id))return 'Duplicate or invalid section identifier.';
  ids.add(p.id);
  for(const [key,val] of Object.entries(p)){
   if(key==='id')continue;
   if(!Object.hasOwn(rules,key)||typeof val!=='string'||val.length>rules[key])return 'Unsupported section field or text too long.';
  }
  if(block.type==='Hero'){
   if(!PAGES.has(p.primaryHref||'courses.html')||!PAGES.has(p.secondaryHref||'courses.html'))return 'Choose an internal button destination.';
   if(!subsets(p.theme||'blue',['blue','white','navy']))return 'Invalid colour theme.';
  }
  if(block.type==='ImageSection'&&p.src&&(!image.test(p.src)||p.src.includes('..')))return 'Images must be in the /media/ folder.';
  if(block.type==='CourseShelf'&&!subsets(p.count||'3',['3','6']))return 'Choose three or six courses.';
  if(block.type==='TextSection'&&!subsets(p.align||'left',['left','center']))return 'Invalid alignment.';
  if(block.type==='Spacer'&&!subsets(p.size||'small',['small','medium','large']))return 'Invalid spacer.';
 }
 return null;
}
