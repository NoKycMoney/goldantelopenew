#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

USER_SITE="$(python -c 'import site; print(site.getusersitepackages())')"
case "$USER_SITE" in
  "$PROJECT_ROOT"/.pythonlibs/*) ;;
  *)
    echo "Refusing to install dependencies outside the workspace: $USER_SITE" >&2
    exit 1
    ;;
esac

if python -m pip show gradio >/dev/null 2>&1; then
  python -m pip uninstall --yes --break-system-packages gradio
fi

python -m pip install --user --break-system-packages -r requirements.txt
python -m pip check
