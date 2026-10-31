---
name: Dashboard category routing
description: Keep direct category-page links from being overridden by the remembered tab during country initialization.
---

For Vietnam, Thailand, India, and Indonesia, category icons should open their dedicated category pages; contacts stays in-place. When opening a country-specific category URL, suppress route changes while `switchCountry` restores the previously selected tab, then activate the category named by the URL.

**Why:** the user wants separate category pages for all four countries except contacts, and country initialization can restore a saved tab that redirects away from the requested deep link.

**How to apply:** Keep each country's category-icon route map aligned with its SEO page paths, and preserve route suppression when changing startup routing or country selection.
