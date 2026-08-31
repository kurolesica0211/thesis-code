# Prompts

Overview of the prompt files under [prompts/](../prompts/), loaded via [prompt_engine.py](../prompts/prompt_engine.py) and wired up in [configs/run_config.py](../configs/run_config.py). Naming convention:

- **`*_system`** — system prompts given to an LLM up front, defining its role and rules.
- **`*_user`** — user prompts, filled in per-task with the actual input data.
- **`translation_*`** — prompts for the separate "explanation" LLM module, which takes raw SHACL violation reports and turns them into concise, noise-free instructions for the main agent.

## Main agent

- [main_system.md](../prompts/main_system.md) — System prompt for the main knowledge-graph-editing agent, used in the SHACL-enabled pipeline. Defines its role as a strict, text-grounded KG engineer, the entity-naming/identifier conventions, the triple directionality rules (source/relation/target), the tool usage constraints, and the required workflow ending in `ValidateShacl` before `Finish`.
- [main_system_without_shacl.md](../prompts/main_system_without_shacl.md) — Variant of `main_system.md` for the no-SHACL baseline/ablation run: same grounding, naming, and directionality rules, but drops the `ValidateShacl` step and its associated instructions since no SHACL validation is available in that setting.
- [main_user.md](../prompts/main_user.md) — User prompt template for the main agent. Injects the input text, ontology, and current data graph state, and reiterates the strict-grounding instruction before asking the agent to proceed with tool calls.
- [not_typed.md](../prompts/not_typed.md) — Follow-up correction prompt sent to the main agent when it calls `Finish` while nodes are still missing a class assignment. Lists the offending nodes and instructs the agent to assign classes before retrying.

## Explanation ("translation") module

- [translation_system.md](../prompts/translation_system.md) — System prompt for the SHACL-explanation LLM. Defines its role as a SHACL interpretation expert that converts raw violation reports into a structured explanation + fix instruction for each violation, referencing the main agent's available tools.
- [translation_user.md](../prompts/translation_user.md) — User prompt template for the explanation module. Injects the raw SHACL violations and asks for one explanation/instruction block per violation, in the same order as the input.
