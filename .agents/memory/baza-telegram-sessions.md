---
name: Baza Telegram sessions
description: Authentication and privacy constraints for the Hugging Face Vietnam user collector.
---

The Baza collector must use a separate authorized Telethon StringSession from the live Replit parser. The collector exports user IDs, public usernames, names, activity and source chats, but deliberately does not collect phone numbers.

**Why:** Telegram rejects concurrent connections that reuse the same auth key with `AuthKeyDuplicated`, and the collector's output is intended to remain within Telegram's available non-phone profile data.

**How to apply:** Create or refresh a dedicated session for the collector, store it only as a Hugging Face Space secret, and keep Excel/JSON output in the authenticated dataset repository because Space filesystem storage is ephemeral.