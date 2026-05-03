import os
import json
import asyncio
from copy import deepcopy
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import init_chat_model
from rdflib import Graph

from configs.run_config import RunConfig
from loaders.base_family_loader import get_loader as base_family_get_loader
from loaders.look_up_family_loader import get_loader as look_up_family_get_loader
from orchestration.tools import ToolClass
from orchestration.tracing import (
    append_trace,
    init_artifact_files,
    append_usage_metadata,
    append_graph_snapshot,
)
from orchestration.agent import build_agent, TaskState, TaskContext
from prompts.prompt_engine import get_prompt, format_prompt
from models.data_models import TaskEntry


def _build_loader(config: RunConfig):
    if config.dataset.source == "custom_family_bench":
        loader = look_up_family_get_loader()
    return loader


def _compute_run_dir(config: RunConfig) -> str:
    if config.output.run_dir:
        return config.output.run_dir
    
    custom_tag = config.output.custom_tag
    safe_model = config.model.name.replace("/", "_").replace(":", "_")
    return os.path.join(config.output.base_dir, f"{custom_tag}_{safe_model}")


def _process_task_entry(
    task_entry: TaskEntry,
    task_idx: int,
    run_dir: str,
    main_system_msg: SystemMessage,
    main_user_prompt_path: str,
    config: RunConfig,
    trace_path: str,
    use_shacl: bool,
) -> Tuple[str, str, Graph]:
    """
    Process a single task entry synchronously.
    Returns: (task_dir, done_reason, delta_graph)
    """
    task_dir = os.path.join(run_dir, task_entry.entry_id)
    os.makedirs(task_dir, exist_ok=True)
    artifacts_dir = os.path.join(task_dir, "artifacts")
    init_artifact_files(artifacts_dir)
    
    # Store initial data graph for delta calculation
    init_data_graph = deepcopy(task_entry.data_graph)
    
    task_manifest_path = os.path.join(task_dir, "task_manifest.json")
    results_path = os.path.join(task_dir, "final_data_graph.ttl")
    task_manifest = {
        "entry_id": task_entry.entry_id,
        "done_reason": "",
        "artifacts_dir": artifacts_dir,
        "results": results_path,
        "iterations": 0
    }
    
    append_trace(trace_path, "run.entry.start", payload={
        "entry_idx": task_entry.entry_id
    })
    
    tool_obj = ToolClass(task_entry.schema_def, task_entry.data_graph, use_shacl)
    agent = build_agent(tool_obj)
    
    main_user_prompt = format_prompt(
        main_user_prompt_path,
        data_graph=task_entry.data_graph.serialize(format="turtle"),
        ontology=task_entry.ontology_graph.serialize(format="turtle"),
        input_text=task_entry.input_text
    )
    main_user_msg = HumanMessage(main_user_prompt)
    
    main_llm = init_chat_model(
        model=config.model.name,
        temperature=config.model.temperature,
        max_retries=config.model.max_retries
    )
    main_llm = main_llm.bind_tools(tool_obj.tools_schemas, tool_choice="any")
    translation_llm = init_chat_model(
        model=config.model.name,
        temperature=config.model.temperature,
        max_retries=config.model.max_retries
    )
    
    append_trace(trace_path, "run.entry.agent.invoke", payload={
        "entry_id": task_entry.entry_id,
    })
    
    final_state = agent.invoke(
        input=TaskState(
            messages=[main_system_msg, main_user_msg],
            data_graph=task_entry.data_graph,
            iterations=0,
            task_manifest=task_manifest
        ),
        context=TaskContext(
            main_llm=main_llm,
            translation_llm=translation_llm,
            entry_id=task_entry.entry_id,
            input_text=task_entry.input_text,
            ontology_graph=task_entry.ontology_graph,
            shacl_graph=task_entry.shacl_graph,
            tracing_path=trace_path,
            config=config.model_dump(),
            artifacts_dir=artifacts_dir
        )
    )
    
    task_manifest["done_reason"] = (
        final_state["task_manifest"]["done_reason"] 
        if final_state["task_manifest"]["done_reason"] != ""
        else "llm_finished"
    )
    task_manifest["iterations"] = final_state["iterations"]
    
    append_trace(trace_path, "run.entry.finish", payload={
        "entry_idx": task_entry.entry_id,
        "done_reason": task_manifest["done_reason"]
    })
    
    # Save results
    final_state["data_graph"].serialize(format="turtle", destination=results_path)
    
    # Calculate delta graph
    delta_graph: Graph = (final_state["data_graph"] - init_data_graph)
    delta_graph.namespace_manager = final_state["data_graph"].namespace_manager
    delta_graph_path = os.path.join(task_dir, "delta_graph.ttl")
    delta_graph.serialize(format="turtle", destination=delta_graph_path)

    append_graph_snapshot(
        artifacts_dir,
        "data_graph",
        final_state["data_graph"].serialize(format="turtle"),
        final_state["iterations"],
        "final_data_graph",
    )
    
    # Save conversation
    final_convo = "\n\n".join([msg.pretty_repr() for msg in final_state["messages"]])
    with open(f"{artifacts_dir}/convos/final_convo.md", "w", encoding="utf-8") as f:
        f.write(final_convo)
    
    # Save usage metadata
    usage_metadata = [msg.usage_metadata for msg in final_state["messages"] if type(msg) is AIMessage]
    append_usage_metadata(
        artifacts_dir,
        "final",
        {
            "iteration": final_state["iterations"],
            "metadata": usage_metadata,
        },
    )
    
    # Save task manifest
    with open(task_manifest_path, "w", encoding="utf-8") as f:
        json.dump(task_manifest, f, indent=4)
    
    return task_dir, task_manifest["done_reason"], delta_graph


async def run_async(config: RunConfig):
    """
    Async version of the runner that processes tasks concurrently.
    - Processes 10 tasks in parallel
    - Each task gets a fresh data graph (no reuse)
    - Collects and merges all delta graphs
    - Saves the merged delta graph to run directory
    """
    run_dir = _compute_run_dir(config)
    os.makedirs(run_dir, exist_ok=True)
    trace_path = os.path.join(run_dir, "trace.jsonl")
    append_trace(trace_path, "async_run.start")
    
    loader = _build_loader(config)
    append_trace(trace_path, "async_run.loader_instantiated")
    
    run_manifest = {
        "run_dir": run_dir,
        "config": config.model_dump(),
        "task_manifests": [],
        "trace": trace_path,
        "mode": "async",
    }
    
    main_system_prompt_path = (
        config.prompts.main_system 
        if config.runtime.shacl_validation 
        else config.prompts.main_system_without_shacl
    )
    main_user_prompt_path = config.prompts.main_user
    main_system_prompt = get_prompt(main_system_prompt_path)
    main_system_msg = SystemMessage(main_system_prompt)
    
    # Load all task entries
    all_tasks = list(loader.load())
    total_tasks = len(all_tasks)
    append_trace(trace_path, "async_run.tasks_loaded", payload={"total": total_tasks})
    
    # Process tasks concurrently with a maximum of 10 workers
    max_workers = 5
    delta_graphs: List[Graph] = []
    loop = asyncio.get_event_loop()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create tasks for all entries
        futures = []
        for idx, task_entry in enumerate(tqdm(all_tasks, desc="Submitting tasks", unit="task")):
            future = loop.run_in_executor(
                executor,
                _process_task_entry,
                task_entry,
                idx,
                run_dir,
                main_system_msg,
                main_user_prompt_path,
                config,
                trace_path,
                config.runtime.shacl_validation,
            )
            futures.append(future)
        
        # Gather all results with progress tracking
        pbar = tqdm(total=len(futures), desc="Processing tasks", unit="task")
        try:
            for future in asyncio.as_completed(futures):
                task_dir, done_reason, delta_graph = await future
                task_manifest_path = os.path.join(task_dir, "task_manifest.json")
                run_manifest["task_manifests"].append(task_manifest_path)
                delta_graphs.append(delta_graph)
                pbar.update(1)
        finally:
            pbar.close()
    
    # Merge all delta graphs
    if delta_graphs:
        merged_delta_graph = delta_graphs[0]
        for delta_graph in delta_graphs[1:]:
            merged_delta_graph = merged_delta_graph + delta_graph
        
        # Ensure namespace manager is preserved
        merged_delta_graph_path = os.path.join(run_dir, "merged_delta_graph.ttl")
        merged_delta_graph.serialize(format="turtle", destination=merged_delta_graph_path)
        append_trace(trace_path, "async_run.merged_delta_graph", payload={
            "path": merged_delta_graph_path,
            "num_triples": len(merged_delta_graph)
        })
    
    # Save run manifest
    with open(f"{run_dir}/run_manifest.json", "w", encoding="utf-8") as f:
        json.dump(run_manifest, f, indent=4)
    
    append_trace(trace_path, "async_run.finish", payload={"total_tasks": total_tasks})
