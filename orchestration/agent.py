from typing import TypedDict, Annotated, List
from rdflib import Graph
from pydantic import BaseModel, create_model, Field
from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime
from langgraph.prebuilt import tools_condition
from langgraph.types import Command
from langchain.chat_models import BaseChatModel
from langchain.messages import SystemMessage, HumanMessage, ToolMessage
from operator import add

from orchestration.tools import ToolClass
from orchestration.tracing import append_trace
from models.data_models import ValidationReport
from prompts.prompt_engine import get_prompt, format_prompt
from core.shacl_functions import format_violations
from core.data_graph_functions import check_ents_typed
from helpers import strip_ns, strip_uri


class TaskState(TypedDict, total=False):
    messages: Annotated[list, add]
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
    tracing_path: str
    config: dict


class ViolationTranslation(BaseModel):
    explanation: str
    instruction: str


def create_translation_response_model(num_violations: int) -> BaseModel:
    TranslationOutput = create_model(
        "TranslationOutput",
        translations=(List[ViolationTranslation], Field(min_length=num_violations, max_length=num_violations))
    )
    return TranslationOutput


def violation_translation(state: TaskState, context: TaskContext):
        append_trace(context["tracing_path"], "run.entry.agent.violation_translation.start", payload={
            "entry_id": context["entry_id"],
            "shacl_tool_call_id": state["shacl_tool_call_id"]
        })
        
        trans_system_path = context["config"]["prompts"]["translation_system"]
        trans_system_prompt = get_prompt(trans_system_path)
        trans_system_msg = SystemMessage(content=trans_system_prompt)
        
        trans_user_path = context["config"]["prompts"]["translation_user"]
        trans_user_prompt = format_prompt(trans_user_path, violations=format_violations(state["violation_report"]))
        trans_user_msg = HumanMessage(content=trans_user_prompt)
        
        response_model = create_translation_response_model(len(state["violation_report"].violations))
        llm = context["llm"].with_structured_output(response_model)
        response = llm.invoke([trans_system_msg, trans_user_msg])
        
        report = state["violation_report"].model_copy()
        for i, v in enumerate(report.violations):
            v.llm_explanation = response.translations[i].explanation
            v.llm_instruction = response.translations[i].instruction
            
        append_trace(context["tracing_path"], "run.entry.agent.violation_translation.finish", payload={
            "entry_id": context["entry_id"],
            "shacl_tool_call_id": state["shacl_tool_call_id"]
        })
        
        state["violation_report"] = report
        
        return (
            format_violations(report, state["data_graph"], context["ontology_graph"], context["shacl_graph"]),
            report,
            state["shacl_tool_call_id"]
        )
        

def check_entities_typed(state: TaskState, context: TaskContext):
        append_trace(context["tracing_path"], "run.event.agent.check_ents_typed.start", payload={
            "entry_id": context["entry_id"]
        })
        
        not_typed = check_ents_typed(state["data_graph"])
        if not bool(not_typed):
            append_trace(context["tracing_path"], "run.event.agent.check_ents_typed.finish", payload={
                "entry_id": context["entry_id"],
                "result": "all_typed"
            })
            
            return END
        else:
            not_typed_str = [strip_uri(strip_ns(str(n))) for n in not_typed]
            
            append_trace(context["tracing_path"], "run.event.agent.check_ents_typed.finish", payload={
                "entry_id": context["entry_id"],
                "result": "not_all_typed",
                "not_typed_nodes": not_typed_str
            })
            
            return (
                format_prompt(context["config"]["prompts"]["not_typed"], nodes=not_typed_str),
                state["finish_tool_call_id"]
            )


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
                "messages": [response],
                "iterations": state["iterations"] + 1
            }
        else:
            append_trace(runtime.context["tracing_path"], "run.entry.agent.max_iter_reached", payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": state["iterations"]
            })
            
            updated_manifest = state["task_manifest"].copy()
            updated_manifest["done_reason"] = "max_iter_reached"
            
            return Command(
                update={
                    "task_manifest": updated_manifest
                },
                goto=END
            )
    
    agent = StateGraph(TaskState, TaskContext)

    agent.add_node("llm", llm)
    agent.add_node("tools", tool_obj.build_tool_node())
    
    agent.add_edge(START, "llm")
    agent.add_conditional_edges("llm", tools_condition)
    
    return agent.compile()
