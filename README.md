# Aptitude Mind Plus — Standalone Educational Website

This is the **website only**. The Instagram/Facebook daily publisher is a separate project and is **not included**. This repository should be named `aptitude-mind-plus` under your GitHub account, with the public website branded **Aptitude Mind Plus**.

## Site features

- Minimal blue-and-white responsive pages: Home, **Free Video Lessons**, Concepts, Practice, PYQs, Courses, Tutoring, Submit a Question, and Admin Review.
- **Free-first model:** original explanations, free guided/video lessons, courses, PYQs and practice are available to everyone. Some advanced workbooks will be paid when ready; paid files require secure fulfilment before sale. Optional personal tutoring/doubt-solving is advertised from **₹3,000 per support programme**; the exact session scope and terms must be agreed before payment.
- Contributors may submit text and an optional compressed photo after asserting sharing rights. Submissions remain private until admin approval; verified official PYQs require separate human verification.
- A private admin dashboard for review, rejection, publishing, and course enquiries. A student cannot publish directly.
- No credit-card collection, payment checkout, trackers, arbitrary external package dependencies, or invented official exam papers.

## Architecture — responsible and low cost

| Service | Role | Free start |
| --- | --- | --- |
| GitHub | Dedicated version-controlled source repo | Yes |
| Cloudflare Pages | Public site, SSL, Functions | Yes, subject to limits |
| Cloudflare D1 | Question metadata, approval states, applications | Yes, subject to limits |
| Cloudflare R2 **Standard** | Private uploaded images, future approved PDFs | Yes, 10 GB-month storage allowance and operation limits |
| Google Drive | Owner's existing 5 TB archive, backups and original teaching notes | Already available |

**Important:** Keep the R2 bucket **private**. Images are read only through the `/api/image/{id}` Function after D1 permission checks. Do not make submitted file objects public directly. No personal Google Drive OAuth credentials should be embedded in this website.

For large user uploads, paid digital content, automated backups, and scale, plan a second-phase security/privacy review, retention/deletion policy and billing alerts. Free-tier quotas are not guarantees of unlimited usage.

## Deploy — do this in order

1. Create a new **public** GitHub repository `aptitude-mind-plus` and put **the contents of this folder** at its repository root. Keep `aptitude-mind-plus-daily` untouched for Instagram/Facebook automation. This package can be uploaded to the new repo, or ChatGPT can populate it after you create an empty repo.
2. In Cloudflare Dashboard > **Workers & Pages > Create > Pages > Connect to Git**, select `VenkataKrishnaYalagala/aptitude-mind-plus`, production branch `main`, framework `None`, root directory **empty/default**, build command **blank**, output directory `public`. This preserves Pages Functions under the project root.
3. Set the project name to `aptitudemindplus` if available. This gives a temporary `*.pages.dev` address while the domain is being registered. A custom domain is optional for the first deployment.
4. In Cloudflare **D1**, create a database `aptitudemindplus-db`. Initialize it using the SQL in `schema/schema.sql` with D1's SQL Console, or the authenticated Wrangler command `npx wrangler d1 execute aptitudemindplus-db --remote --file=schema/schema.sql` from the repo root.
5. In Cloudflare **R2**, create a **Standard storage** bucket `amp-question-uploads` with public access **disabled**. If Cloudflare requests billing verification, check the account's payment and spending controls before enabling it.
6. Under Pages project **Settings > Bindings**, add D1 database binding **`DB`** to `aptitudemindplus-db` and R2 bucket binding **`UPLOADS`** to `amp-question-uploads`. Set both for production. Redeploy to apply.
7. Under Pages project **Settings > Variables and Secrets**, create encrypted secrets **`ADMIN_PASSWORD`** (unique 18+ characters) and **`SESSION_SECRET`** (unique random 32+ characters). Never paste secrets into GitHub, chat or public files. Redeploy again.
8. Check `/api/health` returns `{"ready":true}`. Log in at `/admin.html`. Submit a sample question at `/submit.html`, verify that it is **not public**, approve it, then check `/pyqs.html`. Submit a second question and reject it. Test an image and course enquiry too.
9. Set the actual YouTube, Instagram and Facebook URLs in `public/assets/config.js`, and provide the verified official brand logo (the included SVG is a temporary mark). Finalize a working contact address, privacy/retention policy, copyright process and course/refund terms before advertising paid courses or collecting real student contact details.
10. Register and attach `aptitudemindplus.com` **only after reviewing availability and registration/renewal prices at checkout**. Domain purchase is separate from free hosting. You do not need to buy hosting with your domain.

**Do not use drag-and-drop Direct Upload** for this full website: Cloudflare Pages Functions require Git integration or Wrangler deployment. Direct Upload via the dashboard will not deploy the Functions folder.

### Verify locally

```sh
npm test
python3 -m http.server 8000 --directory public
```

The visual static preview runs without a database, but the forms correctly stay inactive until D1, R2 and administrator secrets are connected. To make recurring content edits, use the free Pages CMS editor described below. For design/source changes, update `build_site.py` or `course_platform.py`, run `python3 build_site.py`, and commit the generated `public/*.html` files.

### Privacy, quality and security notes

- Content moderation has two separate properties: **approved** and **official source verified**. Approval does not imply it came from an official paper. Check source and copyright permissions before marking official.
- Submitted question JPEGs are compressed in the browser and stored in private R2. D1 stores the object key, not the image contents. All object reads are checked against an approved status or signed admin session.
- Files are not silently copied to Google Drive. You can archive approved resources manually, or later add a scoped authenticated backup job using Google Drive API; keep any authorization secrets out of GitHub.
- The current login uses a long password plus signed, HttpOnly session cookies. For a public launch, add Turnstile anti-bot checks and ideally Cloudflare Access for administrative protection. This starter is **not** an independent penetration test.
- Keep the admin endpoint private; never expose uploaded contributor contact information to search engines.
- Do not take payment until duration, syllabus, schedule, refund policy and service terms are clearly written and verified.
- Treat all student personal information with care and establish real deletion/retention controls before broad launch.


## Owner's no-code editor: Pages CMS (free)

The website includes `.pages.yml` and structured data in `content/`, so you can update text, free lessons, approved public YouTube links, prices, courses, announcement banners, optional course images and the official logo **without writing code**.

1. Open **https://app.pagescms.org** in a browser and sign in with the GitHub account that owns `VenkataKrishnaYalagala/aptitude-mind-plus`.
2. Approve the Pages CMS GitHub app for **only this website repository**, not all personal repositories. Your GitHub account controls who can edit.
3. Open `aptitude-mind-plus` in Pages CMS. The editor reads `.pages.yml` automatically.
4. To update a headline: choose **Website settings and homepage**, change the field, then **Save**.
5. To upload an image: open **Media**, upload the photo/logo, and choose its image field in **Website settings** or **Exam pathways**.
6. To add a video: open **Free lessons and YouTube videos**, add a lesson row, enter title, topic, description and a **public YouTube share URL**, and set **Published** to true. The player is automatically embedded in privacy-enhanced mode **only when a visitor clicks Play**. Blank or invalid video links produce no fake player.
7. To change exam course wording: open **Exam pathways**. Do not change the six internal exam codes. To edit the announcement strip: open **Announcement strip**.
8. Click **Save**. Pages CMS commits the data to GitHub. The `Publish edited learning content` GitHub Action regenerates the HTML and commits it to `main`. Cloudflare Pages' Git connection deploys the updated site automatically. Check the Actions tab for failures if the edit doesn't appear.

**What the visual editor does not cover:** changing the underlying layout, backend security or adding new exam categories requires a code change. The existing `public/` pages are generated files; avoid editing those directly because the next regeneration replaces them. This public CMS is for your content and official image assets, **not private student-uploaded files or admin secrets**.

**If you prefer a single deployment per edit:** set Cloudflare Pages' Build command once to `python3 build_site.py` (root `/`, output `public`) and disable `publish-content.yml`; this directly renders CMS edits during the Cloudflare build. The committed-pages workflow above works with the original `exit 0` setting and needs no repeated manual build.

## Free education + optional support business model

- **Open access:** Free original lessons, public YouTube embeds, guided notes, carefully reviewed PYQs, concept explanations, and quizzes. No compulsory registration or payments.
- **Personal help:** An optional ₹3,000 tutoring support programme offered through an enquiry only. Session count, duration, schedule, format, refund and cancellation terms need agreement before payment.
- **YouTube:** The original public video remains on YouTube while its privacy-enhanced embed appears on the website. Only the *eligible YouTube video owner* and YouTube share revenue from video-player advertisements. Embedding the player does not grant the website extra video-ad revenue.
- **Website AdSense (later):** Do not copy Google AdSense scripts to the site before obtaining approval for the final domain, publishing adequate original content and reviewing disclosures and Google policy. Once approved, add the exact publisher script and any required consent controls by a reviewed code change. **Never** pay a third-party claiming guaranteed AdSense approval. No ads are active in this codebase.
- **Google Business Profile:** Helps eligible tutoring businesses become discoverable on Search and Maps, but it is not a direct ad-revenue product. Verify eligibility before creating a listing.
- **Payments:** No checkout is active. A payment provider will require additional eligibility, fee, compliance, refund and privacy work. Do not store card data in D1, R2 or Google Drive.
- **Google Drive:** Use your existing private 5 TB archive for master notes and working materials; **do not** expose private Google Drive files publicly or use them as the anonymous upload backend.

The site's small public course images are saved with GitHub through Pages CMS. Student-uploaded images remain in private Cloudflare R2 behind moderation checks. Do not mix the two storage types.

## Admin and launch checks before taking real applications

Set up and test D1, R2, bindings `DB` / `UPLOADS`, and secrets `ADMIN_PASSWORD` / `SESSION_SECRET`; the public front end can be visited before this, but submissions stay disabled. Add Cloudflare Turnstile anti-bot protection, contact details, a privacy and deletion policy, and verified copyright permissions. Obtain the owner-supplied official logo before branding signoff. Provide captioned videos and descriptive lesson notes for accessibility and search visibility. YouTube videos can be edited and re-uploaded via the YouTube owner account, not the website CMS itself.


## Simplified learning navigation (development preview)

The site groups the previous Courses, Concepts and Video Lessons menu entries under a single **Learn** destination. The four top-level links are Learn, Practice, Past papers and Tutoring. The logo remains the home link. Existing `lessons.html` and `concepts.html` URLs continue to work and are linked inside Learn and the course details.

The Learn page offers exam filtering, fast local search, real course/topic links and a free learning sequence. The six exam detail pages link to relevant lesson notes, topics, original practice and the reviewed past-paper library. The optional **Save this course** button uses browser-only storage (no accounts or server-side tracking). We have not invented student ratings, course duration, certificates, payment gateways, recorded video lessons or exam results.

This feature is staged on `feature/visual-homepage-editor` for review and is not merged to the live site until the editor and backend deployment are verified.

## Latest learning model

All exam course resources, concept notes, original practice and available videos remain **free**. Optional personal tutoring is **₹2,999 per support programme**, subject to agreed session scope, schedule and terms. Past-paper references are indexed by exam, year, topic and concept; source status is shown and private Google Drive PDFs are **not** made public. A student can ask a **private doubt** separately from contributing a question to the public moderated library.

## Social links, comments, and study materials

The editor now exposes **Social accounts and community text**, **Public social posts to feature**, **Learner comments (permission required)**, and **Free and optional paid study materials** in Pages CMS. Leave Instagram and Facebook blank until you have verified the real official URLs. Only approved, consented, source-linked comments are shown as testimonials; no automated scraping or imaginary reviews. Public-post cards open the source on the original platform. Future paid downloads need authentication, checkout, protected delivery and legal/consumer terms. A planned workbook is not available for purchase. See content/social.json, content/social-posts.json, content/feedback.json, content/materials.json.
