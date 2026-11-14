"""Safe, deterministic server-side HTML renderer for Puck homepage JSON.

The editor can rearrange a small set of approved blocks. It cannot save HTML,
JavaScript, remote assets, arbitrary CSS, or alter administrator-only pages.
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

from course_platform import COURSES, CURRENCY
from engagement import community_highlight, materials_highlight

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / 'content' / 'homepage.visual.json'
BLOCKS = {
    'Hero': {'eyebrow': 100, 'title': 220, 'description': 1400, 'primaryText': 90, 'primaryHref': 90, 'secondaryText': 90, 'secondaryHref': 90, 'theme': 16},
    'ExamPaths': {'eyebrow': 100, 'heading': 220, 'description': 1400},
    'CourseShelf': {'eyebrow': 100, 'heading': 220, 'description': 1400, 'count': 3},
    'QuickLinks': {'eyebrow': 100, 'heading': 220, 'description': 1400},
    'FreeLesson': {'eyebrow': 100, 'heading': 220, 'description': 1400, 'buttonText': 90},
    'TextSection': {'eyebrow': 100, 'heading': 220, 'body': 2500, 'align': 10},
    'ImageSection': {'eyebrow': 100, 'heading': 220, 'body': 1200, 'src': 320, 'alt': 220},
    'TutorCTA': {'eyebrow': 100, 'heading': 220, 'description': 1400, 'buttonText': 90},
    'MaterialsShelf': {'eyebrow': 100, 'heading': 220, 'description': 1400},
    'CommunitySpotlight': {'eyebrow': 100, 'heading': 220, 'description': 1400},
    'Spacer': {'size': 10},
}
PAGES = {'courses.html', 'lessons.html', 'concepts.html', 'practice.html', 'pyqs.html', 'tutoring.html', 'submit.html', 'doubts.html'}
IMAGE = re.compile(r'^/media/[a-zA-Z0-9_./-]+\.(?:png|jpg|jpeg|webp|svg)$')
ID = re.compile(r'^[a-zA-Z0-9_-]{1,80}$')
COLORS = ['#2459d3','#9854e0','#ef8c28','#159477','#c65f63','#3971bd']


def e(value: str) -> str:
    return escape(value, quote=True)


def validate_layout(data: dict) -> None:
    if not isinstance(data, dict) or not isinstance(data.get('root'), dict) or not isinstance(data.get('content'), list):
        raise ValueError('A homepage must have root settings and a list of sections.')
    fields = data['root'].get('props')
    if not isinstance(fields, dict) or any(k not in {'title', 'fontStyle'} for k in fields):
        raise ValueError('Invalid homepage settings.')
    if not isinstance(fields.get('title',''), str) or len(fields.get('title','')) > 160:
        raise ValueError('Invalid homepage title.')
    if fields.get('fontStyle','system') not in {'system','modern','readable','editorial'}:
        raise ValueError('Invalid homepage font choice.')
    if len(data['content']) > 24:
        raise ValueError('Too many homepage sections (maximum 24).')
    ids = set()
    for item in data['content']:
        if not isinstance(item, dict) or item.get('type') not in BLOCKS or not isinstance(item.get('props'),dict):
            raise ValueError('Unknown section type or missing properties.')
        allowed = BLOCKS[item['type']]
        props = item['props']
        ident = props.get('id')
        if not isinstance(ident, str) or not ID.fullmatch(ident) or ident in ids:
            raise ValueError('Every section needs a unique, safe identifier.')
        ids.add(ident)
        for key, val in props.items():
            if key == 'id':
                continue
            if key not in allowed or not isinstance(val, str) or len(val) > allowed[key]:
                raise ValueError('Invalid section content or text length.')
        if item['type']=='Hero':
            for key in ('primaryHref','secondaryHref'):
                if props.get(key,'courses.html') not in PAGES:
                    raise ValueError('Buttons must link to a known website page.')
            if props.get('theme','blue') not in {'blue','white','navy'}:
                raise ValueError('Unknown hero colour theme.')
        if item['type']=='ImageSection' and props.get('src'):
            src = props['src']
            if not IMAGE.fullmatch(src) or '..' in src:
                raise ValueError('Images must be uploaded to the local /media/ folder.')
        if item['type']=='CourseShelf' and props.get('count','3') not in {'3','6'}:
            raise ValueError('Course shelf may show three or six courses.')
        if item['type']=='TextSection' and props.get('align','left') not in {'left','center'}:
            raise ValueError('Invalid text alignment.')
        if item['type']=='Spacer' and props.get('size','small') not in {'small','medium','large'}:
            raise ValueError('Invalid spacing setting.')


def wrap_header(eyebrow='', heading='', description='', align='left'):
    klass='ampv-center' if align=='center' else 'ampv-left'
    return f'<div class="ampv-heading {klass}">{f"<span class=\"ampv-eyebrow\">{e(eyebrow)}</span>" if eyebrow else ""}<h2>{e(heading)}</h2>{f"<p>{e(description)}</p>" if description else ""}</div>'


def render_item(item):
    kind=item['type']; p=item['props']; get=lambda key, default='': e(p.get(key,default))
    if kind=='Hero':
        theme=p.get('theme','blue')
        return f'''<section class="ampv-hero ampv-theme-{e(theme)}"><div class="ampv-wrap ampv-hero-grid">
          <div><span class="ampv-eyebrow ampv-hero-kicker">{get('eyebrow')}</span>
          <h1>{get('title')}</h1><p>{get('description')}</p><div class="ampv-actions">
          <a class="ampv-btn ampv-btn-primary" href="{get('primaryHref','courses.html')}">{get('primaryText','Explore')}</a>
          <a class="ampv-btn ampv-btn-secondary" href="{get('secondaryHref','lessons.html')}">{get('secondaryText','Learn more')}</a></div>
          <div class="ampv-hero-caption">Open education &middot; Original practice &middot; Optional tutoring</div></div>
          <div class="ampv-art-card"><div class="ampv-art-label">FEATURED LEARNING</div><div class="ampv-math">7<sup>2026</sup><span>&rarr; 9</span></div><div class="ampv-orbit"></div><div class="ampv-art-footer">Numbers &middot; Patterns &middot; Confidence</div></div>
        </div></section>'''
    if kind=='ExamPaths':
        parts=[]
        for i, course in enumerate(COURSES):
            parts.append(f'<a class="ampv-exam-card" style="--accent:{COLORS[i]}" href="course-{e(course["key"])}.html"><span class="ampv-chip">EXAM PATHWAY</span><span class="ampv-card-arr" aria-hidden="true">&nearr;</span><h3>{e(course["name"])}</h3><small>{e(" · ".join(course["focus"][:2]))}</small></a>')
        return f'<section class="ampv-section"><div class="ampv-wrap">{wrap_header(p.get("eyebrow",""),p.get("heading",""),p.get("description",""))}<div class="ampv-exam-grid">{"".join(parts)}</div></div></section>'
    if kind=='CourseShelf':
        count=6 if p.get('count')=='6' else 3
        cards=[]
        for i, course in enumerate(COURSES[:count]):
            cards.append(f'''<a class="ampv-course" href="course-{e(course['key'])}.html">
              <div class="ampv-course-art" style="--accent:{COLORS[i]}"><span>APTITUDE MIND PLUS</span><strong>{e(course['short'])}</strong><span>THINK CLEARER +</span></div>
              <div class="ampv-course-body"><small>FREE COURSE GUIDE</small><h3>{e(course['title'])}</h3><p>{e(course['summary'])}</p><div class="ampv-course-foot">LEARNING ACCESS <b>FREE</b></div></div>
            </a>''')
        return f'<section class="ampv-section ampv-soft"><div class="ampv-wrap">{wrap_header(p.get("eyebrow",""),p.get("heading",""),p.get("description",""))}<div class="ampv-course-grid">{"".join(cards)}</div></div></section>'
    if kind=='QuickLinks':
        destinations=[('Learn','Choose your exam and start studying','courses.html','01'),('Practice','Try questions we created','practice.html','02'),('Past Papers','Find previous exam questions','pyqs.html','03'),('Ask a Doubt','Send your question to our team','doubts.html','04'),('Tutoring','Apply for personal teacher support','tutoring.html','05')]
        tiles=''.join(f'<a class="ampv-shortcut" href="{e(href)}"><span>{number}</span><h3>{e(title)}</h3><p>{e(desc)}</p><small>Open →</small></a>' for title,desc,href,number in destinations)
        return f'<section class="ampv-section ampv-quicklinks"><div class="ampv-wrap">{wrap_header(p.get("eyebrow",""),p.get("heading",""),p.get("description",""))}<div class="ampv-shortcuts">{tiles}</div></div></section>'
    if kind=='FreeLesson':
        return f'''<section class="ampv-section ampv-lesson-feature"><div class="ampv-wrap ampv-feature-grid">
          <div>{wrap_header(p.get('eyebrow',''),p.get('heading',''),p.get('description',''))}<a class="ampv-btn ampv-btn-primary" href="practice.html#lesson">{get('buttonText','Try the lesson')}</a><p class="ampv-feature-note">No account required &middot; Worked explanations included</p></div>
          <div class="ampv-example" aria-label="Example: units digit of seven to the power of 2026"><span>NUMBER PATTERNS</span><div>7<sup>2026</sup><span>&rarr;</span><strong>9</strong></div><p>Understand why, not just what.</p></div>
        </div></section>'''
    if kind=='TextSection':
        return f'<section class="ampv-section"><div class="ampv-wrap">{wrap_header(p.get("eyebrow",""),p.get("heading",""),p.get("body",""),p.get("align","left"))}</div></section>'
    if kind=='ImageSection':
        src=p.get('src',''); image=f'<img src="{e(src)}" alt="{get("alt")}" loading="lazy">' if src else '<div class="ampv-placeholder">Image placeholder</div>'
        return f'<section class="ampv-section ampv-soft"><div class="ampv-wrap ampv-media-row">{wrap_header(p.get("eyebrow",""),p.get("heading",""),p.get("body",""))}{image}</div></section>'
    if kind=='TutorCTA':
        return f'<section class="ampv-section"><div class="ampv-wrap ampv-cta">{wrap_header(p.get("eyebrow",""),p.get("heading",""),p.get("description",""))}<div><a class="ampv-btn ampv-btn-primary" href="tutoring.html">{get("buttonText","Apply for tutoring")}</a><small class="ampv-cta-price">Optional support from {e(CURRENCY)}</small></div></div></section>'
    if kind=='MaterialsShelf':
        return materials_highlight(p.get('eyebrow',''),p.get('heading',''),p.get('description',''))
    if kind=='CommunitySpotlight':
        return community_highlight(p.get('eyebrow',''),p.get('heading',''),p.get('description',''))
    if kind=='Spacer':
        return f'<div class="ampv-spacer ampv-spacer-{get("size","small")}" aria-hidden="true"></div>'
    raise ValueError('Unknown homepage block.')


def render_home(shell, data_path=DATA_PATH):
    data=json.loads(data_path.read_text(encoding='utf-8'))
    validate_layout(data)
    font=data['root'].get('props',{}).get('fontStyle','system')
    body='<div class="ampv-page ampv-font-'+e(font)+'">'+''.join(render_item(item) for item in data['content'])+'</div>'
    title=data['root'].get('props',{}).get('title','Free aptitude learning')
    return shell('index.html',title,'Learn aptitude with free course guides, original practice and optional tutoring support.',body)

if __name__=='__main__':
    print('Visual homepage sections:',len(json.loads(DATA_PATH.read_text())['content']))
