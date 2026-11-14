"""Curated past paper reference browser.

Public source index only: source records are NOT full question-paper files.
Never embed or expose private Google Drive file IDs/URLs or claim that unverified
third-party scans are official exam materials.
"""
from __future__ import annotations
from pathlib import Path
from html import escape
from urllib.parse import urlparse
import json
import re

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'content/pyq-index.json'
STATUSES={
 'verified':('Official key checked','verified'),
 'conditional':('Answer needs a note','conditional'),
 'deleted':('Deleted by final key','deleted'),
 'source':('Source indexed','source'),
 'pending':('Verification pending','pending'),
 'cancelled':('Cancelled paper','cancelled')
}
EXAMS={'upsc':'UPSC CSAT','gate':'GATE Aptitude','ssc':'SSC','bank':'Banking','rail':'Railways','state':'APPSC / TGPSC'}
OFFICIAL={'www.upsc.gov.in','upsc.gov.in','gate2024.iisc.ac.in','portal-psc.ap.gov.in'}

def e(v):return escape(str(v),quote=True)

def load_index(path=DATA):
 payload=json.loads(path.read_text(encoding='utf-8'))
 items=payload.get('items')
 if not isinstance(items,list) or len(items)>1500:raise ValueError('Invalid past-paper index')
 ids=set()
 for item in items:
  if not isinstance(item,dict):raise ValueError('Invalid past paper record')
  if not re.fullmatch(r'[a-z0-9-]{3,90}',item.get('id','')) or item['id'] in ids:raise ValueError('Invalid or duplicate paper record')
  ids.add(item['id'])
  if item.get('exam') not in EXAMS or item.get('status') not in STATUSES:raise ValueError('Unknown paper category')
  y=item.get('year')
  if not isinstance(y,int) or not (y==0 or 1950<=y<=2035):raise ValueError('Invalid paper year')
  for key in ('exam_label','paper','topic','concept','title','answer','description','note','source_label','source_url'):
   if not isinstance(item.get(key),str) or len(item[key])>1400:raise ValueError('Invalid paper field '+key)
  if item['source_url']:
   url=urlparse(item['source_url'])
   if url.scheme!='https' or url.hostname not in OFFICIAL or url.username or url.password:raise ValueError('Non-official paper source URL')
 return items

def render_pyq_archive():
 items=load_index()
 years=sorted({x['year'] for x in items if x['year']>0},reverse=True)
 topics=sorted({x['topic'] for x in items})
 concepts=sorted({x['concept'] for x in items})
 def opt(values):return ''.join(f'<option value="{e(v)}">{e(v)}</option>' for v in values)
 cards=[]
 for item in items:
  label,cl=STATUSES[item['status']]
  title=item['title']
  year=str(item['year']) if item['year'] else 'Year to verify'
  meta=f'{item["exam_label"]} · {year} · {item["paper"]}'
  if item.get('question_number'):meta+=f' · Q{item["question_number"]}'
  src=f'<a class="pyq-source-link" href="{e(item["source_url"])}" target="_blank" rel="noopener noreferrer">{e(item["source_label"] or "Official exam source")} <span aria-hidden="true">↗</span></a>' if item['source_url'] else '<span class="pyq-unavailable">No verified public source link yet</span>'
  answer=f'<p><strong>Indexed answer:</strong> {e(item["answer"])}</p>' if item['answer'] else ''
  note=f'<p>{e(item["note"])}</p>' if item['note'] else ''
  cards.append(f'''<article class="pyq-record" data-pyq-record data-exam="{e(item['exam'])}" data-year="{item['year']}" data-topic="{e(item['topic'])}" data-concept="{e(item['concept'])}" data-search="{e(' '.join(str(item.get(x,'')) for x in ('title','exam_label','paper','topic','concept','question_number','description')).lower())}">
   <div class="pyq-record-head"><span class="pyq-record-exam">{e(item['exam_label'])}</span><span class="pyq-source-status status-{cl}">{label}</span></div>
   <h3>{e(title)}</h3><p class="pyq-meta">{e(meta)}</p>
   <div class="pyq-tags"><span>{e(item['topic'])}</span><span>{e(item['concept'])}</span></div>
   <p class="pyq-record-summary">{e(item['description'])}</p>
   <details class="pyq-record-details"><summary>Answer and source details <span aria-hidden="true">+</span></summary>{answer}{note}<p>This is a source reference, not a copy of the complete exam question. Read the original paper for exact wording, options and figures.</p>{src}</details>
   </article>''')
 return f'''<section class="page-intro pyq-intro"><div class="wrap narrow"><div class="eyebrow">PREVIOUS EXAM QUESTIONS</div><h1>Past papers, organised for <span class="gradient-text">easy study.</span></h1><p>Find previous-year exam questions by exam, year, topic or concept. We show when an answer is verified, deleted, or still under review.</p></div></section>
 <section class="section compact-section"><div class="wrap"><div class="pyq-archive-intro"><div><h2>Browse past papers</h2><p>These references come from our reviewed exam-paper archive. Open the official source to see complete printed questions and options.</p></div><span class="pyq-count-pill"><strong>{len(items)}</strong> indexed records</span></div>
 <div class="pyq-filters" role="search" aria-label="Find past paper references">
 <label class="pyq-query">Search<input data-pyq-search type="search" maxlength="90" placeholder="Search a question number, exam or concept"></label>
 <label>Exam<select data-pyq-exam><option value="all">All exams</option>{''.join(f'<option value="{k}">{e(v)}</option>' for k,v in EXAMS.items())}</select></label>
 <label>Year<select data-pyq-year><option value="all">All years</option>{opt(years)}<option value="0">Year to verify</option></select></label>
 <label>Topic<select data-pyq-topic><option value="all">All topics</option>{opt(topics)}</select></label>
 <label>Concept<select data-pyq-concept><option value="all">All concepts</option>{opt(concepts)}</select></label>
 </div>
 <div class="pyq-toolbar"><span data-pyq-count role="status" aria-live="polite">{len(items)} records found</span><button type="button" data-pyq-clear>Clear filters</button></div>
 <div class="pyq-record-grid" data-pyq-results>{''.join(cards)}</div><div class="pyq-empty" data-pyq-empty hidden><h3>No matching past papers.</h3><p>Try a different year or concept. We are still checking and organising older papers.</p><button class="button button-light" type="button" data-pyq-clear>Clear filters</button></div>
 <p class="pyq-accuracy"><strong>About this library:</strong> APPSC 2024 contains question-by-question key references. Other paper entries are source-level indexes until individual questions are checked. Papers in Google Drive remain private; this site links to official exam authorities when a source is available. Answers are not labelled official unless the underlying key has been checked.</p></div></section>'''
