import os
from typing import Any, Dict, Optional, TypedDict

from models.data_models import BatchExtractionResult
from validators.shacl_validator import OntologyIndex


class TaskState(TypedDict, total=False):
    pass


def build_shacl_batch_graph():
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as exc:
        raise ImportError(
            "LangGraph is required for SHACL graph orchestration. Install with 'pip install langgraph'."
        ) from exc

    

    graph = StateGraph(TaskState)



    return graph.compile()
