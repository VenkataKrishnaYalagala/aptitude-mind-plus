# Aptitude Mind Plus — Visual editor evaluation

This branch introduces a **preview-only visual homepage editor** so the website owner can test a WordPress-like workflow before changing the production website.

## Scope

- React 19 + Puck 0.24 drag-and-drop builder (`visual-editor/`)
- 7 approved components: hero, exam links, course shelf, text, image, tutoring CTA and spacer
- Desktop/tablet/mobile previews, local autosaved drafts and JSON export
- Strict JSON schema validation in Cloudflare Function and Python static renderer
- Protected publish endpoint authenticated by the existing admin session, using a repository-scoped GitHub token stored as an encrypted Cloudflare secret
- Development-only GitHub Actions build and preview artifacts

## Safety gates before production

- [ ] Verify Puck dependencies compile via GitHub Actions
- [ ] Check desktop and mobile editor interactions in an actual browser
- [ ] Confirm Cloudflare Pages preview project correctly serves `/visual-editor/`
- [ ] Configure Cloudflare Access and verify unauthorized users cannot publish
- [ ] Test save-to-GitHub, generated HTML, and deployment end to end with a harmless edit
- [ ] Test recovery if saving fails and concurrent edits conflict
- [ ] Decide whether to add image upload and additional pages

Production remains on the existing Pages CMS until these gates are completed. The daily social automation project is unaffected.
