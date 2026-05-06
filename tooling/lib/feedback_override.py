from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Optional


OVERRIDE_RE = re.compile(
    r"\[calyx-override:(?P<reason>[^|\]]+)(\|owner:(?P<owner>[^|\]]+))?(\|expires:(?P<expires>\d{4}-\d{2}-\d{2}))?\]"
)


def parse_override(text: str) -> Optional[Dict[str, str]]:
    m = OVERRIDE_RE.search(text or "")
    if not m:
        return None
    return {k: v for k, v in m.groupdict().items() if v}


def validate_override(ov: Dict[str, str], cfg: Dict) -> bool:
    if not ov:
        return False
    if cfg["override"].get("require_owner", True) and "owner" not in ov:
        return False
    if cfg["override"].get("require_expiry", True) and "expires" not in ov:
        return False
    return True


def log_override(path: Path, payload: Dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
