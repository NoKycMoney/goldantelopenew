---
name: Telegram entertainment visibility
description: Rules for keeping entertainment listings aligned with their Telegram groups.
---

Only show entertainment listings carrying the internal confirmation that their source message is still present in the country’s entertainment Telegram group. Store this confirmation separately from channel metadata, and refresh it when new posts arrive or during the periodic group audit.

**Why:** API response preparation masks internal source-channel fields for clients. Using those fields as the sole visibility signal made later requests lose the ability to distinguish verified listings from stale entries.

**How to apply:** When changing the entertainment parser, persistence, or response preparation, preserve the confirmation marker in server-side storage, copy response objects before masking internal fields, and keep the entertainment response uncached so Telegram removals are reflected immediately.