import os
import tqdm
from langchain.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model

from configs.run_config import RunConfig
from loaders.base_family_loader import get_loader as base_family_get_loader
from orchestration.tools import ToolClass
from orchestration.tracing import append_trace
from orchestration.agent import build_agent, TaskState, TaskContext
from prompts.prompt_engine import get_prompt, format_prompt
from models.data_models import TaskEntry

def _build_loader(config: RunConfig):
    if config.dataset.source == "custom_family_bench":
        loader = base_family_get_loader()
        
    return loader

def _compute_run_dir(config: RunConfig) -> str:
    if config.output.run_dir:
        return config.output.run_dir
    
    custom_tag = config.output.custom_tag
    safe_model = config.model.name.replace("/", "_").replace(":", "_")
    return os.path.join(config.output.base_dir, f"{custom_tag}_{safe_model}")

def run(config: RunConfig):
    loader = _build_loader(config)
    run_dir = _compute_run_dir(config)
    os.makedirs(run_dir, exist_ok=True)
    
    trace_path = os.path.join(run_dir, "trace.jsonl")
    append_trace(trace_path, "run.start")
    
    run_manifest = {
        "run_dir": run_dir,
        "config": config.model_dump(),
        "task_entries": [],
        "results": "",
        "trace": trace_path,
    }
    
    manifests_dir = os.path.join(run_dir, "manifests")
    os.makedirs(manifests_dir)
    
    artifacts_dir = os.path.join(run_dir, "artifacts")
    os.makedirs(artifacts_dir)
    
    main_system_prompt_path = config.prompts.main_system
    main_user_prompt_path = config.prompts.main_user
    main_system_prompt = get_prompt(main_system_prompt_path)
    main_system_msg = SystemMessage(main_system_prompt)
    
    for task_entry in tqdm(loader.load(), total=loader.get_total()):
        task_entry: TaskEntry
        
        append_trace(trace_path, "run.entry.start", payload={
            "entry_idx": task_entry.entry_id
        })
        
        task_artifacts_dir = os.path.join(artifacts_dir, task_entry.entry_id)
        os.makedirs(task_artifacts_dir, exist_ok=True)
        
        task_manifest_path = os.path.join(manifests_dir, f"{task_entry.entry_id}.json")
        task_manifest = {
            "entry_id": task_entry.entry_id,
            "done_reason": "",
            "artifacts_dir": task_artifacts_dir
        }
        run_manifest["task_entries"].append(task_manifest_path)
        
        tool_obj = ToolClass(task_entry.schema_def)
        agent = build_agent(tool_obj)
        append_trace(trace_path, "run.entry.agent.invoke", payload={
            "entry_id": task_entry.entry_id,
        })
        
        main_user_prompt = format_prompt(
            main_user_prompt_path,
            data_graph=task_entry.data_graph.serialize(format="turtle"),
            ontology=task_entry.ontology_graph.serialize(format="turtle")
        )
        main_user_msg = HumanMessage(main_user_prompt)
        
        llm = init_chat_model(model=config.model.name)
        
        agent.invoke(
            input=TaskState(
                messages=[main_system_msg, main_user_msg],
                data_graph=task_entry.data_graph,
                run_manifest=run_manifest
            ),
            context=TaskContext(
                llm=llm,
                entry_id=task_entry.entry_id,
                input_text=task_entry.entry_id,
                ontology_graph=task_entry.ontology_graph,
                shacl_graph=task_entry.shacl_graph,
                artifact_dir=task_artifacts_dir,
                tracing_path=trace_path,
                config=config.model_dump(),
                task_manifest=task_manifest
            )
        )
        
        append_trace(trace_path, "run.entry.finish", payload={
            "entry_idx": task_entry.entry_id
        })