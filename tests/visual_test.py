from playwright.sync_api import sync_playwright
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
root=Path(__file__).resolve().parent.parent
class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(root/'public')))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
shots=Path('/mnt/data/aptitude-mind-plus-standalone-previews')
shots.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--no-proxy-server','--allow-file-access-from-files'])
 for size,name in [((1440,900),'desktop'),((390,844),'mobile')]:
  page=browser.new_page(viewport={'width':size[0],'height':size[1]},device_scale_factor=1)
  page.goto(base+'index.html',wait_until='networkidle')
  assert page.title().startswith('Understand Aptitude')
  assert page.locator('h1').inner_text().startswith('Aptitude.')
  assert page.evaluate('document.body.scrollWidth<=window.innerWidth'),f'Horizontal scroll on {name}'
  page.screenshot(path=str(shots/('home-'+name+'.png')),full_page=True)
  page.goto(base+'courses.html',wait_until='networkidle')
  assert page.locator('article.course-card').count()==6
  assert page.locator('.course-card').first.inner_text().count('₹3,000')==1
  page.screenshot(path=str(shots/('courses-'+name+'.png')),full_page=True)
  page.goto(base+'submit.html',wait_until='networkidle')
  assert page.locator('input[type=file]').count()==1
  assert 'requires setup' in page.locator('[data-backend-status]').inner_text()
  page.screenshot(path=str(shots/('submit-'+name+'.png')),full_page=True)
  page.goto(base+'practice.html',wait_until='networkidle')
  assert page.locator('.quiz-card').count()==8
  page.locator('.quiz-card').first.locator('input').nth(3).check()
  page.locator('[data-quiz-submit]').click()
  assert page.locator('[data-quiz-result]').is_visible()
  page.screenshot(path=str(shots/('practice-'+name+'.png')),full_page=True)
  if name=='mobile':
   page.goto(base+'index.html',wait_until='networkidle')
   page.locator('[data-menu-trigger]').click()
   assert page.locator('[data-mobile-nav]').is_visible()
   assert page.evaluate('document.body.scrollWidth<=window.innerWidth')
  page.close()
 browser.close()
server.shutdown()
print('PASS: Desktop/mobile, 6 courses, responsive layout, submission status, 8-question quiz, menu')
