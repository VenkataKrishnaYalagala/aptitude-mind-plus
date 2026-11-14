"""Verify source-only public embeds, review permissions, and paid-file safety."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import engagement as c

assert c.verified_url('https://www.youtube.com/@aptitudemindplus','youtube')
assert c.verified_url('https://www.instagram.com/example/p/abc123','instagram')
assert not c.verified_url('https://www.instagram.com.evil.test/p/x','instagram')
assert not c.verified_url('http://www.facebook.com/page','facebook')
assert not c.verified_url('javascript:alert(1)','youtube')
assert not c.verified_url('https://youtube.com@evil.test/@brand','youtube')
assert not c.verified_url('https://www.youtube.com/@brand','instagram')
assert c.safe_study_link('practice.html#lesson')
assert not c.safe_study_link('https://drive.google.com/file/d/private')
assert not c.safe_study_link('javascript:alert(1)')
assert not c.safe_study_link('../../secret.html')
assert not c.approved_posts()
assert not c.approved_feedback()
assert c.visible_materials()
assert len(c.visible_materials())==4
cards=c.material_cards()
assert 'material-paid' in cards and 'Coming soon' in cards
assert '₹2,999' in c.materials_page(lambda page,title,description,body:body)
assert not 'href=""' in cards
assert 'drive.google.com' not in cards
assert 'href="practice.html#lesson"' in cards
saved_feedback=c.FEEDBACK
saved_posts=c.POSTS
try:
    c.FEEDBACK=[{'display_name':'Learner','quote':'I learnt a clear method in this explanation.',
                 'platform':'instagram','source_url':'https://www.instagram.com/p/example',
                 'permission_confirmed':True,'approved':False}]
    assert not c.feedback_markup()
    c.FEEDBACK[0]['approved']=True
    assert 'Learner' in c.feedback_markup()
    c.FEEDBACK[0]['permission_confirmed']=False
    assert not c.feedback_markup()
    c.FEEDBACK[0]['permission_confirmed']=True
    c.FEEDBACK[0]['quote']='<script>alert("x")</script> this is a much longer review.'
    output=c.feedback_markup()
    assert '<script>' not in output and '&lt;script&gt;' in output
    c.FEEDBACK[0]['source_url']='https://instagram.com.evil.test/p/x'
    assert not c.feedback_markup()
    c.POSTS=[{'platform':'facebook','title':'A useful practice question','source_url':'https://www.facebook.com/example/posts/123','published':False}]
    assert not c.featured_post_markup()
    c.POSTS[0]['published']=True
    assert 'A useful practice question' in c.featured_post_markup()
    c.POSTS[0]['source_url']='https://unrelated.test/'
    assert not c.featured_post_markup()
finally:
    c.FEEDBACK=saved_feedback
    c.POSTS=saved_posts
print('PASS: source-host allowlists, author permission, owner approval, XSS escaping, paid file privacy')
