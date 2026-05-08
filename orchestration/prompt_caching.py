from contextlib import contextmanager
from typing import Sequence
from google import genai
from google.genai import types


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
            ttl="300s",
        ),
    )
    try:
        yield cache
    finally:
        client.caches.delete(name=cache.name)
        
def check_gemini(model: str):
    return model.startswith("google_genai:")