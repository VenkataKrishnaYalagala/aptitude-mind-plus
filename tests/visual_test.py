"""Self-contained Chromium render and interaction QA.

The test uses in-memory HTML/CSS/JS because network navigation is blocked by
some CI/sandbox browser environments. Static link checks run separately.
"""
from pathlib import Path
import re
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent.parent
site=root/'public'
shots=Path('/mnt/data/aptitude-mind-plus-course-preview')
shots.mkdir(parents=True,exist_ok=True)
style=(site/'assets/style.css').read_text()
app=(site/'assets/app.js').read_text()
catalog=(site/'assets/catalog.js').read_text()
videos=(site/'assets/videos.js').read_text()
config=(site/'assets/config.js').read_text()

def load(page,name):
    source=(site/name).read_text()
    source=re.sub(r'<script src="assets/[^\"]+" defer></script>', '', source)
    source=re.sub(r'<link rel="stylesheet" href="assets/style.css">', '', source)
    page.set_content(source,wait_until='domcontentloaded')
    page.add_style_tag(content=style)
    page.add_script_tag(content=config)
    page.add_script_tag(content=app)
    page.add_script_tag(content=catalog)
    page.add_script_tag(content=videos)

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
    try:
        for width,height,label in [(1440,900,'desktop'),(390,844,'mobile'),(768,1024,'tablet')]:
            page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
            errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            load(page,'index.html')
            assert page.locator('h1').inner_text().startswith('Understand aptitude')
            assert page.locator('.market-course-card').count()==3
            assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),f'Homepage overflow: {label}'
            page.screenshot(path=str(shots/f'home-{label}.png'),full_page=True)
            assert page.locator('.hero-search').get_attribute('action')=='courses.html'
            load(page,'courses.html')
            assert page.locator('[data-market-course]').count()==6
            assert page.locator('[data-course-count]').inner_text()=='6 courses'
            page.locator('[data-course-search]').fill('gate')
            assert page.locator('[data-market-course]:visible').count()==1
            page.locator('[data-course-clear]').first.click()
            assert page.locator('[data-market-course]:visible').count()==6
            page.locator('[data-course-filter="upsc"]').click()
            assert page.locator('[data-market-course]:visible').count()==1
            page.locator('[data-course-sort]').select_option('az')
            page.locator('[data-course-filter="all"]').click()
            assert page.locator('[data-market-course]:visible').count()==6
            assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),f'Catalog overflow: {label}'
            page.screenshot(path=str(shots/f'catalog-{label}.png'),full_page=True)
            load(page,'course-upsc.html')
            assert 'UPSC CSAT' in page.locator('h1').inner_text()
            assert page.locator('details.outline-module').count()==4
            assert 'FREE' in page.locator('.detail-price').inner_text()
            page.locator('details.outline-module').last.locator('summary').click()
            assert page.locator('details.outline-module').last.evaluate('(el)=>el.open')
            assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),f'Detail overflow: {label}'
            page.screenshot(path=str(shots/f'detail-{label}.png'),full_page=True)
            load(page,'lessons.html')
            assert page.locator('.video-lesson-card').count()==1
            assert page.locator('iframe').count()==0
            assert 'Read the free lesson' in page.locator('.video-lesson-card').inner_text()
            assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),f'Video library overflow: {label}'
            page.screenshot(path=str(shots/f'videos-{label}.png'),full_page=True)
            load(page,'practice.html')
            assert page.locator('.quiz-card').count()==8
            page.locator('.quiz-card').first.locator('input').nth(3).check()
            page.locator('[data-quiz-submit]').click()
            assert page.locator('[data-quiz-result]').is_visible()
            load(page,'submit.html')
            assert page.locator('input[type=file]').count()==1
            if label=='mobile':
                load(page,'index.html')
                page.locator('[data-menu-trigger]').click()
                assert page.locator('[data-mobile-nav]').is_visible()
            assert not errors,errors
            print(f'PASS: {label}: responsive, search, filters, course detail, practice, menu')
            page.close()
    finally:
        browser.close()
