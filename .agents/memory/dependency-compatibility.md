---
name: Dependency compatibility
description: Why collector control pages avoid Gradio and how to handle the workspace installer quirk.
---

Keep the small standalone collector control pages independent of Gradio.

**Why:** Gradio's latest available release during remediation required Pillow below 13, while the reported image-decoder security fixes required Pillow 13. Flask retained the needed controls without forcing a vulnerable image library or overriding package metadata.

**How to apply:** Before adding a UI framework to the collectors, check its Pillow restrictions against the current security baseline. Verify the main app and each standalone service's requirements separately; they are installed independently.

The managed Python package installer can fail here with “User site-packages are disabled” even when the normal shell Python enables the workspace user site.

**Why:** The managed installer and shell can use different Python wrappers. Repeated managed install attempts did not fix this; the shell Python could install into the workspace user site.

**How to apply:** Confirm the shell's user site points inside the workspace before using it as a fallback. Nix requires pip's externally-managed-environment acknowledgement even for user-site operations. Keep the configured package firewall/index in place; do not modify the Nix store or bypass package security checks.

Removing a dependency from manifests does not remove its old copy from `.pythonlibs`; an obsolete package can keep reporting incompatibilities after a successful install.

**Why:** After Pillow was upgraded to 13, cached Gradio remained installed and still declared a Pillow `<13` requirement.

**How to apply:** When a security update removes a package, explicitly uninstall the stale copy and run `pip check` after installing the new requirements.
