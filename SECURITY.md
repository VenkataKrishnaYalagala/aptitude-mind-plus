# Security policy

This website handles learning content and may handle private student submissions, uploaded images and administrative access.

- **Do not** create a public GitHub issue or pull request containing passwords, session tokens, exploit details, private student submissions or other sensitive personal information.
- Use GitHub's private **Report a vulnerability** feature if it is available for this repository. Otherwise, contact the repository owner privately and ask for a secure reporting channel.
- Revoke and rotate credentials if an accidental exposure is suspected. Deleting a secret in a later commit is not sufficient because Git history can retain it.
- Site administrators should enforce least-privilege Cloudflare bindings and keep uploaded student files in a private bucket.
- Production data, private media and account credentials do not belong in this public source repository.

Security reports will be triaged by the repository owner. No public disclosure timeline is promised.
