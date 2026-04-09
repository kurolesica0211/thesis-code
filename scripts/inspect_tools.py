import sys
import json
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestration.tools import ToolClass
from langchain.chat_models import init_chat_model
from loaders import base_family_loader

loader = base_family_loader.get_loader()
task_entry = next(loader.load())
tool_obj = ToolClass(task_entry.schema_def, task_entry.data_graph)

llm = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite-preview",
)
llm = llm.bind_tools(tool_obj.tools_schemas, tool_choice="any")


def _json_safe(value: Any, *, _seen: set[int] | None = None, _depth: int = 0):
    if _seen is None:
        _seen = set()
    if _depth > 8:
        return "<max_depth_reached>"

    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    value_id = id(value)
    if value_id in _seen:
        return "<cycle_ref>"

    if isinstance(value, dict):
        _seen.add(value_id)
        return {
            str(k): _json_safe(v, _seen=_seen, _depth=_depth + 1)
            for k, v in value.items()
        }
    if isinstance(value, (list, tuple, set)):
        _seen.add(value_id)
        return [_json_safe(v, _seen=_seen, _depth=_depth + 1) for v in value]
    if isinstance(value, type):
        return f"<type {value.__module__}.{value.__name__}>"
    return repr(value)


def build_bound_tools_view(bound_llm) -> dict:
    kwargs = getattr(bound_llm, "kwargs", {})
    tools_payload = kwargs.get("tools") if isinstance(kwargs, dict) else None

    return {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "wrapper_type": f"{type(bound_llm).__module__}.{type(bound_llm).__name__}",
        "bound_type": (
            f"{type(bound_llm.bound).__module__}.{type(bound_llm.bound).__name__}"
            if hasattr(bound_llm, "bound") else None
        ),
        "tool_choice": kwargs.get("tool_choice") if isinstance(kwargs, dict) else None,
        "tools_as_seen_by_model": _json_safe(tools_payload),
        "all_bind_kwargs": _json_safe(kwargs),
        "source_tool_schema_names": [schema.__name__ for schema in tool_obj.tools_schemas],
    }


output_path = Path(__file__).with_name("inspect_tools_output.json")
payload = build_bound_tools_view(llm)
output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Wrote tool binding view to: {output_path}")

