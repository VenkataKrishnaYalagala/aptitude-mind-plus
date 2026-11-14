'''Privacy-conscious, carefully curated community and material pages.

Never build a public testimonial from a user comment without verifiable source,
explicit permission and owner's approval. Never expose paid PDF files directly.
'''
from html import escape
from pathlib import Path
from urllib.parse import urlparse
import json
import re

DIR=Path(__file__).parent/'content'

def data(filename):
    return json.loads((DIR/filename).read_text(encoding='utf-8'))

SOCIAL=data('social.json')
POSTS=data('social-posts.json')
FEEDBACK=data('feedback.json')
MATERIALS=data('materials.json')

PLATFORM_HOSTS={
 'youtube':frozenset(('youtube.com','www.youtube.com','m.youtube.com','youtu.be','www.youtu.be')),
 'instagram':frozenset(('instagram.com','www.instagram.com')),
 'facebook':frozenset(('facebook.com','www.facebook.com','m.facebook.com','fb.watch')),
}
PUBLIC_PAGES=frozenset(('courses.html','lessons.html','concepts.html','practice.html','pyqs.html','doubts.html','tutoring.html','materials.html','community.html'))

def e(value): return escape(str(value),quote=True)

def verified_url(value, platform):
    if not isinstance(value,str) or len(value)>600: return ''
    try:
        parsed=urlparse(value)
        if (parsed.scheme!='https' or parsed.hostname not in PLATFORM_HOSTS.get(platform,()) or
                parsed.username or parsed.password or not parsed.path or parsed.path=='/' or
                any(ord(x)<32 for x in value)):
            return ''
    except ValueError: return ''
    return value

def safe_study_link(value):
    if not isinstance(value,str):return ''
    stem=value.split('#',1)[0]
    return value if stem in PUBLIC_PAGES and re.fullmatch(r'[a-z-]+\.html(?:#[a-z0-9_-]+)?',value) else ''

def social_profiles():
    return [(platform, verified_url(SOCIAL.get(platform+'_url',''),platform))
            for platform in ('youtube','instagram','facebook')
            if verified_url(SOCIAL.get(platform+'_url',''),platform)]

def approved_posts():
    return [x for x in POSTS if isinstance(x,dict) and x.get('published') is True and
            x.get('platform') in PLATFORM_HOSTS and verified_url(x.get('source_url'),x['platform']) and
            isinstance(x.get('title'),str) and 5<=len(x['title'])<=160][:6]

def approved_feedback():
    return [x for x in FEEDBACK if isinstance(x,dict) and x.get('approved') is True and
            x.get('permission_confirmed') is True and x.get('platform') in PLATFORM_HOSTS and
            verified_url(x.get('source_url'),x['platform']) and
            isinstance(x.get('quote'),str) and 12<=len(x['quote'])<=280 and
            isinstance(x.get('display_name'),str) and 2<=len(x['display_name'])<=90][:6]

def visible_materials():
    out=[]
    for x in MATERIALS:
        if not isinstance(x,dict) or x.get('published') is not True:continue
        if x.get('access') not in ('free','paid') or x.get('status') not in ('available','planned'):continue
        if not isinstance(x.get('title'),str) or not x['title'].strip():continue
        if x['access']=='free' and x['status']=='available' and not safe_study_link(x.get('href','')):continue
        # Never generate a direct link for a paid file; checkout needs a protected fulfilment service.
        out.append(x)
    return out

def channel_links(cls='social-pill'):
    return ''.join(f'<a class="{cls}" href="{e(url)}" rel="noopener noreferrer nofollow" target="_blank"><span class="social-icon social-{platform}" aria-hidden="true">{ {"youtube":"▶","instagram":"◎","facebook":"f"}[platform] }</span>{ {"youtube":"YouTube","instagram":"Instagram","facebook":"Facebook"}[platform] } <span aria-hidden="true">↗</span></a>' for platform,url in social_profiles())

def featured_post_markup(limit=3):
    out=[]
    for post in approved_posts()[:limit]:
        platform=post['platform'];url=verified_url(post['source_url'],platform)
        summary=str(post.get('summary',''))[:240]
        out.append(f'<a class="community-post" href="{e(url)}" rel="noopener noreferrer nofollow" target="_blank"><span class="community-meta">{e(platform.title())} · Public post <span aria-hidden="true">↗</span></span><h3>{e(post["title"])}</h3>{f"<p>{e(summary)}</p>" if summary else ""}<span class="community-origin">View the original post</span></a>')
    return ''.join(out)

def feedback_markup(limit=3):
    out=[]
    for item in approved_feedback()[:limit]:
        url=verified_url(item['source_url'],item['platform']);who=item['display_name']
        out.append(f'<figure class="voice-card"><blockquote>“{e(item["quote"])}”</blockquote><figcaption>{e(who)} · {e(item["platform"].title())} <a href="{e(url)}" target="_blank" rel="nofollow noopener noreferrer">View original ↗</a></figcaption></figure>')
    return ''.join(out)

def community_highlight(eyebrow='',heading='',description=''):
    links=channel_links()
    posts=featured_post_markup(2)
    reviews=feedback_markup(1)
    if not links and not posts and not reviews:
        return ''  # Never display invented or unverified community activity.
    # Design stays spacious with only 2-3 dynamic cards, never an unmoderated feed.
    left=f'''<div class="community-intro"><span class="ampv-eyebrow">{e(eyebrow or 'FROM THE CLASSROOM')}</span><h2>{e(heading or SOCIAL.get('section_heading','Connect with us.'))}</h2><p>{e(description or SOCIAL.get('section_description','Join our learning community.'))}</p><div class="social-links">{links}</div><a href="community.html" class="community-text-link">See our community updates <span aria-hidden="true">↗</span></a></div>'''
    right=f'<div class="community-preview">{posts}{reviews}</div>' if posts or reviews else '<div class="community-feature"><span>APTITUDE MIND PLUS / COMMUNITY</span><div>Learn.<br><em>Share.</em><br>Grow.</div><small>Short explanations · Exam tips · New lessons</small></div>'
    return f'<section class="community-section" id="community"><div class="ampv-wrap community-grid">{left}{right}</div></section>'

def community_page(shell):
    links=channel_links()
    posts=featured_post_markup(6)
    reviews=feedback_markup(6)
    sections=''
    if posts:
        sections+=f'<section class="community-body-section"><h2>Recent posts</h2><p>Visit the original post on the social platform.</p><div class="community-post-grid">{posts}</div></section>'
    if reviews:
        sections+=f'<section class="community-body-section"><h2>What learners have shared</h2><p>These comments have a linked original source and permission to appear here.</p><div class="community-post-grid">{reviews}</div></section>'
    if not posts and not reviews:
        sections='<section class="community-body-section community-body-empty"><h2>Find our lessons and updates</h2><p>We will share selected public posts and feedback here after checking the source and getting permission. Until then, you can follow the channels below.</p></section>'
    body=f'''<section class="community-page-hero"><div class="wrap"><span class="ampv-eyebrow">APTITUDE MIND PLUS COMMUNITY</span><h1>Learning is better when we share it.</h1><p>See the questions, lessons and study updates we share. Real learner feedback appears only after permission and review.</p><div class="social-links">{links}</div></div></section><div class="wrap community-body">{sections}<div class="community-invite"><h2>Want to share something about our lessons?</h2><p>Mention Aptitude Mind Plus on a public social post. We review the source and ask for the author's permission before featuring comments on this website.</p></div></div>'''
    return shell('community.html','Community and Social Updates','Official Aptitude Mind Plus social links, selected educational posts and genuine learner feedback.',body)

def material_cards():
    out=[]
    for item in visible_materials():
        access=item['access'];status=item['status'];free=access=='free'
        badge='Free' if free else 'Premium';price=item.get('price_inr')
        label='Available now' if status=='available' else 'Coming soon'
        if not free:
            label='Coming soon' if status=='planned' else 'Enquire before payment'
        slug=str(item.get('slug',''))[:50]
        kind=str(item.get('kind','Study material'))[:45]
        subtitle=str(item.get('summary',''))[:320]
        price_html=f'<span class="material-price">₹{int(price):,}</span>' if not free and isinstance(price,int) and price>0 else ''
        if free and status=='available':
            action=f'<a class="material-action" href="{e(safe_study_link(item["href"]))}">Open free material <span aria-hidden="true">↗</span></a>'
        else:
            action=f'<span class="material-not-yet">{e(label)}</span>'
        out.append(f'''<article class="material-card" data-material data-access="{access}" data-search="{e((item['title']+' '+kind+' '+subtitle+' '+str(item.get('exam',''))).lower())}"><div class="material-card-top"><span class="material-type">{e(kind)}</span><span class="material-badge material-{access}">{badge}</span></div><div class="material-cover material-cover-{access}"><div class="material-cover-art" aria-hidden="true"><span>AMP / MATERIALS</span><strong>{'02' if not free else '01'}</strong><i></i></div></div><div class="material-card-content"><h3>{e(item['title'][:130])}</h3><p>{e(subtitle)}</p><div class="material-bottom">{price_html}{action}</div></div></article>''')
    return ''.join(out)

def materials_page(shell):
    cards=material_cards()
    body=f'''<section class="materials-hero"><div class="wrap"><span class="ampv-eyebrow">STUDY MATERIALS</span><h1>Learn freely. Go further when you choose.</h1><p>Browse free notes and practice. Some additional workbooks will be paid, with prices and contents shown before anyone makes a purchase.</p><div class="materials-stats"><span>Open learning comes first</span><span>Optional premium study packs</span><span>No automatic payments</span></div></div></section><section class="materials-main"><div class="wrap"><div class="materials-toolbar"><div><h2>Find what you need</h2><p>These are the resources currently listed for Aptitude Mind Plus.</p></div><div class="materials-controls"><label class="materials-search-label" for="materials-search">Search resources</label><input id="materials-search" type="search" placeholder="Search study materials" data-material-search maxlength="100"><div class="material-filters" role="group" aria-label="Filter free or paid materials"><button type="button" class="is-active" data-material-filter="all" aria-pressed="true">All</button><button type="button" data-material-filter="free" aria-pressed="false">Free</button><button type="button" data-material-filter="paid" aria-pressed="false">Paid</button></div></div></div><p class="materials-count" data-material-count aria-live="polite"></p><div class="materials-grid">{cards}</div><p class="materials-empty" data-material-empty hidden>No materials match your search.</p><div class="materials-policy"><strong>A note about paid materials</strong><p>We will publish exact pricing, what is included, and how to access each paid file only after secure checkout and delivery are configured. Premium files are never exposed as public downloads. Teacher support is a separate optional service at ₹2,999.</p></div></div></section>'''
    return shell('materials.html','Free and Premium Study Materials','Find free aptitude materials and learn about optional future paid study packs.',body)


def materials_highlight(eyebrow='',heading='',description=''):
    return f'''<section class="materials-feature"><div class="ampv-wrap materials-feature-inner"><div class="materials-feature-copy"><span class="ampv-eyebrow">{e(eyebrow or 'STUDY MATERIALS')}</span><h2>{e(heading or 'Free resources. Optional extras.')}</h2><p>{e(description or 'Find free notes, practice and exam references. Detailed premium workbooks will be listed with clear prices when ready.')}</p><a href="materials.html" class="ampv-btn ampv-btn-primary">Explore study materials <span aria-hidden="true">↗</span></a></div><div class="materials-feature-art" aria-label="Free notes and upcoming premium workbooks"><div><span>01 / OPEN LEARNING</span><strong>Free notes &amp; practice</strong><small>Always available without payment</small></div><div><span>02 / OPTIONAL EXTRAS</span><strong>Premium workbooks</strong><small>Coming soon · prices published before purchase</small></div></div></div></section>'''
