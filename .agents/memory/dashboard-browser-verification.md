---
name: Dashboard browser verification
description: Reliable visual and HTML checks for dynamically rendered dashboard category pages.
---

Headless Chromium `--dump-dom` may hang on dynamic category pages even when the app server and Replit preview are working.

**Why:** These pages load listings and external media asynchronously, which can keep command-line browser dumping from finishing.

**How to apply:** Verify visual rendering with the app preview, use HTTP requests to inspect served HTML, and use focused code or API checks for dynamically generated listing content rather than repeatedly waiting on an unbounded DOM dump.
