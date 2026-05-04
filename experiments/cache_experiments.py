from __future__ import annotations

import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

from google import genai
from google.genai import types
from typing import Sequence
from contextlib import contextmanager
from langchain.messages import HumanMessage, SystemMessage, ToolMessage
from prompts.prompt_engine import get_prompt, format_prompt
from loaders.look_up_family_loader import get_loader as look_up_family_get_loader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model
from orchestration.tools import ToolClass


client = genai.Client()
model = "google_genai:gemini-3.1-flash-lite-preview"

loader = look_up_family_get_loader()
task_entry = list(loader.load())[-1]
main_system_prompt_path = "prompts/main_system.md"
main_user_prompt_path = "prompts/main_user.md"
main_system_prompt = get_prompt(main_system_prompt_path)
main_system_msg = SystemMessage(main_system_prompt)
main_user_prompt = format_prompt(
    main_user_prompt_path,
    data_graph=task_entry.data_graph.serialize(format="turtle"),
    ontology=task_entry.ontology_graph.serialize(format="turtle"),
    input_text=task_entry.input_text
)
main_user_msg = HumanMessage(main_user_prompt)
tool_obj = ToolClass(task_entry.schema_def, task_entry.data_graph, True)

def _build_cache_tools(tool_schemas: Sequence[type] | None):
    tools = []
    for schema in tool_schemas or []:
        tools.append(
            types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(
                        name=schema.__name__,
                        description=(schema.__doc__ or "").strip(),
                        parameters_json_schema=schema.model_json_schema(),
                    )
                ]
            )
        )
    return tools


@contextmanager
def google_cache(
    model: str,
    system_prompt: str,
    user_prompt: str,
    tool_schemas: Sequence[type] | None = None,
):
    client = genai.Client()
    cache = client.caches.create(
        model=model.removeprefix("google_genai:"),
        config=types.CreateCachedContentConfig(
            display_name="Cached Content",
            system_instruction=system_prompt,
            contents=[
                ("human", user_prompt)
            ],
            tools=_build_cache_tools(tool_schemas),
            tool_config=types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(mode="ANY")
            ) if tool_schemas else None,
            ttl="120s",
        ),
    )
    try:
        yield cache
    finally:
        client.caches.delete(name=cache.name)

with google_cache(model, main_system_prompt, main_user_prompt, tool_obj.tools_schemas) as cache:
    llm = init_chat_model(
        model=model,
        cached_content=cache.name
    )
    print(llm.invoke([HumanMessage(content="Start the work")]))

'''
for cache in client.caches.list():
    #print(cache)
    client.caches.delete(name=cache.name)'''