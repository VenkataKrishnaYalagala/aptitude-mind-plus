"""Test the Puck homepage renderer, including text escaping and image safety."""
import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from visual_home import validate_layout, render_home, render_item

ROOT=Path(__file__).resolve().parent.parent
seed=json.loads((ROOT/'content/homepage.visual.json').read_text(encoding='utf8'))
validate_layout(seed)
assert len(seed['content'])==7
assert all(render_item(item) for item in seed['content'])
assert '<a' in render_item(seed['content'][0])
assert 'doubts.html' in render_item(seed['content'][1])
assert 'FREE' in render_item(seed['content'][2])
assert 'practice.html#lesson' in render_item(seed['content'][3])
assert 'tutoring.html' in render_item(seed['content'][-1])
assert 'materials.html' in render_item(seed['content'][4])
assert 'community.html' in render_item(seed['content'][5])
with tempfile.TemporaryDirectory() as directory:
    tmp=Path(directory)/'home.json'
    seed['content'].append({'type':'TextSection','props':{'id':'test-escape','heading':'<script>alert(1)</script>','body':'A note','align':'left'}})
    tmp.write_text(json.dumps(seed),encoding='utf8')
    page=render_home(lambda page,title,description,body: body,tmp)
    assert '<script>alert(1)</script>' not in page
    assert '&lt;script&gt;alert(1)&lt;/script&gt;' in page
    seed['content'][0]['props']['primaryHref']='javascript:alert(1)'
    tmp.write_text(json.dumps(seed),encoding='utf8')
    try:
        render_home(lambda page,title,description,body:body,tmp)
        raise AssertionError('Unsafe href was accepted')
    except ValueError as error:
        assert 'Buttons must' in str(error)
print('PASS: homepage JSON safe HTML, local links and validated blocks')
