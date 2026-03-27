from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def append_trace(trace_path: Optional[str], event: str, payload: Optional[Dict[str, Any]] = None) -> None:
    if not trace_path:
        return
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "payload": payload or {},
    }
    with open(trace_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
