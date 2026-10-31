---
name: Telegram Ads rate limits
description: Operational constraint for target validation and ad creation through Telegram Ads API.
---

Telegram Ads API target-resolution requests can trigger a long `FLOOD_WAIT`; ad creation can then be rejected during the cooldown even when the ad payload is valid.

**Why:** A large burst of target checks caused the subsequent create request to be blocked for roughly 45 minutes.

**How to apply:** Validate candidate channels in small batches, stop immediately on a flood-wait response, and do not retry campaign creation until the cooldown has elapsed.
