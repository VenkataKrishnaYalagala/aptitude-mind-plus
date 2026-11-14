# Aptitude Mind Plus — Visual editor evaluation

This branch introduces a **preview-only visual homepage editor** so the website owner can test a WordPress-like workflow before changing the production website.

## Scope

- React 19 + Puck 0.24 drag-and-drop builder (`visual-editor/`)
- 8 approved components: hero, course shelf, featured free lesson, exam links, text, image, tutoring CTA and spacer
- Desktop/tablet/mobile previews, local autosaved drafts and JSON export
- Strict JSON schema validation in Cloudflare Function and Python static renderer
- Protected publish endpoint authenticated by the existing admin session, using a repository-scoped GitHub token stored as an encrypted Cloudflare secret
- Development-only GitHub Actions build and preview artifacts

## Safety gates before production

- [x] Verify Puck dependencies compile via GitHub Actions
- [ ] Check drag-and-drop editor interactions in an authenticated browser (static homepage desktop, tablet and mobile tests passed)
- [ ] Confirm Cloudflare Pages preview project correctly serves `/visual-editor/`
- [ ] Configure Cloudflare Access and verify unauthorized users cannot publish
- [ ] Test save-to-GitHub, generated HTML, and deployment end to end with a harmless edit
- [ ] Test recovery if saving fails and concurrent edits conflict
- [ ] Decide whether to add image upload and additional pages

Production remains on the existing Pages CMS until these gates are completed. The daily social automation project is unaffected.

## Clear navigation, international readability (new)

Primary navigation is now **Learn · Practice · Past papers · Tutoring**. Home is accessible from the official logo. The Learn catalog is the entry point for all exam-specific course guides and links to concepts and video lessons. Existing concept and video URLs remain valid for search engines, bookmarks, and older social posts, but no longer compete at the top navigation level.

The homepage has four purposeful sections. The visual editor still allows additional optional sections. Course detail guides display the connected learning steps, then syllabus and optional tutoring. Saved-course state lives only in the visitor's browser (localStorage); there is **no account, synced progress, paid checkout or certificate service**.

This is a deliberate first-party design using useful educational patterns rather than copying another platform's layout, names, ratings or proprietary graphics.


## New student learning navigation

Homepage Quick Links show Learn, Original Practice, Past Papers, Ask a Doubt and Tutoring. All lessons and resources remain free. Optional teacher support is ₹2,999 per support programme with the exact scope agreed before payment.

## Student Doubts backend

Doubts are sent privately to the owner and are **not** contributed exam questions. The owner can review the text under Student doubts, reply using their email app, and mark as answered. The site does not send email automatically and does not promise a fixed reply time. Before public launch, apply the incremental D1 migration at `schema/migrations/2026-11-student-doubts.sql` to the *existing* database and test with a sample doubt; never reset live data. No student contact data should appear in the public PYQ index.

## Past Papers archive status

`content/pyq-index.json` holds curated source metadata and APPSC 2024 Q121–150 answer references; it does not publish complete original paper text. User's Google Drive holds private archives; do not make them public or copy without reviewing rights and original papers. Individual paper excerpts require manual page-by-page provenance and copyright review before website publication.
