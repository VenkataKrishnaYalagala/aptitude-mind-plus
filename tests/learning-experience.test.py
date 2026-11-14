"""Behavioral and responsive checks for consolidated learning experience."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re

ROOT=Path(__file__).resolve().parent.parent
PUBLIC=ROOT/'public'
CSS=[(PUBLIC/'assets/style.css').read_text(),(PUBLIC/'assets/visual-home.css').read_text(),(PUBLIC/'assets/engagement.css').read_text()]
SCRIPTS=[(PUBLIC/'assets/config.js').read_text(),(PUBLIC/'assets/app.js').read_text(),(PUBLIC/'assets/catalog.js').read_text(),(PUBLIC/'assets/videos.js').read_text(),(PUBLIC/'assets/pyq-index.js').read_text(),(PUBLIC/'assets/materials.js').read_text()]
OUT=Path('/mnt/data/amp-redesign/screenshots');OUT.mkdir(parents=True,exist_ok=True)

def load(page,path):
    source=(PUBLIC/path).read_text()
    source=re.sub(r'<script src="assets/[^\"]+" defer></script>', '', source)
    source=re.sub(r'<link rel="stylesheet" href="assets/[^\"]+">', '', source)
    page.set_content(source,wait_until='domcontentloaded')
    for sheet in CSS: page.add_style_tag(content=sheet)
    for script in SCRIPTS: page.add_script_tag(content=script)
    page.evaluate('window.scrollTo(0,0)')

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
    try:
        for width,height,label in [(1440,900,'desktop'),(810,1000,'tablet'),(390,844,'mobile')]:
            page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
            errors=[]
            page.on('pageerror',lambda e: errors.append(str(e)))
            load(page,'index.html')
            nav=page.locator('.desktop-nav .nav-link')
            assert nav.all_inner_texts()==['Learn','Practice','Past Papers','Tutoring']
            assert page.locator('.ampv-course').count()==3
            assert page.locator('a[href="doubts.html"]').count() >= 1
            assert page.locator('.ampv-lesson-feature a[href="practice.html#lesson"]').count()==1
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Homepage overflow at {label}'
            page.screenshot(path=str(OUT/f'homepage-{label}.png'),full_page=True)
            if label=='mobile':
                page.locator('[data-menu-trigger]').click()
                assert page.locator('[data-mobile-nav]').is_visible()
                assert page.locator('[data-mobile-nav] a[href="courses.html"]').is_visible()
            assert page.locator('.materials-feature').count()==1
            assert page.locator('.community-section').count()==1
            assert page.locator('.community-section .social-youtube').count()==1
            assert page.locator('.voice-card').count()==0
            load(page,'materials.html')
            assert page.locator('[data-material]').count()==4
            assert page.locator('[data-material-count]').inner_text()=='4 resources found'
            page.locator('[data-material-filter="paid"]').click()
            assert page.locator('[data-material]:visible').count()==1
            assert 'Coming soon' in page.locator('[data-material]:visible').inner_text()
            page.locator('[data-material-filter="free"]').click()
            assert page.locator('[data-material]:visible').count()==3
            page.locator('[data-material-search]').fill('units digit')
            assert page.locator('[data-material]:visible').count()==1
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Materials overflow at {label}'
            load(page,'community.html')
            assert page.locator('.social-youtube').count()>=1
            assert page.locator('.voice-card').count()==0
            assert page.locator('.community-post').count()==0
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Community overflow at {label}'
            load(page,'courses.html')
            assert page.locator('.market-course-card').count()==6
            assert page.locator('.learn-resource-card').count()==3
            assert page.locator('.learn-concept').count()==4
            assert page.locator('[data-course-count]').inner_text()=='6 courses'
            page.locator('[data-course-search]').fill('gate')
            assert page.locator('[data-market-course]:visible').count()==1
            page.locator('[data-course-clear]').first.click()
            page.locator('[data-course-filter="bank"]').click()
            assert page.locator('[data-market-course]:visible').count()==1
            page.locator('[data-course-filter="all"]').click()
            page.locator('[data-course-sort]').select_option('az')
            assert page.locator('[data-market-course]:visible').count()==6
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Catalog overflow at {label}'
            page.screenshot(path=str(OUT/f'learn-{label}.png'),full_page=True)
            load(page,'course-upsc.html')
            assert 'UPSC' in page.locator('h1').inner_text()
            assert page.locator('.detail-learning-step').count()==4
            assert page.locator('details.outline-module').count()==4
            assert page.locator('.detail-recommendations .market-course-card').count()==3
            save=page.locator('[data-save-course]')
            assert save.count()==1
            assert save.get_attribute('aria-pressed')=='false'
            save.click()
            assert save.get_attribute('aria-pressed')=='true'
            save.click()
            assert save.get_attribute('aria-pressed')=='false'
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Course detail overflow at {label}'
            page.screenshot(path=str(OUT/f'course-{label}.png'),full_page=True)
            load(page,'pyqs.html')
            assert page.locator('[data-pyq-record]').count()==55
            assert page.locator('[data-pyq-count]').inner_text()=='55 records found'
            page.locator('[data-pyq-exam]').select_option('gate')
            assert page.locator('[data-pyq-record]:visible').count()==9
            page.locator('[data-pyq-year]').select_option('2024')
            assert page.locator('[data-pyq-record]:visible').count()==8
            page.locator('[data-pyq-clear]').first.click()
            page.locator('[data-pyq-exam]').select_option('state')
            page.locator('[data-pyq-year]').select_option('2024')
            assert page.locator('[data-pyq-record]:visible').count()==30
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Past papers overflow at {label}'
            load(page,'doubts.html')
            assert page.locator('[data-doubt-form]').count()==1
            assert page.locator('[data-doubt-form] input[name=email]').count()==1
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Doubts overflow at {label}'
            load(page,'practice.html')
            assert page.locator('.quiz-card').count()==8
            load(page,'lessons.html')
            assert page.locator('.video-lesson-card').count()==1
            assert page.locator('iframe').count()==0
            assert not errors,(label,errors)
            print('PASS',label,'navigation, courses, filters, embedded resources, saved-course toggle, overflow')
            page.close()
    finally:
        browser.close()
