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
from orchestration.tracing import append_trace, append_usage_metadata, append_graph_snapshot
from core.data_graph_functions import (
    assign_class as assign_class_core,
    unassign_class as unassign_class_core,
    add_triple as add_triple_core,
    remove_triple as remove_triple_core,
    add_literal as add_literal_core,
    remove_literal as remove_literal_core,
    GraphLiterals,
    check_ents_typed
)
from core.shacl_functions import pyshacl_validate, format_violations
from prompts.prompt_engine import get_prompt, format_prompt
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
        
        llm = context["translation_llm"].with_structured_output(response_model, include_raw=True)
        response = llm.invoke([trans_system_msg, trans_user_msg])
        ai_msg = response["raw"]
        parsed = response["parsed"]
        translation_convo = [trans_system_msg, trans_user_msg, ai_msg]
        final_translation_convo = "\n\n".join([msg.pretty_repr() for msg in translation_convo])

        convos_dir = f"{context['artifacts_dir']}/convos"
        with open(f"{convos_dir}/{state['iterations']}_iter_translation_convo.md", "w", encoding="utf-8") as f:
            f.write(final_translation_convo)

        append_usage_metadata(
            context["artifacts_dir"],
            "translation",
            {
                "iteration": state["iterations"],
                "shacl_tool_call_id": state["shacl_tool_call_id"],
                "metadata": ai_msg.usage_metadata,
            },
        )
        
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
            

def check_min_iterations_reached(state: TaskState, context: TaskContext):
    append_trace(context["tracing_path"], "run.event.agent.check_iterations_reached.start", payload={
            "entry_id": context["entry_id"]
        })
    
    if state["iterations"] < context["config"]["runtime"]["min_iterations"]:
        append_trace(context["tracing_path"], "run.event.agent.check_iterations_reached.reached", payload={
            "entry_id": context["entry_id"]
        })
        return (
            "You finished earlier than is required, you may double-check your work. If you are sure that you have finished, just continue using the Finish tool.",
            state["finish_tool_call_id"]
        )
    else:
        return END


class ToolClass:
    tools: dict[str, Callable]
    arg_schemas: dict[str, BaseModel]
    Relation: type
    Class: type
    
    
    def __init__(self, schema: Schema, data_graph: Graph, shacl_validation: bool = True):
        self.Relation = Literal[tuple([reldef.relation for reldef in schema.relations])]
        self.Type = Literal[tuple(schema.entities)]
        
        assign_class_defs = {
            "source": (str, Field(description="A node in the data graph (if not exists yet, it is created)"+
                                                "to which you want to assign a class.")),
            "type": (self.Type, Field(description="A type (out of the list of allowed entity types) " + 
                                                    "that you want to assign to the source node."))
        }
        unassign_class_defs = {
            "source": (str, Field(description="A node in the data graph (if not exists yet, it is created) which class you want to remove.")),
            "type": (self.Type, Field(description="A type (out of the allowed entity types) " +
                                                    "that is assigned to the source and should be removed"))
        }
        AssignClass = create_model("AssignClass", **assign_class_defs)
        AssignClass.__doc__ = """
        Use this tool to assign a class to a node. This is essentially AddTriple with relation being rdf:type
        and target being an allowed entity type. Note that it does not matter whether the source node already
        exists (participates in any triples), the class assignment is anyway valid. Make sure that all nodes
        have classes assigned to them!
        """
        UnassignClass = create_model("UnassignClass", **unassign_class_defs)
        UnassignClass.__doc__ = """
        Use this tool to remove a class assigned to a node. This is essentially RemoveTriple with relation
        being rdf:type and target being an allowed entity type. Make sure that the source node actually
        has that class assigned to it which you want to remove! And also make sure that all nodes have
        classes assigned to them!
        """
        
        add_triple_defs = {
            "source": (str, Field(description="A source node of the triple.")),
            "relation": (self.Relation, Field(description="A relation (out of the allowed relations) " + 
                                                            "defined between the source and target of this triple")),
            "target": (str, Field(description="A target node of the triple."))
        }
        remove_triple_defs = {
            "source": (str, Field(description="An existing source node of the triple to be removed.")),
            "relation": (self.Relation, Field(description="A relation (out of the allowed relations) defined " + 
                                                            "between the source and target of the triple to be removed")),
            "target": (str, Field(description="An existing target node of the triple to be removed"))
        }
        AddTriple = create_model("AddTriple", **add_triple_defs)
        RemoveTriple = create_model("RemoveTriple", **remove_triple_defs)
        AddTriple.__doc__ = """
        Use this tool to add a triple to the data graph. Make sure the relation comes from the list of allowed relations
        for this ontology. The triple should be specified as `source`, `relation`, `target`.
        """
        RemoveTriple.__doc__ = """
        Use this tool to remove a triple from the data graph. Make sure the triple that you are about to remove actually exists.
        Specify it as `source`, `relation`, `target`.
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
        
        literals = [uri.value.n3(data_graph.namespace_manager) for uri in GraphLiterals]
        self.LiteralsType = Literal[tuple(literals)]
        
        add_literal_defs = {
            "source": (str, Field(description="A node in the data graph (if not exists yet, it is created) "
                                                +"to which you want to add a literal through a relation")),
            "relation": (self.Relation, Field(description="A relation (out of the allowed relations) " + 
                                                            "defined between the source and the literal")),
            "literal_value": (str, Field(description="The value that the literal is going to bear")),
            "literal_type": (self.LiteralsType, Field(description="The type of the literal out of the list of allowed literal types"))
        }
        AddLiteral = create_model("AddLiteral", **add_literal_defs)
        AddLiteral.__doc__ = """
        Use (only) this tool to create a triple whose target is going to be a literal value. This is essentially AddTriple
        but with the target being a literal and thus with full validation support. As previously, if the source node
        does not exist yet, it is created. If there are problems with validating the literal_value, an error report
        will be returned.
        """
        
        remove_literal_defs = {
            "source": (str, Field(description="An existing node in the data graph "
                                                +"from which you want to remove a relation ending with a literal")),
            "relation": (self.Relation, Field(description="The relation " + 
                                                            "defined between the source and the literal")),
            "literal_value": (str, Field(description="The value of the literal")),
            "literal_type": (self.LiteralsType, Field(description="The datatype of the defined literal out of the list of allowed types."))
        }
        RemoveLiteral = create_model("RemoveLiteral", **remove_literal_defs)
        RemoveLiteral.__doc__ = """
        Use (only) this tool to remove a triple which has a literal as the target. This is essentially RemoveTriple but with
        the correct handling of literals. To correctly specify the literal target of the triple, you need to provide
        both the value and datatype, both of which can be identified from the literal. 
        For example, literal '2026-04-08'^^xsd:date has type 'date' and value '2026-04-08'.
        'Hello World'^^xsd:string has type 'string' and value 'Hello World.'
        """
        
        
        self.tools_schemas = [AssignClass, UnassignClass, AddTriple, RemoveTriple, Finish, AddLiteral, RemoveLiteral]
        self.tools = {
            "AssignClass": self.assign_class,
            "UnassignClass": self.unassign_class,
            "AddTriple": self.add_triple,
            "RemoveTriple": self.remove_triple,
            "Finish": self.finish,
            "AddLiteral": self.add_literal,
            "RemoveLiteral": self.remove_literal
        }
        
        if shacl_validation == True:
            self.tools_schemas.append(ValidateShacl)
            self.tools["ValidateShacl"] = self.validate_shacl
        
        self.data_graph_edit_tools = ["AssignClass", "UnassignClass", "AddTriple", "RemoveTriple", "AddLiteral", "RemoveLiteral"]
        self.literal_edit_tools = ["AddLiteral", "RemoveLiteral"]
        
        
    def build_tool_node(self):
        
        def execute_tool_calls(state: TaskState, runtime: Runtime[TaskContext]):
            append_trace(runtime.context["tracing_path"], "run.entry.agent.tools.start", payload={
                "entry_id": runtime.context["entry_id"]
            })
            
            last_msg = state["messages"][-1]
            if type(last_msg) is AIMessage:
                last_msg: AIMessage
                tool_calls: list[ToolCall] = last_msg.tool_calls
                call_results = []
                has_pending_data_graph_snapshot = False
                for call in tool_calls:
                    tool_runtime = ToolRuntime_(
                        state=state,
                        context=runtime.context,
                        tool_call_id=call["id"]
                    )
                    output = self.tools[call["name"]](tool_runtime, **call["args"])
                    if call["name"] in self.data_graph_edit_tools:
                        state["data_graph"] = output[0]
                        has_pending_data_graph_snapshot = True
                    elif call["name"] == "ValidateShacl":
                        if has_pending_data_graph_snapshot:
                            append_graph_snapshot(
                                runtime.context["artifacts_dir"],
                                "data_graph",
                                state["data_graph"].serialize(format="turtle"),
                                state["iterations"],
                                "pre_validation",
                                call["id"],
                            )
                            has_pending_data_graph_snapshot = False

                        state["violation_report"] = output[1]
                        
                        if len(output) > 3 and output[2]:
                            append_graph_snapshot(
                                runtime.context["artifacts_dir"],
                                "validation_graph",
                                output[2].serialize(format="turtle"),
                                state["iterations"],
                                "validate_shacl",
                                call["id"],
                            )
                    call_results.append((output, call["name"]))

                if has_pending_data_graph_snapshot:
                    append_graph_snapshot(
                        runtime.context["artifacts_dir"],
                        "data_graph",
                        state["data_graph"].serialize(format="turtle"),
                        state["iterations"],
                        "post_edits",
                    )
                
                append_trace(runtime.context["tracing_path"], "run.entry.agent.tools.executed_tools", payload={
                    "entry_id": runtime.context["entry_id"]
                })
                
                messages = []
                last_edit = -1
                for i, (_, name) in enumerate(reversed(call_results)):
                    if name in self.data_graph_edit_tools:
                        last_edit = len(call_results) - i - 1
                        break
                
                for i, (output, name) in enumerate(call_results):
                    content = []
                    
                    if name in self.data_graph_edit_tools:
                        error = False
                        err_msg = []
                        
                        if name in self.literal_edit_tools and output[1] is not None:
                            error = True
                            err_msg.append(f"Literal value validation error: {output[1]}")
                        
                        if error:
                            content.append("Note that this edit to the data graph was not applied "+
                                                                                     f"due to the following errors:\n{textwrap.indent(chr(10).join(err_msg), '  ')}")
                        
                        if i == last_edit:
                            content.append("The final data graph after all the edits:" +
                                                                                 f"\n{textwrap.indent(output[0].serialize(format='turtle'), '  ')}")
                        else:
                            content.append("Look at the messages below to see the final data graph after all the edits.")
                            
                    elif name == "ValidateShacl":
                        content.append(output[0])
                        
                    elif name == "Finish":
                        if type(output) is not tuple and output == END:
                            append_trace(runtime.context["tracing_path"], "run.entry.agent.tools.finish!", payload={
                                "entry_id": runtime.context["entry_id"]
                            })
                            return Command(goto=END)
                        else:
                            content.append(output[0])
                
                    msg_str = "\n\n".join(content)
                    messages.append(ToolMessage(
                        content=msg_str,
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


    def assign_class(self, runtime: ToolRuntime_, source: str, type: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.assign_class.start",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": source,
                "type": type
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        data_graph = assign_class_core(data_graph, source, type)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.assign_class.finish",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": source,
                "type": type
            }
        )
        
        return (data_graph, runtime.tool_call_id)
    
    
    def unassign_class(self, runtime: ToolRuntime_, source: str, type: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.unassign_class.start",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": source,
                "type": type
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        data_graph = unassign_class_core(data_graph, source, type)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.unassign_class.finish",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": source,
                "type": type
            }
        )
        
        return (data_graph, runtime.tool_call_id)
    
    
    def add_triple(self, runtime: ToolRuntime_, source: str, relation: str, target: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.add_triple.start",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": source,
                "relation": relation,
                "object": target
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        data_graph = add_triple_core(data_graph, source, relation, target)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.add_triple.finish",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": source,
                "relation": relation,
                "object": target
            }
        )
        
        return (data_graph, runtime.tool_call_id)
    
    
    def remove_triple(self, runtime: ToolRuntime_, source: str, relation: str, target: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.remove_triple.start",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": source,
                "relation": relation,
                "object": target
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        data_graph = remove_triple_core(data_graph, source, relation, target)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.remove_triple.finish",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": source,
                "relation": relation,
                "object": target
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

        conforms, report, graph = pyshacl_validate(data_graph, runtime.context["ontology_graph"], runtime.context["shacl_graph"])
        
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
            return ("SHACL validation has not produced any violations.", report, graph, runtime.tool_call_id)
        
        if runtime.context["config"]["runtime"]["violation_translation"]:
            msg, report, tool_id = violation_translation(runtime.state, runtime.context)
            return (msg, report, graph, tool_id)
        else:
            return (
                format_violations(report,
                                  runtime.state["data_graph"],
                                  runtime.context["ontology_graph"],
                                  runtime.context["shacl_graph"]),
                report,
                graph,
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
        
        check_one = check_entities_typed(runtime.state, runtime.context)
        if check_one == END:
            return check_min_iterations_reached(runtime.state, runtime.context)
        else:
            return check_one
        
        
    def add_literal(self, runtime: ToolRuntime_, source: str, relation: str, literal_value: str, literal_type: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.add_literal.start",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": source,
                "relation": relation,
                "literal_value": literal_value,
                "literal_type": literal_type
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        parsed, data_graph, err_msg = add_literal_core(data_graph, source, relation, literal_value, literal_type)
        if not parsed:
            append_trace(
                runtime.context["tracing_path"],
                "run.entry.agent.tools.add_literal.parsing_error",
                payload={
                    "entry_id": runtime.context["entry_id"],
                    "iterations": runtime.state["iterations"],
                    "tool_call_id": runtime.tool_call_id,
                    "subject": source,
                    "relation": relation,
                    "literal_value": literal_value,
                    "literal_type": literal_type,
                    "err_msg": err_msg
                }
            )
            
            return (data_graph, err_msg, runtime.tool_call_id)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.add_literal.finish",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": source,
                "relation": relation,
                "literal_value": literal_value,
                "literal_type": literal_type
            }
        )
        
        return (data_graph, None, runtime.tool_call_id)
    
    
    def remove_literal(self, runtime: ToolRuntime_, source: str, relation: str, literal_value: str, literal_type: str):
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.remove_literal.start",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": source,
                "relation": relation,
                "literal_value": literal_value,
                "literal_type": literal_type
            }
        )
        
        data_graph: Graph = runtime.state["data_graph"]
        
        parsed, data_graph, err_msg = remove_literal_core(data_graph, source, relation, literal_value, literal_type)
        if not parsed:
            append_trace(
                runtime.context["tracing_path"],
                "run.entry.agent.tools.remove_literal.parsing_error",
                payload={
                    "entry_id": runtime.context["entry_id"],
                    "iterations": runtime.state["iterations"],
                    "tool_call_id": runtime.tool_call_id,
                    "subject": source,
                    "relation": relation,
                    "literal_value": literal_value,
                    "literal_type": literal_type,
                    "err_msg": err_msg
                }
            )
            
            return (data_graph, err_msg, runtime.tool_call_id)
        
        append_trace(
            runtime.context["tracing_path"],
            "run.entry.agent.tools.remove_literal.finish",
            payload={
                "entry_id": runtime.context["entry_id"],
                "iterations": runtime.state["iterations"],
                "tool_call_id": runtime.tool_call_id,
                "subject": source,
                "relation": relation,
                "literal_value": literal_value,
                "literal_type": literal_type
            }
        )
        
        return (data_graph, None, runtime.tool_call_id)