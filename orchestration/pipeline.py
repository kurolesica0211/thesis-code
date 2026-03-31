from typing import TypedDict
from langchain.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from rdflib import Graph

from models.data_models import Schema


class TaskState(TypedDict, total=False):
    messages: list
    data_graph: Graph
    run_manifest: dict
    
class TaskContext(TypedDict):
    entry_id: str
    input_text: str
    ontology_graph: Graph
    shacl_graph: Graph
    schema_def: Schema
    artifact_dir: str
    tracing_path: str
    config: dict


def build_agent():
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as exc:
        raise ImportError(
            "LangGraph is required for SHACL graph orchestration. Install with 'pip install langgraph'."
        ) from exc

    

    agent = StateGraph(TaskState)



    return agent.compile()
