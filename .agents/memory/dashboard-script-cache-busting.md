---
name: Dashboard script cache busting
description: Check the static JavaScript URL version when preview behavior appears stale after frontend edits.
---

Replit's preview can keep using a cached static JavaScript file after its source has changed.

**Why:** The visa landing route initially appeared to ignore the new startup behavior until the script URL's version query changed.

**How to apply:** When the served page reflects new HTML but old JavaScript behavior, check the script URL's cache-busting query before revising correct application logic.
