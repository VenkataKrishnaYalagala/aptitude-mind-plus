import React from 'react';
import courses from '../../content/courses.json';
import social from '../../content/social.json';
import socialPosts from '../../content/social-posts.json';
import feedback from '../../content/feedback.json';
import './preview.css';
import '../../public/assets/engagement.css';

const options = [
  ['Courses', 'courses.html'],
  ['Free video lessons', 'lessons.html'],
  ['Concepts', 'concepts.html'],
  ['Practice', 'practice.html'],
  ['PYQ library', 'pyqs.html'],
  ['Tutoring', 'tutoring.html'],
  ['Submit a question', 'submit.html'],
  ['Ask a doubt', 'doubts.html'],
  ['Study materials', 'materials.html'],
  ['Community', 'community.html']
].map(([label, value]) => ({ label, value }));

const s = (value) => typeof value === 'string' ? value : '';
const local = (link) => options.find(x => x.value === link)?.value || 'courses.html';
const asset = (path) => /^\/media\/[a-zA-Z0-9_./-]+\.(?:png|jpg|jpeg|webp|svg)$/.test(s(path)) && !path.includes('..') ? path : '';
const EXAM_ACCENTS = ['#2459d3','#9854e0','#ef8c28','#159477','#c65f63','#3971bd'];
const trustedHosts = {youtube:['www.youtube.com','youtube.com','youtu.be'],instagram:['www.instagram.com','instagram.com'],facebook:['www.facebook.com','facebook.com','m.facebook.com','fb.watch']};
const trustedSocial = (value, platform) => {
  try{const u=new URL(value);return u.protocol==='https:'&&trustedHosts[platform]?.includes(u.hostname)&&u.pathname.length>1&&!u.username&&!u.password?u.href:'';}
  catch{return ''}
};
const profiles = ['youtube','instagram','facebook'].map(platform=>({platform,url:trustedSocial(social[platform+'_url'],platform)})).filter(item=>item.url);
const publishedPosts = socialPosts.filter(p=>p.published===true&&trustedSocial(p.source_url,p.platform));
const approvedFeedback = feedback.filter(x=>x.approved===true&&x.permission_confirmed===true&&trustedSocial(x.source_url,x.platform)&&x.quote&&x.display_name);


function Heading({eyebrow,heading,description,align='left'}) {
  return <div className={`ampv-heading ampv-${align}`}>
    {eyebrow && <span className="ampv-eyebrow">{eyebrow}</span>}
    <h2>{heading}</h2>
    {description && <p>{description}</p>}
  </div>;
}

export const config = {
  categories: {
    essentials: {title: 'Main page sections', components: ['Hero','QuickLinks','CourseShelf','FreeLesson','MaterialsShelf','CommunitySpotlight','TutorCTA','ExamPaths','TextSection']},
    extras: {title: 'Images and spacing', components: ['ImageSection','Spacer']}
  },
  root: {
    fields: {
      title: {type:'text',label:'Browser title'},
      fontStyle: {type:'select',label:'Font', options:[
        {label:'Apple-style system',value:'system'},
        {label:'Modern',value:'modern'},
        {label:'Readable',value:'readable'},
        {label:'Editorial',value:'editorial'}
      ]}
    },
    defaultProps: {title:'Aptitude Mind Plus',fontStyle:'system'},
    render: ({children,fontStyle}) => <div className={`ampv-page ampv-font-${fontStyle||'system'}`}>{children}</div>
  },
  components: {
    Hero: {
      label: 'Large welcome section',
      fields: {
        eyebrow:{type:'text',label:'Small headline'},
        title:{type:'text',label:'Main headline'},
        description:{type:'textarea',label:'Supporting text'},
        primaryText:{type:'text',label:'First button text'},
        primaryHref:{type:'select',label:'First button destination',options},
        secondaryText:{type:'text',label:'Second button text'},
        secondaryHref:{type:'select',label:'Second button destination',options},
        theme:{type:'select',label:'Background',options:[{label:'Soft blue',value:'blue'},{label:'Clean white',value:'white'},{label:'Deep navy',value:'navy'}]}
      },
      defaultProps:{eyebrow:'LEARN FREE',title:'Understand aptitude. Prepare with confidence.',description:'Explore free lessons and practice.',primaryText:'Start learning',primaryHref:'courses.html',secondaryText:'Watch videos',secondaryHref:'lessons.html',theme:'blue'},
      render:({eyebrow,title,description,primaryText,primaryHref,secondaryText,secondaryHref,theme})=><section className={`ampv-hero ampv-theme-${['blue','white','navy'].includes(theme)?theme:'blue'}`}>
        <div className="ampv-wrap ampv-hero-grid"><div>
          <span className="ampv-eyebrow ampv-hero-kicker">{eyebrow}</span>
          <h1>{title}</h1><p>{description}</p>
          <div className="ampv-actions"><a className="ampv-btn ampv-btn-primary" href={'/'+local(primaryHref)}>{primaryText||'Explore'}</a>
            <a className="ampv-btn ampv-btn-secondary" href={'/'+local(secondaryHref)}>{secondaryText||'Learn more'}</a></div>
          <div className="ampv-hero-caption">Open education · Original practice · Optional tutoring</div>
        </div><div className="ampv-art-card"><div className="ampv-art-label">FEATURED LEARNING</div><div className="ampv-math">7<sup>2026</sup><span>→ 9</span></div><div className="ampv-orbit"/><div className="ampv-art-footer">Numbers · Patterns · Confidence</div></div></div>
      </section>
    },
    ExamPaths: {
      label:'Exam category links',
      fields:{eyebrow:{type:'text'},heading:{type:'text'},description:{type:'textarea'}},
      defaultProps:{eyebrow:'EXAM PATHWAYS',heading:'Choose your exam.',description:'One foundation for many exams.'},
      render:({eyebrow,heading,description})=><section className="ampv-section"><div className="ampv-wrap">
        <Heading {...{eyebrow,heading,description}}/><div className="ampv-exam-grid">
          {courses.map((course,i)=><a key={course.key} className="ampv-exam-card" style={{'--accent':EXAM_ACCENTS[i]}} href={'/course-'+course.key+'.html'}><span className="ampv-chip">EXAM PATHWAY</span><span className="ampv-card-arr">↗</span><h3>{course.name}</h3><small>{course.focus.slice(0,2).join(' · ')}</small></a>)}
        </div></div></section>
    },
    CourseShelf:{
      label:'Free course cards',
      fields:{eyebrow:{type:'text'},heading:{type:'text'},description:{type:'textarea'},count:{type:'select',label:'How many courses?',options:[{label:'3 courses',value:'3'},{label:'6 courses',value:'6'}]}},
      defaultProps:{eyebrow:'OPEN CLASSROOM',heading:'Find your free pathway.',description:'Free course guides and practice.',count:'3'},
      render:({eyebrow,heading,description,count})=><section className="ampv-section ampv-soft"><div className="ampv-wrap"><Heading {...{eyebrow,heading,description}}/>
        <div className="ampv-course-grid">{courses.slice(0,count==='6'?6:3).map((course,i)=><a className="ampv-course" key={course.key} href={'/course-'+course.key+'.html'}><div className="ampv-course-art" style={{'--accent':EXAM_ACCENTS[i]}}><span>APTITUDE MIND PLUS</span><strong>{course.short||course.name}</strong><span>THINK CLEARER +</span></div><div className="ampv-course-body"><small>FREE COURSE GUIDE</small><h3>{course.title}</h3><p>{course.summary}</p><div className="ampv-course-foot">LEARNING ACCESS <b>FREE</b></div></div></a>)}</div>
      </div></section>
    },
    QuickLinks:{
      label:'Links to learning sections',
      fields:{eyebrow:{type:'text'},heading:{type:'text'},description:{type:'textarea'}},
      defaultProps:{eyebrow:'START HERE',heading:'What would you like to do today?',description:'Learn, practise, browse past papers or ask for help.'},
      render:({eyebrow,heading,description})=>{
        const items=[['Learn','Choose your exam and start studying','courses.html'],['Practice','Try questions we created','practice.html'],['Past Papers','Find previous exam questions','pyqs.html'],['Ask a Doubt','Send your question to our team','doubts.html'],['Tutoring','Apply for personal teacher support','tutoring.html']];
        return <section className="ampv-section ampv-quicklinks"><div className="ampv-wrap"><Heading {...{eyebrow,heading,description}}/><div className="ampv-shortcuts">{items.map(([title,detail,href],i)=><a className="ampv-shortcut" href={'/'+href} key={href}><span>{String(i+1).padStart(2,'0')}</span><h3>{title}</h3><p>{detail}</p><small>Open →</small></a>)}</div></div></section>;
      }
    },
    FreeLesson:{
      label:'Featured free lesson',
      fields:{eyebrow:{type:'text'},heading:{type:'text'},description:{type:'textarea'},buttonText:{type:'text'}},
      defaultProps:{eyebrow:'TRY A FREE LESSON',heading:'Learn why powers repeat.',description:'A real worked example and an eight-question practice quiz.',buttonText:'Start free lesson'},
      render:({eyebrow,heading,description,buttonText})=><section className="ampv-section ampv-lesson-feature"><div className="ampv-wrap ampv-feature-grid"><div><Heading {...{eyebrow,heading,description}}/><a className="ampv-btn ampv-btn-primary" href="/practice.html#lesson">{buttonText||'Start free lesson'}</a><p className="ampv-feature-note">No account required · Worked explanations included</p></div><div className="ampv-example"><span>NUMBER PATTERNS</span><div>7<sup>2026</sup><span>→</span><strong>9</strong></div><p>Understand why, not just what.</p></div></div></section>
    },
    TextSection:{
      label:'Heading and paragraph',
      fields:{eyebrow:{type:'text'},heading:{type:'text'},body:{type:'textarea'},align:{type:'select',options:[{label:'Left',value:'left'},{label:'Center',value:'center'}]}},
      defaultProps:{eyebrow:'OUR APPROACH',heading:'Understand first. Solve next.',body:'Learn concepts, practise, and build confidence.',align:'center'},
      render:({eyebrow,heading,body,align})=><section className="ampv-section"><div className="ampv-wrap"><Heading {...{eyebrow,heading,description:body,align}}/></div></section>
    },
    ImageSection:{
      label:'Image and description',
      fields:{eyebrow:{type:'text'},heading:{type:'text'},body:{type:'textarea'},src:{type:'text',label:'Uploaded image path (/media/...)'},alt:{type:'text',label:'Image description'}},
      defaultProps:{eyebrow:'LEARN VISUALLY',heading:'A clearer explanation.',body:'',src:'',alt:'Aptitude study material'},
      render:({eyebrow,heading,body,src,alt})=><section className="ampv-section ampv-soft"><div className="ampv-wrap ampv-media-row"><Heading {...{eyebrow,heading,description:body}}/>{asset(src)?<img src={asset(src)} alt={alt||''} />:<div className="ampv-placeholder">Choose an image from your <b>/media/</b> library to display it here.</div>}</div></section>
    },
    MaterialsShelf:{
      label:'Free and paid materials',
      fields:{eyebrow:{type:'text'},heading:{type:'text'},description:{type:'textarea'}},
      defaultProps:{eyebrow:'STUDY MATERIALS',heading:'Free resources. Optional extras.',description:'Find free notes, practice and exam references. Premium workbooks will be listed with prices when ready.'},
      render:({eyebrow,heading,description})=><section className="materials-feature"><div className="ampv-wrap materials-feature-inner"><div className="materials-feature-copy"><span className="ampv-eyebrow">{eyebrow||'STUDY MATERIALS'}</span><h2>{heading||'Free resources. Optional extras.'}</h2><p>{description}</p><a className="ampv-btn ampv-btn-primary" href="/materials.html">Explore study materials ↗</a></div><div className="materials-feature-art"><div><span>01 / OPEN LEARNING</span><strong>Free notes & practice</strong><small>Always available without payment</small></div><div><span>02 / OPTIONAL EXTRAS</span><strong>Premium workbooks</strong><small>Coming soon · prices published before purchase</small></div></div></div></section>
    },
    CommunitySpotlight:{
      label:'Social and approved learner feedback',
      fields:{eyebrow:{type:'text'},heading:{type:'text'},description:{type:'textarea'}},
      defaultProps:{eyebrow:'LEARN WITH OUR COMMUNITY',heading:'Follow along as we learn.',description:'Watch our lessons, see new questions and follow our social pages.'},
      render:({eyebrow,heading,description})=><section className="community-section" id="community"><div className="ampv-wrap community-grid"><div className="community-intro"><span className="ampv-eyebrow">{eyebrow||'FROM THE CLASSROOM'}</span><h2>{heading||social.section_heading}</h2><p>{description||social.section_description}</p><div className="social-links">{profiles.map(({platform,url})=><a className="social-pill" href={url} key={url} target="_blank" rel="noopener noreferrer nofollow"><span className={'social-icon social-'+platform}>{({youtube:'▶',instagram:'◎',facebook:'f'})[platform]}</span>{platform[0].toUpperCase()+platform.slice(1)} ↗</a>)}</div><a href="/community.html" className="community-text-link">See our community updates ↗</a></div>
      {(publishedPosts.length||approvedFeedback.length)?<div className="community-preview">{publishedPosts.slice(0,2).map(p=><a className="community-post" href={trustedSocial(p.source_url,p.platform)} key={p.source_url} target="_blank" rel="noopener noreferrer nofollow"><span className="community-meta">{p.platform} · Public post ↗</span><h3>{p.title}</h3><p>{p.summary}</p><span className="community-origin">View original post</span></a>)}{approvedFeedback.slice(0,1).map(f=><figure className="voice-card" key={f.source_url}><blockquote>“{f.quote}”</blockquote><figcaption>{f.display_name} · {f.platform}</figcaption></figure>)}</div>:<div className="community-feature"><span>APTITUDE MIND PLUS / COMMUNITY</span><div>Learn.<br/><em>Share.</em><br/>Grow.</div><small>Short explanations · Exam tips · New lessons</small></div>}</div></section>
    },
    TutorCTA:{
      label:'Tutoring invitation',
      fields:{eyebrow:{type:'text'},heading:{type:'text'},description:{type:'textarea'},buttonText:{type:'text'}},
      defaultProps:{eyebrow:'OPTIONAL TEACHER SUPPORT',heading:'Need help from a teacher?',description:'Core courses, lessons and practice are free. Some optional workbooks may be paid. Teacher support is ₹2,999 after we confirm class details.',buttonText:'Apply for teacher support'},
      render:({eyebrow,heading,description,buttonText})=><section className="ampv-section"><div className="ampv-wrap ampv-cta"><div><Heading {...{eyebrow,heading,description}}/></div><a className="ampv-btn ampv-btn-primary" href="/tutoring.html">{buttonText||'Enquire'}</a></div></section>
    },
    Spacer:{
      label:'Vertical spacing',
      fields:{size:{type:'select',options:[{label:'Small',value:'small'},{label:'Medium',value:'medium'},{label:'Large',value:'large'}]}},
      defaultProps:{size:'small'},
      render:({size})=><div aria-hidden="true" className={'ampv-spacer ampv-spacer-'+(['small','medium','large'].includes(size)?size:'small')}/>
    }
  }
};
