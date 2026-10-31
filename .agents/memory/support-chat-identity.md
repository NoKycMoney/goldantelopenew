---
name: Telegram identity and counts
description: Verified Telegram identity requirements for support chat history and unique-user counters.
---

Support chat messages and history must remain separate for each verified Telegram user. Use Telegram Mini App `initData` validated on the server as the source of the user's `@username` and profile photo; do not trust client-supplied identity fields. Returning Telegram users should reopen their own saved conversation across devices. Non-Telegram visits cannot be automatically identified and remain guest conversations.

The public site visitor counter uses daily unique IP fingerprints, not Telegram IDs. IPs are normalized and HMAC-hashed with a server-side key and date; never store raw IP addresses for this counter. Telegram chat ownership and Telegram-specific user counts still require server-verified Telegram IDs.

**Why:** The user changed the public counter requirement to unique visitor IPs while keeping verified Telegram IDs for chat identity.

**How to apply:** Use the privacy-preserving IP fingerprint for the public visitor counter. Validate signed Telegram Mini App `initData` server-side before using an ID for chat ownership or Telegram-specific counts; preserve stable per-user conversation mapping.

Telegram bot `/start` registrations use a separate cumulative counter. Add a unique Telegram user only after the admin group confirms that the user's ID and username notice was delivered.

**Why:** The user wants the bot counter to include only users whose registration notice reached the admin group, without mixing those users with website visitor analytics.

**How to apply:** Handle private-chat `/start` updates, deduplicate by Telegram ID, send the group notice first, then persist the count. Keep the website analytics counter separate.
