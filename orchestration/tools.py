import textwrap
from pydantic import create_model, Field, BaseModel
from langgraph.types import Command
from typing import Literal, Callable
from langchain.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from rdflib import Graph
from langgraph.runtime import Runtime
from langchain_core.messages.content import ToolCall
from langgraph.graph import END

from models.data_models import Schema, TaskState, TaskContext, ViolationTranslation, ToolRuntime_
from orchestration.tracing import append_trace
from core.data_graph_functions import assign_class as assign_class_core
from core.data_graph_functions import unassign_class as unassign_class_core
from core.data_graph_functions import add_triple as add_triple_core
from core.data_graph_functions import remove_triple as remove_triple_core
from core.data_graph_functions import add_literal as add_literal_core, GraphLiterals
from core.shacl_functions import pyshacl_validate, format_violations
from prompts.prompt_engine import get_prompt, format_prompt
from core.shacl_functions import format_violations
from core.data_graph_functions import check_ents_typed
from helpers import strip_ns, strip_uri


def create_translation_response_model(num_violations: int) -> BaseModel:
    TranslationOutput = create_model(
        "TranslationOutput",
        translations=(list[ViolationTranslation], Field(min_length=num_violations, max_length=num_violations))
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
        trans_user_prompt = format_prompt(
            trans_user_path,
            violations=format_violations(
                state["violation_report"],
                state["data_graph"],
                context["ontology_graph"],
                context["shacl_graph"]
            )
        )
        trans_user_msg = HumanMessage(content=trans_user_prompt)
        
        response_model = create_translation_response_model(len(state["violation_report"].violations))
        llm = context["llm"].with_structured_output(response_model, include_raw=True)
        response = llm.invoke([trans_system_msg, trans_user_msg])
        ai_msg = response["raw"]
        parsed = response["parsed"]
        translation_convo = [trans_system_msg, trans_user_msg, ai_msg]
        
        with open(f"{context["artifacts_dir"]}/{state["iterations"]}_iter_translation_convo.md", "w") as f:
            f.write(translation_convo)
        
        with open(f"{context["artifacts_dir"]}/{state["iterations"]}_iter_translation_metadata.md", "w") as f:
            f.write(ai_msg.usage_metadata)
        
        report = state["violation_report"].model_copy()
        for i, v in enumerate(report.violations):
            v.llm_explanation = parsed.translations[i].explanation
            v.llm_instruction = parsed.translations[i].instruction
            
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
        if not not_typed:
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


class ToolClass:
    tools: dict[str, Callable]
    arg_schemas: dict[str, BaseModel]
    Relation: type
    Class: type
    
    
    def __init__(self, schema: Schema):
        self.Relation = Literal[tuple([reldef.relation for reldef in schema.relations])]
        self.Type = Literal[tuple(schema.entities)]
        
        assign_class_defs = {
            "subject": (str, Field(description="A node in the data graph (if not exists yet, it is created)"+
                                                "to which you want to assign a class.")),
            "type": (self.Type, Field(description="A type (out of the list of allowed entity types) " + 
                                                    "that you want to assign to the subject node."))
        }
        unassign_class_defs = {
            "subject": (str, Field(description="A node in the data graph (if not exists yet, it is created) which class you want to remove.")),
            "type": (self.Type, Field(description="A type (out of the allowed entity types) " +
                                                    "that is assigned to the subject and should be removed"))
        }
        AssignClass = create_model("AssignClass", **assign_class_defs)
        AssignClass.__doc__ = """
        Use this tool to assign a class to a node. This is essentially AddTriple with relation being rdf:type
        and object being an allowed entity type. Note that it does not matter whether the subject node already
        exists (participates in any triples), the class assignment is anyway valid. Make sure that all nodes
        have classes assigned to them!
        """
        UnassignClass = create_model("UnassignClass", **unassign_class_defs)
        UnassignClass.__doc__ = """
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
        
        add_literal_defs = {
            "subject": (str, Field(description="A node in the data graph (if not exists yet, it is created) "
                                                +"to which you want to add a literal through a relation")),
            "relation": (self.Relation, Field(description="A relation (out of the allowed relations) " + 
                                                            "defined between the subject and the literal")),
            "literal_value": (str, Field(description="The value that the literal is going to bear")),
            "literal_type": (GraphLiterals, Field(description="The type of the literal out of the list of allowed literal types"))
        }
        AddLiteral = create_model("AddLiteral", **add_literal_defs)
        AddLiteral.__doc__ = """
        Use this tool to create a triple which object is going to be a literal value. This is essentially AddTriple
        but with the object being a literal and thus with full validation support. As previously, if the subject node
        does not exist yet, it is created. If there are problems with validating the literal_value, an error report
        will be returned.
        """
        
        #TODO: add RemoveLiteral
        
        self.tools_schemas = [AssignClass, UnassignClass, AddTriple, RemoveTriple, ValidateShacl, Finish, AddLiteral]
        self.tools = {
            "AssignClass": self.assign_class,
            "UnassignClass": self.unassign_class,
            "AddTriple": self.add_triple,
            "RemoveTriple": self.remove_triple,
            "ValidateShacl": self.validate_shacl,
            "Finish": self.finish,
            "AddLiteral": self.add_literal
        }
        self.data_graph_edit_tools = ["AssignClass", "UnassignClass", "AddTriple", "RemoveTriple"]
        
        
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
                    tool_runtime = ToolRuntime_(
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
                                content="The final data graph after the sequence of edits:" +
                                         f"\n\n{textwrap.indent(output[0].serialize(format="turtle"), '  ')}",
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


    def assign_class(self, runtime: ToolRuntime_, subject: str, type: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.assign_class.start",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "type": type
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        data_graph = assign_class_core(data_graph, subject, type)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.assign_class.finish",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "type": type
            }
        )
        
        return (data_graph, runtime.tool_call_id)
    
    
    def unassign_class(self, runtime: ToolRuntime_, subject: str, type: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.unassign_class.start",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "type": type
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        data_graph = unassign_class_core(data_graph, subject, type)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.unassign_class.finish",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "type": type
            }
        )
        
        return (data_graph, runtime.tool_call_id)
    
    
    def add_triple(self, runtime: ToolRuntime_, subject: str, relation: str, object: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.add_triple.start",
            payload={
                "entry_id": runtime.context["entry_id"],
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
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "relation": relation,
                "object": object
            }
        )
        
        return (data_graph, runtime.tool_call_id)
    
    
    def remove_triple(self, runtime: ToolRuntime_, subject: str, relation: str, object: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.remove_triple.start",
            payload={
                "entry_id": runtime.context["entry_id"],
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
            "run.entry.agent.tools.remove_triple.finish",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "relation": relation,
                "object": object
            }
        )
        
        return (data_graph, runtime.tool_call_id)
        
        
    def validate_shacl(self, runtime: ToolRuntime_):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.validate_shacl.start",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        conforms, report = pyshacl_validate(data_graph, runtime.context["ontology_graph"], runtime.context["shacl_graph"])
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.validate_shacl.finish",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "conforms": conforms,
                "tool_call_id": runtime.tool_call_id,
            }
        )
        
        runtime.state["violation_report"] = report
        runtime.state["shacl_tool_call_id"] = runtime.tool_call_id
        
        if conforms:
            return ("SHACL validation has not produced any violations.", runtime.tool_call_id)
        
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
            
        
    def finish(self, runtime: ToolRuntime_):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.finish.triggered",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
            }
        )
        
        runtime.state["finish_tool_call_id"] = runtime.tool_call_id
        
        return check_entities_typed(runtime.state, runtime.context)
        
        
    def add_literal(self, runtime: ToolRuntime_, subject: str, relation: str, literal_value: str, literal_type: GraphLiterals):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.add_literal.start",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "relation": relation,
                "literal_value": literal_value,
                "literal_type": literal_type.value
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        data_graph = add_literal_core(data_graph, subject, relation, literal_value, literal_type)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.add_literal.finish",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": subject,
                "relation": relation,
                "literal_value": literal_value,
                "literal_type": literal_type.value
            }
        )
        
        return (data_graph, runtime.tool_call_id)