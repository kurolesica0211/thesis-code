from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional, TypedDict

from models.data_models import BatchExtractionResult, CategoryBatch
from extractors.extractor import Extractor
from validators.shacl_validator import OntologyIndex


class ShaclBatchState(TypedDict, total=False):
    batch: CategoryBatch
    rdf_ontology_text: str
    shacl_shapes_ttl: str
    ontology_format: str
    max_rounds: int
    current_round: int
    prompt_caching_enabled: bool
    correction_template_path: str
    violation_translation_template_path: str
    shacl_log_file: Optional[str]
    batch_result: BatchExtractionResult
    report: Any
    shapes_graph: Any
    violations_by_entry: Dict[int, list]
    correction_plan: Dict[str, Any]
    translation_text: str
    corrected_data: Dict[str, Any]
    should_correct: bool
    done_reason: str
    trace_path: Optional[str]
    artifact_dir: Optional[str]
    ont_idx: OntologyIndex


def build_shacl_batch_graph(extractor: Extractor):
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as exc:
        raise ImportError(
            "LangGraph is required for SHACL graph orchestration. Install with 'pip install langgraph'."
        ) from exc

    def llm_extract_initial(state: ShaclBatchState) -> ShaclBatchState:
        from orchestration.tracing import append_trace

        batch = state["batch"]
        append_trace(
            state.get("trace_path"),
            "graph.node.llm_extract_initial.start",
            {"category": batch.category, "entries": len(batch.entries)},
        )
        result = extractor.extract_batch_rdf(
            batch.entries,
            state["rdf_ontology_text"],
            schema_def=batch.schema_def,
        )
        append_trace(
            state.get("trace_path"),
            "graph.node.llm_extract_initial.end",
            {"category": batch.category},
        )
        return {
            "batch_result": result,
            "current_round": 1,
        }

    def validate_shacl(state: ShaclBatchState) -> ShaclBatchState:
        from orchestration.tracing import append_trace
        from validators.shacl_validator import validate_batch

        append_trace(
            state.get("trace_path"),
            "graph.node.validate_shacl.start",
            {
                "round": state.get("current_round", 1),
                "category": state["batch"].category,
            },
        )
        report, shapes_graph, ont_idx, _ = validate_batch(
            state["batch_result"].results,
            state["rdf_ontology_text"],
            state["shacl_shapes_ttl"],
            ontology_format=state["ontology_format"],
        )

        if report.conforms:
            round_num = state.get("current_round", 1)
            if state.get("shacl_log_file"):
                from extractors.extractor import _log_round_conforms

                _log_round_conforms(state["shacl_log_file"], round_num)

            return {
                "report": report,
                "shapes_graph": shapes_graph,
                "violations_by_entry": {},
                "should_correct": False,
                "done_reason": "conforms",
            }

        violations_by_entry = report.group_violations_by_entry()
        current_round = state.get("current_round", 1)
        max_rounds = state.get("max_rounds", 1)
        should_correct = current_round <= max_rounds

        next_state = {
            "report": report,
            "shapes_graph": shapes_graph,
            "ont_idx": ont_idx,
            "violations_by_entry": violations_by_entry,
            "should_correct": should_correct,
            "done_reason": "needs_correction" if should_correct else "max_rounds_reached",
        }
        append_trace(
            state.get("trace_path"),
            "graph.node.validate_shacl.end",
            {
                "round": current_round,
                "conforms": report.conforms,
                "violations": len(report.violations),
                "should_correct": should_correct,
            },
        )
        return next_state

    def prepare_correction_round(state: ShaclBatchState) -> ShaclBatchState:
        from orchestration.tracing import append_trace

        batch = state["batch"]
        round_num = state.get("current_round", 1)
        append_trace(
            state.get("trace_path"),
            "graph.node.prepare_correction_round.start",
            {
                "round": round_num,
                "category": batch.category,
            },
        )
        plan = extractor.prepare_shacl_correction_round(
            entries=batch.entries,
            current_result=state["batch_result"],
            rdf_ontology_text=state["rdf_ontology_text"],
            ont_idx=state["ont_idx"],
            violations_by_entry=state["violations_by_entry"],
            shapes_graph=state["shapes_graph"],
            round_num=round_num,
            correction_template_path=state.get("correction_template_path", "prompts/two_step_correction/correction.md"),
            violation_translation_template_path=state.get(
                "violation_translation_template_path",
                "prompts/two_step_correction/violation_translation.md",
            ),
            schema_def=batch.schema_def,
            artifact_dir=state.get("artifact_dir"),
        )
        append_trace(
            state.get("trace_path"),
            "graph.node.prepare_correction_round.end",
            {
                "round": round_num,
                "category": batch.category,
            },
        )

        artifact_dir = state.get("artifact_dir") or "results"
        os.makedirs(artifact_dir, exist_ok=True)

        # Restore markdown dumps for both LLM prompts used in the correction phase.
        with open(
            os.path.join(artifact_dir, f"shacl_round_{round_num}_translation_prompt.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(plan["translation_prompt"])

        with open(
            os.path.join(artifact_dir, f"shacl_round_{round_num}_correction_prompt.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(plan["correction_prompt"])

        return {
            "correction_plan": plan,
        }

    def llm_violation_translation(state: ShaclBatchState) -> ShaclBatchState:
        from orchestration.tracing import append_trace

        plan = state["correction_plan"]
        round_num = state.get("current_round", 1)
        append_trace(
            state.get("trace_path"),
            "graph.node.llm_violation_translation.start",
            {"round": round_num, "category": state["batch"].category},
        )
        translation_text = extractor.llm_translate_violations(
            plan["translation_prompt"],
            use_prompt_caching=state.get("prompt_caching_enabled", True),
        )
        append_trace(
            state.get("trace_path"),
            "graph.node.llm_violation_translation.end",
            {"round": round_num, "category": state["batch"].category},
        )

        artifact_dir = state.get("artifact_dir") or "results"
        os.makedirs(artifact_dir, exist_ok=True)
        with open(
            os.path.join(artifact_dir, f"shacl_round_{round_num}_translation_response.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(translation_text)

        return {"translation_text": translation_text}

    def llm_correction(state: ShaclBatchState) -> ShaclBatchState:
        from orchestration.tracing import append_trace

        plan = state["correction_plan"]
        round_num = state.get("current_round", 1)
        append_trace(
            state.get("trace_path"),
            "graph.node.llm_correction.start",
            {"round": round_num, "category": state["batch"].category},
        )
        corrected_data = extractor.llm_correct_from_translation(
            translation_prompt=plan["translation_prompt"],
            translation_text=state["translation_text"],
            correction_prompt=plan["correction_prompt"],
            response_model=plan["response_model"],
            use_prompt_caching=state.get("prompt_caching_enabled", True),
        )

        conversation_artifact = {
            "model": extractor.model_name,
            "round": round_num,
            "anthropic_prompt_caching": state.get("prompt_caching_enabled", True),
            "messages": [
                {"role": "user", "name": "violation_translation", "content": plan["translation_prompt"]},
                {"role": "assistant", "name": "violation_translation_response", "content": state["translation_text"]},
                {"role": "user", "name": "correction_request", "content": plan["correction_prompt"]},
                {"role": "assistant", "name": "correction_response", "content": corrected_data},
            ],
        }
        
        artifact_dir = state.get("artifact_dir") or "results"
        os.makedirs(artifact_dir, exist_ok=True)

        with open(
            os.path.join(artifact_dir, f"shacl_round_{round_num}_correction_response.json"),
            "w",
            encoding="utf-8",
        ) as f:
            import json
            
            f.write(json.dumps(corrected_data, ensure_ascii=False, indent=2))

        with open(
            f"{artifact_dir}/shacl_round_{round_num}_conversation.json",
            "w",
            encoding="utf-8",
        ) as f:
            import json

            json.dump(conversation_artifact, f, ensure_ascii=False, indent=2)

        append_trace(
            state.get("trace_path"),
            "graph.node.llm_correction.end",
            {"round": round_num, "category": state["batch"].category},
        )
        return {"corrected_data": corrected_data}

    def merge_correction(state: ShaclBatchState) -> ShaclBatchState:
        from orchestration.tracing import append_trace

        round_num = state.get("current_round", 1)
        append_trace(
            state.get("trace_path"),
            "graph.node.merge_correction.start",
            {"round": round_num, "category": state["batch"].category},
        )
        merged = extractor.merge_shacl_corrections(
            entries=state["batch"].entries,
            current_result=state["batch_result"],
            violations_by_entry=state["violations_by_entry"],
            corrected_data=state["corrected_data"],
            round_num=round_num,
            shacl_log_file=state.get("shacl_log_file"),
        )
        append_trace(
            state.get("trace_path"),
            "graph.node.merge_correction.end",
            {"round": round_num, "category": state["batch"].category},
        )
        return {
            "batch_result": merged,
            "current_round": round_num + 1,
        }

    def route_after_validate(state: ShaclBatchState) -> str:
        from orchestration.tracing import append_trace

        route = "prepare_correction_round" if state.get("should_correct", False) else "finish"
        append_trace(
            state.get("trace_path"),
            "graph.route.after_validate",
            {
                "route": route,
                "done_reason": state.get("done_reason"),
            },
        )
        return route

    graph = StateGraph(ShaclBatchState)
    graph.add_node("llm_extract_initial", llm_extract_initial)
    graph.add_node("validate_shacl", validate_shacl)
    graph.add_node("prepare_correction_round", prepare_correction_round)
    graph.add_node("llm_violation_translation", llm_violation_translation)
    graph.add_node("llm_correction", llm_correction)
    graph.add_node("merge_correction", merge_correction)

    graph.add_edge(START, "llm_extract_initial")
    graph.add_edge("llm_extract_initial", "validate_shacl")
    graph.add_conditional_edges(
        "validate_shacl",
        route_after_validate,
        {
            "prepare_correction_round": "prepare_correction_round",
            "finish": END,
        },
    )
    graph.add_edge("prepare_correction_round", "llm_violation_translation")
    graph.add_edge("llm_violation_translation", "llm_correction")
    graph.add_edge("llm_correction", "merge_correction")
    graph.add_edge("merge_correction", "validate_shacl")

    return graph.compile()
