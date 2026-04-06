from pydantic import create_model, Field, BaseModel, ValidationError
from langchain.tools import tool
from langgraph.types import Command
from langchain.messages import ToolMessage, AIMessage
from typing import type, Literal, Callable, TypedDict
from rdflib import Graph
from langgraph.runtime import Runtime
from langchain_core.messages.content import ToolCall
from langgraph.graph import END

from models.data_models import Schema
from orchestration.tracing import append_trace
from core.data_graph_functions import add_class as add_class_core
from core.data_graph_functions import remove_class as remove_class_core
from core.data_graph_functions import add_triple as add_triple_core
from core.data_graph_functions import remove_triple as remove_triple_core
from core.shacl_functions import pyshacl_validate, format_violations
from orchestration.agent import TaskState, TaskContext, violation_translation, check_entities_typed


class _ToolRuntime(BaseModel):
    state: TaskState
    context: TaskContext
    tool_call_id: str


class ToolClass:
    tools: dict[str, Callable]
    arg_schemas: dict[str, BaseModel]
    Relation: type
    Class: type
    
    
    def __init__(self, schema: Schema):
        self.Relation = Literal[tuple([reldef.relation for reldef in schema.relations])]
        self.Type = Literal[tuple(schema.entities)]
        
        add_class_defs = {
            "subject": (str, Field(description="A node in the data graph to which you want to assign a class.")),
            "type": (self.Type, Field(description="A type (out of the list of allowed entity types) " + 
                                                    "that you want to assign to the subject node."))
        }
        remove_class_defs = {
            "subject": (str, Field(description="A node in the data graph which class you want to remove.")),
            "type": (self.Type, Field(description="A type (out of the allowed entity types) " +
                                                    "that is assigned to the subject and should be removed"))
        }
        AddClass = create_model("AddClass", **add_class_defs)
        AddClass.__doc__ = """
        Use this tool to assign a class to a node. This is essentially AddTriple with relation being rdf:type
        and object being an allowed entity type. Note that it does not matter whether the subject node already
        exists (participates in any triples), the class assignment is anyway valid. Make sure that all nodes
        have classes assigned to them!
        """
        RemoveClass = create_model("RemoveClass", **remove_class_defs)
        RemoveClass.__doc__ = """
        Use this tool to remove a class assigned to a node. This is essentially RemoveTriple with relation
        being rdf:type and object being an allowed entity type. Make sure that the subject node actually
        has that class assigned to it which you want to remove! And also make sure that all nodes have
        classes assigned to them!
        """
        
        add_triple_defs = {
            "subject": (str, Field(description="A subject node of the triple.")),
            "relation": (self.Relation, Field(description="A relation (out of the allowed relations) " + 
                                                            "defined between the subject and object of this triple")),
            "object": (str, Field(description="An object node of the triple."))
        }
        remove_triple_defs = {
            "subject": (str, Field(description="An existing subject node of the triple to be removed.")),
            "relation": (self.Relation, Field(description="A relation (out of the allowed relations) defined " + 
                                                            "between the subject and object of the triple to be removed")),
            "object": (str, Field(description="An existing object node of the triple to be removed"))
        }
        AddTriple = create_model("AddTriple", **add_triple_defs)
        RemoveTriple = create_model("RemoveTriple", **remove_triple_defs)
        AddTriple.__doc__ = """
        Use this tool to add a triple to the data graph. Make sure the relation comes from the list of allowed relations
        for this ontology.
        """
        RemoveTriple.__doc__ = """
        Use this tool to remove a triple from the data graph. Make sure the triple that you are about to remove actually exists.
        """
        
        ValidateShacl = create_model(
            "ValidateShacl",
            __doc__="""Use this tool to validate that the current data graph adheres to the ontology.
                        The validation is performed through SHACL, the shapes are pre-generated.
                        The tool does not have any input arguments, the data graph is passed internally."""
        )
        Finish = create_model(
            "Finish",
            __doc__="""Use this tool to finish the work. No input arguments required."""
        )
        
        self.tools_schemas = [AddClass, RemoveClass, AddTriple, RemoveTriple, ValidateShacl, Finish]
        self.tools = {
            "AddClass": self.add_class,
            "RemoveClass": self.remove_class,
            "AddTriple": self.add_triple,
            "RemoveTriple": self.remove_triple,
            "ValidateShacl": self.validate_shacl,
            "Finish": self.finish
        }
        self.data_graph_edit_tools = ["AddClass", "RemoveClass", "AddTriple", "RemoveTriple"]
        
        
    def build_tool_node(self):
        
        def execute_tool_calls(state: TaskState, runtime: Runtime[TaskContext]):
            append_trace(runtime.context["tracing_path"], "run.entry.agent.tools.start", payload={
                "entry_id": runtime.context["entry_id"]
            })
            
            last_msg = state["messages"][-1]
            if type(last_msg) is AIMessage:
                last_msg: AIMessage
                tool_calls: list[ToolCall] = last_msg.tool_calls
                outputs = []
                for call in tool_calls:
                    tool_runtime = _ToolRuntime(
                        state=state,
                        context=runtime.context,
                        tool_call_id=call["id"]
                    )
                    output = self.tools[call["name"]](tool_runtime, **call["args"])
                    if call["name"] in self.data_graph_edit_tools:
                        state["data_graph"] = output[0]
                    elif call["name"] == "ValidateShacl":
                        state["violation_report"] = output[1]
                    outputs.append((output, call["name"]))
                
                append_trace(runtime.context["tracing_path"], "run.entry.agent.tools.executed_tools", payload={
                    "entry_id": runtime.context["entry_id"]
                })
                
                messages = []
                for i, (output, name) in enumerate(outputs):
                    if name in self.data_graph_edit_tools:
                        if (i+1 < len(outputs)) and (outputs[i+1][-1] in self.data_graph_edit_tools):
                            messages.append(ToolMessage(
                                content="Look at the messages below to see the final data graph after the sequence of edits.",
                                tool_call_id=output[-1]
                            ))
                        else:
                            messages.append(ToolMessage(
                                content=f"The final data graph after the sequence of edits:\n\n  {output[0].serialize(format="turtle")}",
                                tool_call_id=output[-1]
                            ))
                    elif name == "ValidateShacl":
                        messages.append(ToolMessage(
                            content=output[0],
                            tool_call_id=output[-1]
                        ))
                    elif name == "Finish":
                        if type(output) is not tuple and output == END:
                            append_trace(runtime.context["tracing_path"], "run.entry.agent.tools.finish!", payload={
                                "entry_id": runtime.context["entry_id"]
                            })
                            return Command(goto=END)
                        else:
                            messages.append(ToolMessage(
                                content=output[0],
                                tool_call_id=output[-1]
                            ))
                            
                append_trace(runtime.context["tracing_path"], "run.entry.agent.tools.formatted_messages", payload={
                    "entry_id": runtime.context["entry_id"]
                })
                
                return Command(
                    update={
                        "messages": messages,
                    },
                    goto="llm"
                )
            else:
                raise Exception("TERRIBLE ERROR: the last message is not AIMessage")
        
        return execute_tool_calls

        

    def add_class(self, runtime: _ToolRuntime, subject: str, type: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.add_class.start",
            payload={
                "entry_id": runtime.context["tracing_path"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "type": type
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        data_graph = add_class_core(data_graph, subject, type)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.add_class.finish",
            payload={
                "entry_id": runtime.context["tracing_path"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "type": type
            }
        )
        
        return (data_graph, runtime.tool_call_id)
    
    def remove_class(self, runtime: _ToolRuntime, subject: str, type: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.remove_class.start",
            payload={
                "entry_id": runtime.context["tracing_path"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "type": type
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        data_graph = remove_class_core(data_graph, subject, type)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.remove_class.finish",
            payload={
                "entry_id": runtime.context["tracing_path"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "type": type
            }
        )
        
        return (data_graph, runtime.tool_call_id)
    
    def add_triple(self, runtime: _ToolRuntime, subject: str, relation: str, object: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.add_triple.start",
            payload={
                "entry_id": runtime.context["tracing_path"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "relation": relation,
                "object": object
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        data_graph = add_triple_core(data_graph, subject, relation, object)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.add_triple.finish",
            payload={
                "entry_id": runtime.context["tracing_path"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "relation": relation,
                "object": object
            }
        )
        
        return (data_graph, runtime.tool_call_id)
    
    def remove_triple(self, runtime: _ToolRuntime, subject: str, relation: str, object: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.remove_triple.start",
            payload={
                "entry_id": runtime.context["tracing_path"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "relation": relation,
                "object": object
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        data_graph = remove_triple_core(data_graph, subject, relation, object)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.remove_triple.start",
            payload={
                "entry_id": runtime.context["tracing_path"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "relation": relation,
                "object": object
            }
        )
        
        return (data_graph, runtime.tool_call_id)
        
    def validate_shacl(self, runtime: _ToolRuntime):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.validate_shacl.start",
            payload={
                "entry_id": runtime.context["tracing_path"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        report = pyshacl_validate(data_graph, runtime.context["ontology_graph"], runtime.context["shacl_graph"])
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.validate_shacl.finish",
            payload={
                "entry_id": runtime.context["tracing_path"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
            }
        )
        
        runtime.state["violation_report"] = report
        runtime.state["shacl_tool_call_id"] = runtime.tool_call_id
        
        if runtime.context["config"]["runtime"]["violation_translation"]:
            return violation_translation(runtime.state, runtime.context)
        else:
            return (
                format_violations(report,
                                  runtime.state["data_graph"],
                                  runtime.context["ontology_graph"],
                                  runtime.context["shacl_graph"]),
                report,
                runtime.tool_call_id
            )
            
        
    def finish(self, runtime: _ToolRuntime):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.finish.triggered",
            payload={
                "entry_id": runtime.context["tracing_path"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
            }
        )
        
        runtime.state["finish_tool_call_id"] = runtime.tool_call_id
        
        return check_entities_typed(runtime.state, runtime.context)
        