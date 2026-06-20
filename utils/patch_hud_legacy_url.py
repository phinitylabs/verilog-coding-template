#!/usr/bin/env python
"""Point the hud-python SDK's job/trace links at the legacy web UI.

Why this exists
---------------
HUD's v6 release moved the v4/v5 web app to ``https://legacy.hud.ai`` -- the
old ``https://hud.ai`` URL now serves the new (incompatible) v6 UI. The
hud-python SDK that this template pins (0.5.x) *hardcodes* ``https://hud.ai``
when it builds the job/trace URL it prints and auto-opens in your browser on
``uv run hud eval ...``. It ignores the ``HUD_WEB_URL`` setting for those two
links, so a ``.env`` override alone does nothing.

This script rewrites those two URLs in the *installed* package so the links
open the working (legacy) UI. Because the SDK lives in ``.venv`` (recreated by
``uv sync``), the change can't be committed -- run this once after install:

    uv run python utils/patch_hud_legacy_url.py

Re-run it after any ``uv sync`` or hud-python upgrade. It is idempotent.

Target base URL defaults to ``https://legacy.hud.ai`` but honours ``HUD_WEB_URL``
if you've set it, so power users can repoint without editing this file.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

OLD_BASE = "https://hud.ai"
NEW_BASE = os.environ.get("HUD_WEB_URL", "https://legacy.hud.ai").rstrip("/")

# Files (relative to the installed `hud` package) and the URL path prefixes that
# get rewritten from OLD_BASE -> NEW_BASE within each.
TARGETS: dict[str, tuple[str, ...]] = {
    "eval/manager.py": ("/jobs/",),
    "eval/display.py": ("/trace/",),
}


def find_hud_pkg() -> Path:
    """Return the directory of the installed `hud` package."""
    import hud  # noqa: PLC0415 -- imported lazily so a missing SDK gives a clear error

    return Path(hud.__file__).resolve().parent


def patch_file(path: Path, prefixes: tuple[str, ...]) -> bool:
    """Rewrite OLD_BASE -> NEW_BASE for the given path prefixes. Returns True if changed."""
    text = path.read_text(encoding="utf-8")
    new_text = text
    for prefix in prefixes:
        new_text = new_text.replace(f"{OLD_BASE}{prefix}", f"{NEW_BASE}{prefix}")
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    if NEW_BASE == OLD_BASE:
        print(f"Target base is {NEW_BASE!r}; nothing to repoint.")
        return 0

    try:
        pkg = find_hud_pkg()
    except ImportError:
        print("ERROR: hud-python is not installed. Run `uv sync` first.", file=sys.stderr)
        return 1

    print(f"hud package : {pkg}")
    print(f"repoint     : {OLD_BASE} -> {NEW_BASE}\n")

    changed = 0
    for rel, prefixes in TARGETS.items():
        f = pkg / rel
        if not f.exists():
            print(f"  skip (not found, SDK layout changed?): {rel}")
            continue
        if patch_file(f, prefixes):
            changed += 1
            print(f"  patched : {rel}")
        else:
            # Either already patched, or the hardcoded URL moved in a newer SDK.
            already = NEW_BASE in f.read_text(encoding="utf-8")
            print(f"  ok      : {rel} ({'already legacy' if already else 'no match -- check SDK version'})")

    print(f"\nDone. {changed} file(s) patched.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
