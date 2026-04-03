from typing import TypedDict
from rdflib import Graph
from pydantic import BaseModel
from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime
from langgraph.prebuilt import tools_condition
from langgraph.types import Command
from langchain.chat_models import BaseChatModel
from langchain.messages import SystemMessage, HumanMessage

from orchestration.tools import ToolClass
from orchestration.tracing import append_trace
from models.data_models import ValidationReport
from prompts.prompt_engine import get_prompt, format_prompt
from core.shacl_functions import format_violations


class TaskState(TypedDict, total=False):
    messages: list
    iterations: int
    data_graph: Graph
    shacl_tool_call_id: str
    finish_tool_call_id: str
    to_end: bool
    task_manifest: dict
    violation_report: ValidationReport
    
class TaskContext(TypedDict):
    llm: BaseChatModel
    entry_id: str
    input_text: str
    ontology_graph: Graph
    shacl_graph: Graph
    artifact_dir: str
    tracing_path: str
    config: dict


def create_translation_response_model(num_violations: int) -> BaseModel:
    ...


def build_agent(tool_obj: ToolClass):
    
    def llm(state: TaskState, runtime: Runtime[TaskContext]):
        if state["iterations"] < runtime.context["config"]["runtime"]["max_iterations"]:
            append_trace(runtime.context["tracing_path"], "run.entry.agent.llm.invoke", payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": state["iterations"]
            })
            
            response = runtime.context["llm"].invoke(state["messages"])
            
            append_trace(runtime.context["tracing_path"], "run.entry.agent.llm.finished", payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": state["iterations"]
            })
            
            return {
                "messages": state["messages"].append(response),
                "iterations": state["iterations"] + 1
            }
        else:
            append_trace(runtime.context["tracing_path"], "run.entry.agent.max_iter_reached", payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": state["iterations"]
            })
            
            updated_manifest = state["task_manifest"]
            updated_manifest["done_reason"] = "max_iter_reached"
            
            return Command(
                update={
                    "task_manifest": updated_manifest
                },
                goto=END
            )
    
    def violation_translation(state: TaskState, runtime: Runtime[TaskContext]):
        trans_system_path = runtime.context["config"]["prompts"]["translation_system"]
        trans_system_prompt = get_prompt(trans_system_path)
        trans_system_msg = SystemMessage(content=trans_system_prompt)
        
        trans_user_path = runtime.context["config"]["prompts"]["translation_user"]
        trans_user_prompt = format_prompt(trans_user_path, violations=format_violations(state["violation_report"]))
        trans_user_msg = HumanMessage(content=trans_user_prompt)
        
        response_model = create_translation_response_model(len(state["violation_report"].violations))
        llm = runtime.context["llm"].with_structured_output(response_model)
        response = llm.invoke([trans_system_msg, trans_user_msg])
        #TODO: finish!
    
    def check_entities_typed(state: TaskState, runtime: Runtime[TaskContext]):
        #TODO: use Command's goto to route to END or llm
        pass
    
    agent = StateGraph(TaskState, TaskContext)

    agent.add_node("llm", llm)
    agent.add_node("tools", tool_obj.build_tool_node())
    agent.add_node("violation_translation", violation_translation)
    agent.add_node("check_entities_typed", check_entities_typed)
    
    agent.add_edge(START, "llm")
    agent.add_conditional_edges("llm", tools_condition)
    # tools route to subsequent nodes through Command's goto
    agent.add_edge("violation_translation", "llm")
    # check_entities_typed routes to llm or END through Command's goto
    
    return agent.compile()
