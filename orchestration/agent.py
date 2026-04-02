from typing import TypedDict
from rdflib import Graph
from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime
from langgraph.prebuilt import tools_condition
from langchain.chat_models import BaseChatModel

from orchestration.tools import ToolClass


class TaskState(TypedDict, total=False):
    messages: list
    data_graph: Graph
    run_manifest: dict
    shacl_tool_call_id: str
    finish_tool_call_id: str
    to_end: bool
    violation_report: ... #TODO: define the type when implementing the tool
    
class TaskContext(TypedDict):
    llm: BaseChatModel #TODO: don't forget to define the type
    entry_id: str
    input_text: str
    ontology_graph: Graph
    shacl_graph: Graph
    artifact_dir: str
    tracing_path: str
    config: dict
    task_manifest: dict


def build_agent(tool_obj: ToolClass):
    
    def llm(state: TaskState, runtime: Runtime[TaskContext]):
        #TODO: invoke and append AIMessage to the end
        pass
    
    def violation_translation(state: TaskState, runtime: Runtime[TaskContext]):
        pass
    
    def format_violations(state: TaskState, runtime: Runtime[TaskContext]):
        #TODO: add a ToolMessage with the formatted report
        pass
    
    def check_entities_typed(state: TaskState, runtime: Runtime[TaskContext]):
        #TODO: use Command's goto to route to END or llm
        pass
    
    agent = StateGraph(TaskState, TaskContext)

    agent.add_node("llm", llm)
    agent.add_node("tools", tool_obj.build_tool_node())
    agent.add_node("violation_translation", violation_translation)
    agent.add_node("check_entities_typed", check_entities_typed)
    agent.add_node("format_violations", format_violations)
    
    agent.add_edge(START, "llm")
    agent.add_conditional_edges("llm", tools_condition)
    # tools route to subsequent nodes through Command's goto
    agent.add_edge("format_violations", "llm")
    # check_entities_typed routes to llm or END through Command's goto
    
    return agent.compile()
