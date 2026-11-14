# Aptitude Mind Plus — Visual Homepage Editor (Puck pilot)

This folder is a **development prototype** of a WordPress-like drag-and-drop page editor powered by [Puck](https://puckeditor.com/) 0.24 (MIT).

## What works
- Drag permitted sections in the left sidebar onto the canvas; rearrange and delete sections.
- Click text blocks to change headlines, descriptions and button labels.
- Change the homepage font, hero background, course shelf size and image paths.
- Preview in desktop, tablet and phone viewports.
- Drafts persist in **this browser only** (localStorage). Export a JSON backup any time.
- After administrator login and secure Cloudflare configuration, **Publish** saves a reviewed page layout to GitHub's `content/homepage.visual.json`. The existing GitHub Action regenerates the static homepage and Cloudflare Pages deploys the result.

## What stays protected

The public site cannot be changed by anonymous visitors. `PUT /api/editor/home` requires your existing HMAC-signed admin session, same-origin requests and a private `GITHUB_CONTENT_TOKEN` Cloudflare Pages secret. Each editor block is validated on the server and rendered as escaped HTML by `visual_home.py`. Arbitrary scripts, HTML, and external image addresses are rejected.

The editor UI itself is a **development-only prototype** on `feature/visual-homepage-editor`. Do not merge it into the public site until it has passed real-device testing, admin sign-in, Cloudflare setup and a complete publish-and-redeploy test. For extra protection in production, configure Cloudflare Access to require your verified account on `/visual-editor/*`.

## Local preview

From the repository root:

```bash
npm install --prefix visual-editor
npm run dev --prefix visual-editor
```

Open the URL printed by Vite (usually `http://127.0.0.1:5173/visual-editor/`). Local draft editing works without Cloudflare or GitHub credentials. The secure publishing API will not work locally unless running through Pages Functions and signing in as admin.

The CI workflow `.github/workflows/visual-home-editor.yml` installs dependencies and verifies that Puck compiles. It also generates `public/visual-editor/` for branch preview. Do **not** use the original Pages build command to install dependencies yet.

## Enabling real publishing, later

1. Finish setting up Cloudflare D1, private R2 and `ADMIN_PASSWORD`, `SESSION_SECRET` for the existing admin sign-in. Test `/api/admin/session` from a signed-in browser.
2. Generate a **fine-grained GitHub personal access token** with only `Contents: Read and write` access to `VenkataKrishnaYalagala/aptitude-mind-plus`. Don't give it access to the daily publishing repo or other accounts.
3. In **Cloudflare Pages > Settings > Variables and Secrets**, add an **encrypted secret** named `GITHUB_CONTENT_TOKEN`. Never paste its value into chat, HTML, repository code or Pages CMS.
4. Apply suitable Cloudflare Access protection on the editor path and redeploy so the Function receives the secret.
5. Visit the protected editor, sign in, make a harmless text edit, choose Publish, and verify the GitHub Action and Cloudflare deployment; test rollback.

**Do not merge before those tests.** Puck has no separate licence fee; Cloudflare/GitHub quotas and any optional paid domain still apply.

## Current limitations

- This first pilot edits **the homepage only** and uses a set of approved layout components, not arbitrary freeform HTML.
- The image field accepts a local `/media/...` path uploaded through Pages CMS; a native image-uploader is a later improvement.
- The optional ₹3,000 tutoring programme price still comes from existing site settings; the editor can't change billing terms or collect payments.
- Other site pages, question moderation and lesson records remain on the current system.
- A successful GitHub commit is **not** a completed Cloudflare deployment; use the build dashboards to verify.
