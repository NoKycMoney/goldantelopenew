---
name: GitHub snapshot sync
description: Reliable GitHub synchronization when the local repository history is shallow or unrelated to the destination history.
---

When synchronizing a shallow local repository to a separate GitHub branch, publish a self-contained root snapshot rather than pushing the local commit history. Keep authentication sessions and other local credentials out of the snapshot.

**Why:** A normal push from an unrelated shallow history can make the remote unpacker request an object that is not present locally. The GitHub connector proxy may also reject large or HTML request bodies through its Cloudflare layer even when the OAuth connection is healthy.

**How to apply:** Build a temporary sanitized index from the current working tree, write a root tree/commit, and push it only to the dedicated sync branch. Before importing a remote snapshot, inspect its tree for session files and exclude them; verify the branch tree and confirm the protected/default branch SHA is unchanged.