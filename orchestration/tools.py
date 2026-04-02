from pydantic import create_model, Field, BaseModel
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage
from langgraph.prebuilt import ToolNode
from typing import type, Literal, Callable
from rdflib import Graph

from models.data_models import Schema
from helpers import strip_ns


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
        for this ontology
        """
        RemoveTriple.__doc__ = """
        Use this tool to remove a triple from the data graph. Make sure the triple that you are about to remove actually exists.
        """
        
        self.tools = {
            "add_class": tool("AddClass", self.add_class, arg_schema=AddClass),
            "remove_class": tool("RemoveClass", self.remove_class, arg_schema=RemoveClass),
            "add_triple": tool("AddTriple", self.add_triple, args_schema=AddTriple),
            "remove_triple": tool("RemoveTriple", self.remove_triple, args_schema=RemoveTriple),
            "validate_shacl": tool("ValidateShacl", self.validate_shacl),
            "finish": tool("Finish", self.finish)
        }
        self.arg_schemas = {
            "AddClass": AddClass,
            "RemoveClass": RemoveClass,
            "AddTriple": AddTriple,
            "RemoveTriple": RemoveTriple
        }
        
        
    def build_tool_node(self):
        return ToolNode(
            tools=[func for (_, func) in self.tools.items()]
        )
        
    #TODO: add missing tools (validate_shacl, finish)

    def add_class(self, runtime: ToolRuntime, subject: str, type: str):
        subject = strip_ns(subject)
        type = strip_ns(type)
        self.arg_schemas["AddClass"].model_validate({
            "subject": subject,
            "type": type
        })
        
        data_graph: Graph = runtime.state["data_graph"]
        
        #TODO: use the logic from core
        ...
        
        return Command(
            update={
                "data_graph": data_graph,
                "messages": [
                    ToolMessage(
                        content=f"The updated data graph is:\n{data_graph.serialize(format="turtle")}",
                        tool_call_id=runtime.state["tool_call_id"]
                    )
                ]
            },
            goto="llm"
        )
    
    def remove_class(self, runtime: ToolRuntime, subject: str, type: str):
        subject = strip_ns(subject)
        type = strip_ns(type)
        self.arg_schemas["RemoveClass"].model_validate({
            "subject": subject,
            "type": type
        })
        
        data_graph: Graph = runtime.state["data_graph"]
        
        ...
        
        return Command(
            update={
                "data_graph": data_graph,
                "messages": [
                    ToolMessage(
                        content=f"The updated data graph is:\n{data_graph.serialize(format="turtle")}",
                        tool_call_id=runtime.state["tool_call_id"]
                    )
                ]
            },
            goto="llm"
        )
    
    def add_triple(self, runtime: ToolRuntime, subject: str, relation: str, object: str):
        subject = strip_ns(subject)
        relation = strip_ns(relation)
        object = strip_ns(object)
        self.arg_schemas["AddTriple"].model_validate({
            "subject": subject,
            "relation": relation,
            "object": object
        })
        
        data_graph: Graph = runtime.state["data_graph"]
        
        ...
        
        return Command(
            update={
                "data_graph": data_graph,
                "messages": [
                    ToolMessage(
                        content=f"The updated data graph is:\n{data_graph.serialize(format="turtle")}",
                        tool_call_id=runtime.state["tool_call_id"]
                    )
                ]
            },
            goto="llm"
        )
    
    def remove_triple(self, runtime: ToolRuntime, subject: str, relation: str, object: str):
        subject = strip_ns(subject)
        relation = strip_ns(relation)
        object = strip_ns(object)
        self.arg_schemas["RemoveTriple"].model_validate({
            "subject": subject,
            "relation": relation,
            "object": object
        })
        
        data_graph: Graph = runtime.state["data_graph"]
        
        ...
        
        return Command(
            update={
                "data_graph": data_graph,
                "messages": [
                    ToolMessage(
                        content=f"The updated data graph is:\n{data_graph.serialize(format="turtle")}",
                        tool_call_id=runtime.state["tool_call_id"]
                    )
                ]
            },
            goto="llm"
        )
        
    def validate_shacl(self, runtime: ToolRuntime):
        """
        Use this tool to validate that the current data graph adheres to the ontology.
        The validation is performed through SHACL, the shapes are pre-generated.
        The tool does not have any input arguments, the data graph is passed internally.
        """
        data_graph: Graph = runtime.state["data_graph"]
        
        ...
        
        return Command(
            update={
                "violation_report": ...,
                "shacl_tool_call_id": runtime.state["tool_call_id"]
            },
            goto="violation_translation" if runtime.context["config"]["runtime"]["violation_translation"] else "format_violations"
        )
        
    def finish(self, runtime: ToolRuntime):
        """
        Use this tool to finish the work. No input arguments required.
        """
        return Command(
            update={
                "to_end": True,
                "finish_tool_call_id": runtime.state["tool_call_id"]
            },
            goto="check_entities_typed"
        )
        