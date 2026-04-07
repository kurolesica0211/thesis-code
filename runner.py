import os
from tqdm import tqdm
import json
from langchain.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
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
    run_dir = _compute_run_dir(config)
    os.makedirs(run_dir, exist_ok=True)
    trace_path = os.path.join(run_dir, "trace.jsonl")
    append_trace(trace_path, "run.start")
    
    loader = _build_loader(config)
    
    append_trace(trace_path, "run.loader_instantiated")
    
    run_manifest = {
        "run_dir": run_dir,
        "config": config.model_dump(),
        "task_manifests": [],
        "trace": trace_path,
    }
    
    main_system_prompt_path = config.prompts.main_system
    main_user_prompt_path = config.prompts.main_user
    main_system_prompt = get_prompt(main_system_prompt_path)
    main_system_msg = SystemMessage(main_system_prompt)
    
    for task_entry in tqdm(loader.load(), total=loader.get_total()):
        task_entry: TaskEntry
        
        append_trace(trace_path, "run.entry.start", payload={
            "entry_idx": task_entry.entry_id
        })
        
        task_dir = os.path.join(run_dir, task_entry.entry_id)
        os.makedirs(task_dir, exist_ok=True)
        artifacts_dir = os.path.join(task_dir, "artifacts")
        os.makedirs(artifacts_dir, exist_ok=True)
        
        task_manifest_path = os.path.join(task_dir, "task_manifest.json")
        results_path = os.path.join(task_dir, "final_data_graph.ttl")
        task_manifest = {
            "entry_id": task_entry.entry_id,
            "done_reason": "",
            "artifacts_dir": artifacts_dir,
            "results": results_path
        }
        run_manifest["task_manifests"].append(task_manifest_path)
        
        tool_obj = ToolClass(task_entry.schema_def)
        agent = build_agent(tool_obj)
        
        main_user_prompt = format_prompt(
            main_user_prompt_path,
            data_graph=task_entry.data_graph.serialize(format="turtle"),
            ontology=task_entry.ontology_graph.serialize(format="turtle"),
            input_text=task_entry.input_text
        )
        main_user_msg = HumanMessage(main_user_prompt)
        
        llm = init_chat_model(
            model=config.model.name,
            temperature=config.model.temperature,
            max_retries=config.model.max_retries
        )
        llm = llm.bind_tools(tool_obj.tools_schemas)
        
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
                llm=llm,
                entry_id=task_entry.entry_id,
                input_text=task_entry.entry_id,
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
        append_trace(trace_path, "run.entry.finish", payload={
            "entry_idx": task_entry.entry_id,
            "done_reason": task_manifest["done_reason"]
        })
        
        #––––– Dump the results –––––––––––––––––––––––––––––––
        with open(results_path, "w") as f:
            f.write(final_state["data_graph"].serialize(format="turtle"))
            
        final_convo = "\n\n".join([msg.pretty_repr() for msg in final_state["messages"]])
        with open(f"{artifacts_dir}/final_convo.md", "w") as f:
            f.write(final_convo)
        
        usage_metadata = [msg.usage_metadata for msg in final_state["messages"] if type(msg) is AIMessage]
        with open(f"{artifacts_dir}/convo_usage_metadata.json", "w") as f:
            json.dump(usage_metadata, f, indent=4)
        
        with open(task_manifest_path, "w") as f:
            json.dump(task_manifest, f, indent=4)
        
    with open(f"{run_dir}/run_manifest.json", "w") as f:
        json.dump(run_manifest, f, indent=4)