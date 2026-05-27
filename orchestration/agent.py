"""Agent construction for the pipeline.

This module wires a `StateGraph` with two principal nodes:
- `llm`: invokes the main LLM to produce the next message
- `tools`: executes side-effecting tool calls extracted from AI messages

The compiled agent is used by the runner to iteratively call the LLM and
apply tool-driven edits to the in-memory data graph.
"""

from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime
from langgraph.prebuilt import tools_condition
from langgraph.types import Command

from orchestration.tools import ToolClass
from orchestration.tracing import append_trace
from models.data_models import TaskState, TaskContext
from orchestration.tests import test_calls_basic, test_calls_basic1


def build_agent(tool_obj: ToolClass):
    """Construct and compile the agent StateGraph using `tool_obj`.

    The returned compiled agent exposes an `invoke` method that accepts a
    `TaskState` and `TaskContext` and drives the LLM ↔ tools loop until
    termination conditions are reached.
    """

    def llm(state: TaskState, runtime: Runtime[TaskContext]):
        """LLM node: call the configured LLM and increment the iteration
        counter, or terminate when `max_iterations` is reached.
        """
        if state["iterations"] < runtime.context["config"]["runtime"]["max_iterations"]:
            append_trace(runtime.context["tracing_path"], "run.entry.agent.llm.invoke", payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": state["iterations"]
            })
            
            response = runtime.context["main_llm"].invoke(state["messages"])
            #response = test_calls_basic1(state["iterations"])
            
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

    # Add nodes: the LLM node and the tools node produced by ToolClass
    agent.add_node("llm", llm)
    agent.add_node("tools", tool_obj.build_tool_node())
    
    # Start by invoking the LLM; transition to tools when tool calls are present
    agent.add_edge(START, "llm")
    agent.add_conditional_edges("llm", tools_condition)
    
    return agent.compile()
