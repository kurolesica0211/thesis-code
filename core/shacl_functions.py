from rdflib import Graph, SH, RDF, URIRef
from pyshacl import validate as py_validate
import re
import textwrap

from models.data_models import Violation, ValidationReport
from helpers import strip_uri, strip_ns
from core.data_graph_functions import extract_classes


def pyshacl_validate(data_graph: Graph, ont_graph: Graph, shacl_graph: Graph, debug: bool = False) -> tuple[bool, ValidationReport]:
    conforms, results_graph, _ = py_validate(
        data_graph=data_graph + shacl_graph,
        shacl_graph=shacl_graph,
        #ont_graph=ont_graph,
        advanced=True,
        abort_on_first=False,
        debug=debug
    )
    
    report = ValidationReport(conforms=conforms)
    
    if not conforms:
        report.violations = parse_results_graph(results_graph)
    
    return conforms, report, results_graph
    
    
def parse_results_graph(results_graph: Graph) -> list[Violation]:
    violations = []
    for result_node in results_graph.subjects(RDF.type, SH.ValidationResult):
        severity = results_graph.value(result_node, SH.resultSeverity)
        focus = results_graph.value(result_node, SH.focusNode)
        path = results_graph.value(result_node, SH.resultPath)
        value = results_graph.value(result_node, SH.value)
        source = results_graph.value(result_node, SH.sourceConstraintComponent)
        source_shape = results_graph.value(result_node, SH.sourceShape)
        message = results_graph.value(result_node, SH.resultMessage)
        
        violations.append(Violation(
            severity=strip_ns(strip_uri(str(severity))),
            focus=focus,
            path=path,
            value=value,
            constraint=strip_ns(strip_uri(str(source))),
            source_shape=source_shape,
            message=str(message)
        ))
    
    return violations


def serialize_shape(graph: Graph, shape_uri: URIRef) -> str:
    mini_graph = graph.cbd(shape_uri)
    for prefix, namespace in graph.namespaces():
        mini_graph.bind(prefix, namespace)
    serialized_cleaned = re.sub(r'@prefix.*\n|@base.*\n', '', mini_graph.serialize(format="turtle")).strip()
    return serialized_cleaned


def format_violations(report: ValidationReport, data_graph: Graph, ont_graph: Graph, shacl_graph: Graph) -> str:
    text = ""
    text += "VALIDATION RESULTS\n"
    text += f"Total violations:{len(report.violations)}\n"
    text += "Violations:\n\n"
    
    for (i, v) in enumerate(report.violations, start=1):
        text += f"  Violation [{i}]:\n"
        text += f"    Severity: {v.severity}\n"
        text += f"    Focus node: {strip_uri(strip_ns(str(v.focus)))}\n"
        text += f"    Path: {strip_uri(strip_ns(str(v.path)))}\n"
        text += f"    Value: {strip_uri(strip_ns(str(v.value)))}\n"
        text += f"    Constraint: {v.constraint}\n"
        text += f"    Source shape:\n{textwrap.indent(serialize_shape(shacl_graph, v.source_shape), '      ')}\n"
        text += f"    SHACL message: {v.message}\n"
        text += "\n"
        
        focus_cls_uris = extract_classes(data_graph, v.focus)
        text += f"    Classes assigned to the focus node: {[cls.n3(ont_graph.namespace_manager) for cls in focus_cls_uris]}\n"
        text += f"    Definitions of the classes assigned to the focus node:\n"
        for cls in focus_cls_uris:
            text += f"      Class {cls.n3(ont_graph.namespace_manager)}:\n{textwrap.indent(serialize_shape(ont_graph, cls), '        ')}\n"
        text += "\n"
            
        if v.path is not None:
            text += f"    Definition of the path:\n{textwrap.indent(serialize_shape(ont_graph, v.path), '      ')}"
            text += "\n"
        
        if v.value is not None:
            value_cls_uris = extract_classes(data_graph, v.value)
            text += f"    Classes assigned to the value node: {[cls.n3(ont_graph.namespace_manager) for cls in value_cls_uris]}\n"
            text += f"    Definitions of the classes assigned to the value node:\n"
            for cls in focus_cls_uris:
                text += f"      Class {cls.n3(ont_graph.namespace_manager)}:\n{textwrap.indent(serialize_shape(ont_graph, cls), '        ')}\n"
        text += "\n"
                
        if v.llm_explanation is not None and v.llm_instruction is not None:
            text += f"    LLM-provided explanation of the violation:\n{textwrap.indent(v.llm_explanation, '      ')}\n"
            text += f"    LLM-provided instruction on how to handle the violation:\n{textwrap.indent(v.llm_instruction, '      ')}"
        text += "\n\n\n"
        
    return text