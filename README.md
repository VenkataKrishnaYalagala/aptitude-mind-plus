# Aptitude Mind Plus — Standalone Educational Website

This is the **website only**. The Instagram/Facebook daily publisher is a separate project and is **not included**. This repository should be named `aptitude-mind-plus` under your GitHub account, with the public website branded **Aptitude Mind Plus**.

## Site features

- Minimal blue-and-white responsive pages: Home, Concepts, Practice, PYQs, Courses, Tutoring, Submit a Question, and Admin Review.
- Original, arithmetic-tested practice and exam categories; each standard exam-specific aptitude course is advertised at **₹3,000** (course scope, dates and payment terms need confirmation before registration).
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

The visual static preview runs without a database, but the forms correctly stay inactive until D1, R2 and administrator secrets are connected. To make edits, edit `build_site.py`, run `python3 build_site.py` to generate pages, and commit the generated `public/*.html` files.

### Privacy, quality and security notes

- Content moderation has two separate properties: **approved** and **official source verified**. Approval does not imply it came from an official paper. Check source and copyright permissions before marking official.
- Submitted question JPEGs are compressed in the browser and stored in private R2. D1 stores the object key, not the image contents. All object reads are checked against an approved status or signed admin session.
- Files are not silently copied to Google Drive. You can archive approved resources manually, or later add a scoped authenticated backup job using Google Drive API; keep any authorization secrets out of GitHub.
- The current login uses a long password plus signed, HttpOnly session cookies. For a public launch, add Turnstile anti-bot checks and ideally Cloudflare Access for administrative protection. This starter is **not** an independent penetration test.
- Keep the admin endpoint private; never expose uploaded contributor contact information to search engines.
- Do not take payment until duration, syllabus, schedule, refund policy and service terms are clearly written and verified.
- Treat all student personal information with care and establish real deletion/retention controls before broad launch.
