---
name: GitHub listing imports
description: Constraints when importing listing JSON files from the goldantelope11 GitHub repository.
---

The repository’s Vietnam listing file can be committed as a Git LFS pointer while the referenced object is unavailable from GitHub. Treat the pointer as non-data and preserve the local Vietnam dataset; import only validated JSON content.

**Why:** Importing the pointer would replace a working JSON dataset with a 133-byte non-JSON file, and the LFS batch endpoint can report that the object does not exist.

**How to apply:** Fetch listing files from the intended branch, parse and validate them before writing, merge by `id`/`listing_id` with local records preferred on conflicts, and never import session or credential files.