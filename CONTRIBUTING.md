# Contributing to Aptitude Mind Plus

This repository is the **Aptitude Mind Plus** learning website, not the social-media publishing service. Keep changes focused on the site and verified learning content.

## Development

1. Create a topic branch and explain the intended change in a pull request.
2. Edit structured educational content in `content/` (or through the existing Pages CMS). The Python build scripts produce public pages; do not silently overwrite CMS-authored information.
3. Validate changes locally:

   ```sh
   npm test
   python3 build_site.py
   python3 tests/static_audit.py
   python3 -m py_compile build_site.py course_platform.py
   ```

4. Review the generated `public/` pages and any changes to Cloudflare Pages Functions.
5. Request review before merging changes that affect publication, privacy, authentication, payments or deployment settings.

## Content standards

- Explain the concept first, then worked examples, practice and previous-year questions.
- Label newly authored questions **original practice**.
- Label content **official PYQ** only when exam, year, paper and answer key have been checked against a trustworthy primary source.
- Do not upload copyrighted textbooks, examination papers, paid courses or other third-party materials without appropriate rights or permission.
- Keep student submissions and moderation records out of public GitHub history.
- Use descriptive filenames, alt text and accessible headings for learning media.

## Security and secrets

Never commit `.env` files, access tokens, student data, API credentials or private upload URLs. Use Cloudflare's encrypted secrets and private storage bindings as documented in the README. Do not include real credentials in issues or pull requests.

Public site assets under `public/media/` may be PNG, JPEG, SVG or WebP. These are intentionally **not** globally ignored by Git, so approved CMS uploads can be versioned.

For security reports, see [SECURITY.md](SECURITY.md).
