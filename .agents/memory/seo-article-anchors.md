---
name: SEO article anchors
description: Keep article contents links aimed at visible, correct headings inside Telegram Mini App pages.
---

Use unique IDs for headings in each SEO article. Handle table-of-contents clicks within the source article and scroll with enough top offset to keep the heading below Telegram's fixed Mini App header.

**Why:** Multiple country and category articles share a dashboard template, and the fixed Telegram header can cover headings after native fragment scrolling.

**How to apply:** When changing SEO article rendering or TOCs, preserve article-scoped target lookup, unique heading IDs, and the fixed-header scroll offset; verify every TOC link resolves to the matching heading across country routes.
