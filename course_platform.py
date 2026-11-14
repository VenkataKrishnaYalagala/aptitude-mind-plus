"""Course-first catalog pages for Aptitude Mind Plus.

All course metadata below is editorial guidance, not a promise of a finalized
schedule, credential, recording, rating, or live seat availability.
"""
from html import escape

import json
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs

HERE=Path(__file__).parent
COURSES=json.loads((HERE/'content/courses.json').read_text(encoding='utf-8'))
for item in COURSES:
    # Convert CMS-editable object modules to simple (heading, topics) pairs.
    item['modules']=[(module['heading'],module.get('topics',[])) for module in item.get('modules',[])]
SITE=json.loads((HERE/'content/site.json').read_text(encoding='utf-8'))
LESSONS=json.loads((HERE/'content/lessons.json').read_text(encoding='utf-8'))
CURRENCY='₹'+format(int(SITE.get('support_price') or 3000),',')

def video_id(url):
    if not isinstance(url,str) or not url.startswith('https://'):return None
    p=urlparse(url)
    host=(p.hostname or '').lower()
    candidate=None
    if host in ('youtu.be','www.youtu.be'):
        candidate=p.path.strip('/').split('/')[0]
    elif host in ('youtube.com','www.youtube.com','m.youtube.com','youtube-nocookie.com','www.youtube-nocookie.com'):
        candidate=parse_qs(p.query).get('v',[''])[0] if p.path=='/watch' else (p.path.split('/')[2] if p.path.startswith(('/embed/','/shorts/')) and len(p.path.split('/'))>2 else None)
    return candidate if candidate and re.fullmatch(r'[A-Za-z0-9_-]{11}',candidate) else None

def safe_image(value):
    return value if isinstance(value,str) and re.fullmatch(r'/media/[a-zA-Z0-9_./-]+\.(?:png|jpg|jpeg|webp|svg)',value) and '..' not in value else ''


def e(value):
    return escape(str(value), quote=True)


def button(text, href, variant='primary'):
    return f'<a class="button button-{variant}" href="{e(href)}">{e(text)} <span aria-hidden="true">&rarr;</span></a>'


def course_cover(item, extra=''):
    key=item['key']
    cover=safe_image(item.get('cover_image',''))
    photo=f'<img class="market-custom-cover" src="{e(cover)}" alt="" loading="lazy">' if cover else ''
    return f'''<div class="market-cover cover-{key} {extra}" aria-hidden="true">{photo}
      <span class="cover-grid"></span><span class="cover-circle cover-circle-one"></span><span class="cover-circle cover-circle-two"></span>
      <span class="cover-topline">APTITUDE MIND PLUS <span> / {e(item['short'])}</span></span>
      <span class="cover-mark">{e(item['symbol'])}</span>
      <span class="cover-foot">THINK CLEARER <span class="cover-plus">+</span></span>
    </div>'''


def course_card(item):
    key=item['key']
    chips=''.join(f'<span>{e(t)}</span>' for t in item['focus'][:2])
    search_text=' '.join([item['name'],item['title'],item['summary'],*item['focus'],key]).lower()
    return f'''<article class="market-course-card" data-market-course data-exam="{e(key)}" data-search="{e(search_text)}" id="course-{e(key)}">
     <a href="course-{e(key)}.html" class="market-image-link" aria-label="Explore {e(item['name'])} course">{course_cover(item)}</a>
     <div class="market-card-main"><div class="market-card-top"><span>EXAM PREPARATION</span><span class="market-level">Foundation + practice</span></div>
      <h3><a href="course-{e(key)}.html">{e(item['title'])}</a></h3>
      <p>{e(item['summary'])}</p><div class="market-chips">{chips}</div>
     </div>
     <div class="market-card-bottom"><div><small>LEARNING ACCESS</small><strong>FREE</strong></div><a class="market-card-link" href="course-{e(key)}.html" aria-label="View {e(item['name'])} course details">Explore course <span aria-hidden="true">&rarr;</span></a></div>
    </article>'''


def home(shell):
    cards=''.join(course_card(x) for x in COURSES[:3])
    chips=''.join(f'<a href="courses.html?exam={e(x["key"])}" class="exam-pill exam-pill-{e(x["key"])}"><span class="pill-indicator"></span>{e(x["name"])} <span aria-hidden="true">&rarr;</span></a>' for x in COURSES)
    main='''<section class="market-hero"><div class="wrap market-hero-grid">
    <div class="market-hero-copy"><span class="market-kicker"><span class="live-dot"></span> BUILT FOR EVERY APTITUDE LEARNER</span>
     <h1>Your next exam starts with a <span>clearer way to learn.</span></h1>
     <p>One destination for aptitude across India's competitive exams. Explore focused courses, understand concepts, practise with explanations, and build real confidence.</p>
     <form class="hero-search" action="courses.html" method="get" role="search" aria-label="Search aptitude courses"><label for="hero-search-input" class="sr-only">Search courses or exams</label><span class="search-symbol" aria-hidden="true">&#9906;</span><input id="hero-search-input" name="q" type="search" placeholder="Search CSAT, GATE, reasoning..." autocomplete="off" maxlength="90"><button type="submit">Find a course <span aria-hidden="true">&rarr;</span></button></form>
     <div class="hero-assurance"><span><span aria-hidden="true">&#10003;</span> Free concepts &amp; quizzes</span><span><span aria-hidden="true">&#10003;</span> Exam-focused pathways</span><span><span aria-hidden="true">&#10003;</span> Human-reviewed PYQs</span></div>
    </div>
    <div class="market-hero-showcase" aria-label="Featured aptitude course preview">
      <div class="showcase-orb showcase-orb-one"></div><div class="showcase-orb showcase-orb-two"></div>
      <div class="showcase-card">
       <div class="showcase-label"><span class="showcase-bookmark">FEATURED PATHWAY</span><span class="showcase-mark">AMP / 01</span></div>
       <div class="showcase-art" aria-hidden="true"><span class="art-line art-line-one"></span><span class="art-line art-line-two"></span><span class="art-sigma">&#8721;</span><span class="art-equation">x<sup>2</sup> + y<sup>2</sup></span><span class="art-chip">Reason &middot; Solve &middot; Grow</span></div>
       <div class="showcase-info"><span class="showcase-small">UPSC CSAT / GENERAL APTITUDE</span><h2>Turn complex questions into clear answers.</h2><div class="showcase-bottom"><span>COURSE GUIDE</span><a href="course-upsc.html">Explore pathway <span aria-hidden="true">&rarr;</span></a></div></div>
      </div><a href="practice.html#lesson" class="showcase-float"><span class="float-icon">&#9654;</span><span><strong>Try a free lesson</strong><small>Units digit &amp; cyclicity</small></span><span aria-hidden="true">&nearr;</span></a>
    </div>
    </div></section>
    <section class="market-explore-strip"><div class="wrap"><div class="explore-label">EXPLORE BY EXAM</div><div class="exam-pills">'''+chips+'''</div></div></section>
    <section class="market-section" id="featured-courses"><div class="wrap"><div class="market-section-header"><div><span class="market-eyebrow">YOUR NEXT STEP</span><h2>Find the free pathway that fits your goal.</h2><p>Purpose-built aptitude pathways, free to explore and practise.</p></div><a class="market-all-link" href="courses.html">Browse all six courses <span aria-hidden="true">&rarr;</span></a></div>
      <div class="market-course-grid home-course-grid">'''+cards+'''</div>
      <div class="market-quiet-note">Concepts, lessons and practice are free. Optional personal tutoring is available from {e(CURRENCY)}; the session plan and terms are agreed before payment.</div>
    </div></section>
    <section class="market-section learning-workflow"><div class="wrap"><div class="market-section-header"><div><span class="market-eyebrow">HOW LEARNING WORKS</span><h2>A thoughtful path from concept to exam.</h2><p>Learn the reason behind a method, not just the final answer.</p></div></div>
      <div class="workflow-grid"><article class="workflow-tile"><span class="workflow-num">01</span><div class="workflow-graphic graphic-concept"><span>7<sup>2</sup></span><span class="graphic-equals">=</span><strong>49</strong></div><h3>Learn the idea</h3><p>Start with clear, original concept explanations and worked examples.</p><a href="concepts.html">Explore concepts &rarr;</a></article><article class="workflow-tile"><span class="workflow-num">02</span><div class="workflow-graphic graphic-quiz"><span>Question 01</span><div><i></i><i></i><i class="selected"></i><i></i></div></div><h3>Practise with feedback</h3><p>Answer questions, check your work, and understand where you went wrong.</p><a href="practice.html">Try free practice &rarr;</a></article><article class="workflow-tile"><span class="workflow-num">03</span><div class="workflow-graphic graphic-library"><span>PYQ REVIEW</span><strong>Exam / Topic / Source</strong><div class="library-lines"></div><i>&#10003;</i></div><h3>Connect it to exams</h3><p>Use the reviewed question library to put each concept in context.</p><a href="pyqs.html">Open the PYQ library &rarr;</a></article></div>
    </div></section>
    <section class="market-section market-free"><div class="wrap free-lesson-panel"><div class="free-lesson-copy"><span class="market-eyebrow">START FREE</span><h2>One small lesson.<br>One big insight.</h2><p>Discover why the last digits of large powers repeat. Then test your understanding with eight original practice questions.</p><div class="free-actions">'''+button('Try the free lesson','practice.html#lesson')+'''<a href="concepts.html">See all concepts &rarr;</a></div></div><div class="free-lesson-graphic" aria-hidden="true"><span class="free-math-label">PATTERNS IN POWERS</span><div class="free-power">7<sup>2026</sup> <span>= ?</span></div><div class="free-cycle"><span>7</span><span>9</span><span>3</span><span>1</span></div><span class="free-solution">The pattern repeats every 4 powers.</span></div></div></section>
    <section class="market-section end-invite"><div class="wrap end-invite-box"><div><span class="market-eyebrow">NEED GUIDANCE?</span><h2>Learn with a course built around your exam.</h2><p>Learn the foundations for free, then ask for individual teaching support if needed. Applying is free.</p></div>'''+button('Explore all courses','courses.html')+'''</div></section>'''
    main=main.replace('BUILT FOR EVERY APTITUDE LEARNER',e(SITE.get('hero_kicker','FREE LEARNING FOR EVERY EXAM')))
    main=main.replace('Your next exam starts with a <span>clearer way to learn.</span>',e(SITE.get('hero_title','Learn free. Prepare with confidence.')))
    main=main.replace("One destination for aptitude across India's competitive exams. Explore focused courses, understand concepts, practise with explanations, and build real confidence.",e(SITE.get('hero_description','Free concepts and practice, with optional tutor-led support.')))
    main=main.replace('{e(CURRENCY)}',e(CURRENCY))
    return shell('index.html','Free Courses & Aptitude Learning','Browse free aptitude video lessons, original concepts, practice and a reviewed PYQ library.',main)


def courses(shell):
    cards=''.join(course_card(x) for x in COURSES)
    buttons='<button type="button" class="catalog-filter active" data-course-filter="all" aria-pressed="true">All courses <span>6</span></button>'
    buttons+=''.join(f'<button type="button" class="catalog-filter" data-course-filter="{e(x["key"])}" aria-pressed="false">{e(x["name"])} <span>1</span></button>' for x in COURSES)
    main='''<section class="catalog-banner"><div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Courses</span></nav><span class="market-kicker"><span class="live-dot"></span> EXPLORE APTITUDE COURSES</span><h1>Find your <span>next breakthrough.</span></h1><p>Choose your exam. Learn the foundations for free, then request optional personal guidance when you need it.</p>
    <form class="catalog-search" role="search" action="courses.html" method="get"><label class="sr-only" for="catalog-search-input">Search courses, topics and exams</label><span aria-hidden="true">&#9906;</span><input id="catalog-search-input" name="q" data-course-search type="search" maxlength="90" placeholder="Search course name, subject or skill..." autocomplete="off"><button type="submit">Search <span aria-hidden="true">&rarr;</span></button></form>
    </div></section>
    <section class="market-section catalog-content"><div class="wrap catalog-layout" data-catalog>
    <aside class="catalog-sidebar"><div class="catalog-side-title"><h2>Filter courses</h2><button type="button" data-course-clear>Reset</button></div><p>PREPARE FOR</p><div class="catalog-filter-list">'''+buttons+'''</div><div class="catalog-sidebar-note"><strong>Only aptitude.</strong><span>Our courses focus on aptitude, reasoning, verbal ability and relevant mathematical skills. They do not cover every subject in an exam.</span></div></aside>
    <div class="catalog-results"><div class="catalog-toolbar"><div><span class="market-eyebrow">OUR PROGRAMMES</span><h2>All aptitude courses</h2><span class="catalog-count" data-course-count aria-live="polite">6 courses</span></div><label class="catalog-sort">Sort by <select data-course-sort aria-label="Sort courses"><option value="default">Exam pathway</option><option value="az">Name: A to Z</option></select></label></div>
    <div class="market-course-grid catalog-course-grid" data-course-grid>'''+cards+'''</div>
    <div class="catalog-empty" data-course-empty hidden><strong>No matching courses yet.</strong><p>Try a different exam or topic, or clear the search to view all six pathways.</p><button type="button" class="button button-light" data-course-clear>Clear filters</button></div>
    <p class="catalog-disclaimer">All free course guides and upcoming video lessons are open to everyone. Optional tutoring is available at {e(CURRENCY)} for a support programme; confirm sessions and terms before payment.</p>
    </div></div></section><section class="market-section market-catalog-footer"><div class="wrap end-invite-box"><div><span class="market-eyebrow">FREE LEARNING FOR EVERYONE</span><h2>Try the learning approach first.</h2><p>Start with an original units-digit lesson and interactive practice quiz.</p></div>'''+button('Try a free lesson','practice.html#lesson')+'''</div></section>'''
    main=main.replace('{e(CURRENCY)}',e(CURRENCY))
    return shell('courses.html','Explore Aptitude Courses','Search and compare UPSC CSAT, GATE, SSC, Banking, APPSC/TGPSC and Railways aptitude courses.',main)


def course_detail(shell, item):
    key=item['key']
    outcomes=''.join(f'<li><span aria-hidden="true">&#10003;</span><span>{e(x)}</span></li>' for x in item['outcomes'])
    modules=''.join(f'<details class="outline-module" {"open" if i==0 else ""}><summary><span class="outline-num">{i+1:02d}</span><strong>{e(label)}</strong><span class="outline-toggle" aria-hidden="true">+</span></summary><ul>{"".join(f"<li>{e(x)}</li>" for x in points)}</ul></details>' for i,(label,points) in enumerate(item['modules']))
    focus=''.join(f'<span>{e(x)}</span>' for x in item['focus'])
    cards=''.join(course_card(x) for x in COURSES if x['key'] != key)[:15000]
    body=f'''<section class="detail-hero detail-{e(key)}"><div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="courses.html">Courses</a><span aria-hidden="true">/</span><span>{e(item['name'])}</span></nav>
     <div class="detail-hero-layout"><div class="detail-heading"><span class="market-kicker"><span class="live-dot"></span> APTITUDE MIND PLUS / {e(item['short'])}</span><h1>{e(item['title'])}</h1><p>{e(item['summary'])}</p><div class="detail-tags">{focus}</div>
     <div class="detail-actions">{button('Watch free lessons',f'lessons.html?exam={key}')}{button('Request personal tutoring',f'tutoring.html?course={key}#apply','light')}</div><div class="detail-fineprint">Application is free. No payment is collected on this website.</div></div>
     <aside class="detail-enrol-card" aria-label="Free learning and optional tutoring">{course_cover(item,'detail-cover')}<div class="detail-enrol-body"><div class="detail-price-label">SELF-PACED LEARNING</div><div class="detail-price">FREE <span>/ open lessons</span></div><p>Learn with free videos and practice as they become available. Personal tutoring is an optional paid service.</p><a class="button button-primary full-button" href="tutoring.html?course={e(key)}#apply">Apply for tutoring &rarr;</a><ul><li>Exam-specific aptitude focus</li><li>Concept-first explanations</li><li>Free application, no automatic charge</li></ul></div></aside></div></div></section>
     <section class="market-section detail-body"><div class="wrap detail-content-layout"><div class="detail-body-main"><div class="detail-section" id="outcomes"><span class="market-eyebrow">THE LEARNING GOAL</span><h2>What you'll work toward</h2><p>These are the intended learning outcomes for the pathway. The final class plan is agreed before enrolment.</p><ul class="outcomes-grid">{outcomes}</ul></div>
      <div class="detail-section" id="outline"><span class="market-eyebrow">COURSE GUIDE</span><h2>Explore the course outline</h2><p>An indicative topic roadmap, not a confirmed timetable or promise of recorded lessons. Exact coverage varies with the agreed class format and exam requirements.</p><div class="outline-list">{modules}</div></div>
      <div class="detail-section" id="suitable"><span class="market-eyebrow">A GOOD PLACE TO BEGIN</span><h2>Who this pathway is for</h2><p>Students preparing for the aptitude, mental ability or reasoning component of {e(item['name'])}. Beginners can start with the free lesson and build from foundational concepts.</p><div class="detail-note"><strong>Before enrolling</strong><p>We will confirm the schedule, number of sessions, teaching mode, full syllabus, assessment approach and payment terms. Optional {e(CURRENCY)} tutoring support is separate from the free online lessons, and does not cover every subject in the examination.</p></div></div>
      <div class="detail-section" id="faq"><span class="market-eyebrow">GOOD TO KNOW</span><h2>Common questions</h2><div class="faq-list"><details><summary>Does this course cover the whole examination?</summary><p>No. Aptitude Mind Plus focuses on the aptitude, numerical, verbal and reasoning portions relevant to each exam. Other examination subjects are not included.</p></details><details><summary>Is the free learning section really free?</summary><p>Yes. Videos, concepts, exercises and approved questions are open to all. Only optional personal tutoring is paid; applying does not take payment.</p></details><details><summary>Are recorded lessons or certificates included?</summary><p>Lessons appear only after real videos are published. Certificates and recorded tutoring sessions are not promised.</p></details><details><summary>Can I try something for free first?</summary><p>Yes. Visit our free units-digit concept lesson and original eight-question practice quiz. No account is required.</p></details></div></div></div>
      <aside class="detail-rail"><div class="detail-rail-card"><span class="market-eyebrow">FREE PREVIEW</span><h3>See how we teach.</h3><p>Try an original lesson about repeating units-digit patterns.</p><div class="rail-equation">7<sup>2026</sup> &rarr; <b>9</b></div><a href="practice.html#lesson">Open free lesson &rarr;</a></div><div class="detail-rail-card detail-help"><h3>Need course guidance?</h3><p>Tell us which exam you're targeting and what you'd like to improve.</p><a href="tutoring.html?course={e(key)}#apply">Ask a question &rarr;</a></div></aside></div></section>
     <section class="market-section detail-recommendations"><div class="wrap"><div class="market-section-header"><div><span class="market-eyebrow">KEEP EXPLORING</span><h2>More exam pathways</h2></div><a class="market-all-link" href="courses.html">View full catalog &rarr;</a></div><div class="market-course-grid home-course-grid">{''.join(course_card(x) for x in COURSES if x['key']!=key)[:3]}</div></div></section>'''
    return shell('courses.html', item['title'], item['summary'],body)


def detail_pages(shell):
    return {f'course-{item["key"]}.html':course_detail(shell,item) for item in COURSES}


def lessons_page(shell):
    visible=[item for item in LESSONS if item.get('published')]
    exam_labels={'all':'All exams','upsc':'UPSC CSAT','gate':'GATE','ssc':'SSC','bank':'Banking','state':'APPSC / TGPSC','rail':'Railways'}
    cards=[]
    for item in visible:
        title=e(item.get('title','Free lesson'));summary=e(item.get('summary',''))
        exam=item.get('exam','all')
        if exam not in exam_labels:continue
        id=video_id(item.get('youtube_url',''))
        image=safe_image(item.get('cover_image',''))
        thumb=f'<img src="{e(image)}" loading="lazy" alt="">' if image else '<span class="lesson-symbol" aria-hidden="true">∑</span>'
        if id:
            player=f'<button type="button" class="video-play" data-play-video="{id}" aria-label="Play {title} on this page">▶ Play lesson</button>'
            link=f'<a class="lesson-youtube-link" href="https://www.youtube.com/watch?v={id}" target="_blank" rel="noopener noreferrer">Watch on YouTube ↗</a>'
        else:
            relative=item.get('link','')
            if not re.fullmatch(r'(?:practice|concepts|pyqs)\.html(?:#[a-zA-Z0-9-]+)?',relative):relative='practice.html#lesson'
            player=f'<a class="video-play" href="{e(relative)}">Read the free lesson →</a>'
            link=''
        notes=item.get('notes','')
        notes_html=f'<details class="video-notes"><summary>Read lesson notes</summary><p>{e(notes)}</p></details>' if notes else ''
        cards.append(f'''<article class="video-lesson-card" data-lesson-exam="{e(exam)}" data-lesson-search="{e((title+' '+summary+' '+str(item.get('topic',''))).lower())}">
            <div class="video-preview" data-video-frame>{thumb}{player}</div>
            <div class="video-card-body"><div class="video-meta">{e(exam_labels[exam])} · {e(item.get('topic','General aptitude'))}</div><h2>{title}</h2><p>{summary}</p>{notes_html}<div class="video-card-bottom"><span>FREE LEARNING</span>{link}</div></div></article>''')
    listing=''.join(cards) if cards else '<div class="video-empty"><h2>Free video lessons are on the way.</h2><p>Start with the current practice lesson; video embeds will appear here as soon as the channel owner publishes them.</p><a href="practice.html#lesson">Try the units-digit lesson →</a></div>'
    body=f'''<section class="catalog-banner video-hero"><div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Free videos</span></nav><span class="market-kicker">YOUR OPEN CLASSROOM</span><h1>Learn freely. <span>Grow confidently.</span></h1><p>Original aptitude lessons alongside practice questions. When a YouTube lesson is available, play it right here or open it on YouTube.</p></div></section>
    <section class="market-section video-section"><div class="wrap"><div class="video-toolbar"><div><span class="market-eyebrow">LESSON LIBRARY</span><h2>Video lessons & guided notes</h2></div><label class="sr-only" for="video-search">Search lessons</label><input id="video-search" type="search" data-video-search placeholder="Search topics or skills..."></div><div class="video-filters" aria-label="Filter lessons by exam"><button type="button" class="video-filter active" data-video-filter="all" aria-pressed="true">All subjects</button>{''.join(f'<button type="button" class="video-filter" data-video-filter="{k}" aria-pressed="false">{e(v)}</button>' for k,v in exam_labels.items() if k!='all')}</div><div class="video-grid" data-video-grid>{listing}</div><p class="video-no-results" data-video-none hidden>No lessons match your search yet.</p></div></section>
    <section class="market-section section-soft"><div class="wrap"><div class="end-invite-box"><div><span class="market-eyebrow">STUCK ON A QUESTION?</span><h2>Free content. Optional teacher support.</h2><p>Learn independently at no charge, then request personal tutoring if you want structured guidance.</p></div>{button('Ask about tutoring','tutoring.html#apply')}</div></div></section>'''
    return shell('lessons.html','Free Video Lessons & Guided Notes','Watch free aptitude videos, learn concepts, and test understanding with original practice.',body)
