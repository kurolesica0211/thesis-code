from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from typing import Any, Dict, Optional


# Global lock registry for thread-safe file writing
_trace_lock = threading.Lock()
_file_locks: Dict[str, threading.Lock] = {}


def _get_file_lock(path: str) -> threading.Lock:
    with _trace_lock:
        lock = _file_locks.get(path)
        if lock is None:
            lock = threading.Lock()
            _file_locks[path] = lock
        return lock


def init_artifact_files(artifacts_dir: str) -> None:
    os.makedirs(artifacts_dir, exist_ok=True)
    os.makedirs(os.path.join(artifacts_dir, "convos"), exist_ok=True)

    usage_path = os.path.join(artifacts_dir, "usage_metadata.json")
    graphs_path = os.path.join(artifacts_dir, "graphs.json")

    usage_lock = _get_file_lock(usage_path)
    with usage_lock:
        if not os.path.exists(usage_path):
            with open(usage_path, "w", encoding="utf-8") as f:
                json.dump({"translation": [], "final": []}, f, indent=4)

    graphs_lock = _get_file_lock(graphs_path)
    with graphs_lock:
        if not os.path.exists(graphs_path):
            with open(graphs_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)


def append_usage_metadata(artifacts_dir: str, entry_type: str, metadata: Dict[str, Any]) -> None:
    usage_path = os.path.join(artifacts_dir, "usage_metadata.json")
    lock = _get_file_lock(usage_path)
    with lock:
        with open(usage_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        if entry_type not in content:
            content[entry_type] = []

        content[entry_type].append(metadata)

        with open(usage_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4)


def append_graph_snapshot(
    artifacts_dir: str,
    graph_type: str,
    graph_turtle: str,
    iteration: int,
    source: str,
    tool_call_id: Optional[str] = None,
) -> None:
    graphs_path = os.path.join(artifacts_dir, "graphs.json")
    lock = _get_file_lock(graphs_path)
    entry = {
        "graph_type": graph_type,
        "iteration": iteration,
        "source": source,
        "tool_call_id": tool_call_id,
        "graph": graph_turtle,
    }
    with lock:
        with open(graphs_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        content.append(entry)

        with open(graphs_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4)


def append_trace(trace_path: Optional[str], event: str, payload: Optional[Dict[str, Any]] = None) -> None:
    if not trace_path:
        return
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "payload": payload or {},
    }
    with _trace_lock:
        with open(trace_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
