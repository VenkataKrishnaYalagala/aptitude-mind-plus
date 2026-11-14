"""Dependency-free checks for the website's static pages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

root = Path(__file__).resolve().parent.parent / 'public'
known = sorted(root.glob('*.html'))
assert len(known) == 17, f'Expected 16 pages, got {len(known)}'

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
        self.title = False
        self.alt_missing = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('a','link') and attrs.get('href'):
            self.paths.append(attrs['href'])
        if tag in ('img','script') and attrs.get('src'):
            self.paths.append(attrs['src'])
        if tag=='img' and 'alt' not in attrs:
            self.alt_missing += 1

for page in known:
    html = page.read_text(encoding='utf8')
    parser = References()
    parser.feed(html)
    assert '<title>' in html, f'Missing title {page.name}'
    assert '<meta name="description"' in html, f'Missing description {page.name}'
    assert not parser.alt_missing, f'Image missing alt in {page.name}'
    for path in parser.paths:
        scheme = urlsplit(path)
        if scheme.scheme or path.startswith(('//','#','mailto:','tel:')):
            continue
        dest=unquote(scheme.path)
        if not dest:
            continue
        candidate=(page.parent/dest).resolve()
        assert candidate.is_relative_to(root.resolve()), f'Unsafe relative path in {page.name}: {path}'
        assert candidate.exists(), f'Broken local reference in {page.name}: {path}'
assert 'rights' in (root/'submit.html').read_text()
assert 'LEARNING ACCESS' in (root/'courses.html').read_text()
assert 'FREE' in (root/'courses.html').read_text()
assert '₹3,000' in (root/'tutoring.html').read_text()
assert 'Free Video Lessons' in (root/'lessons.html').read_text()
assert 'admin' in (root/'admin.html').read_text()
print(f'PASS: {len(known)} HTML pages, page titles, image alt text, and all local links')

for exam in ('upsc','gate','ssc','bank','state','rail'):
    html=(root/f'course-{exam}.html').read_text(encoding='utf8')
    assert 'Course Guide' in html or 'COURSE GUIDE' in html
    assert 'SELF-PACED LEARNING' in html and 'FREE' in html
    assert 'tutoring.html?course=' in html
