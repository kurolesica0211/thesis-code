# LLM-based Knowledge Graph Construction Pipeline

This repository contains a pipeline that uses an LLM agent to extract or refine
knowledge graphs, validate them with SHACL, and store run artifacts.

## Quick start

1. Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` file at the repository root for any model
credentials or environment variables the LLM adapter requires. The pipeline
calls `load_dotenv()` on startup.

4. Run the example pipeline (uses the example config by default):

```bash
python main.py
# or explicitly:
python main.py --config configs/example_run_config.yaml
```

5. To run in asynchronous (concurrent) mode, enable it in the YAML config:

```yaml
# in configs/example_run_config.yaml or your chosen config
runtime:
  async_mode: true
```

Then run the same `python main.py` command.

## Full dataset / production runs

The `main.py` includes a convenience commented line that points to the full
run config. If you wish to run against your full dataset, either:

- point the CLI at `configs/run_config.yaml` explicitly:

```bash
python main.py --config configs/run_config.yaml
```

- or uncomment the reserved line in `main.py` that references the full config
  (this line is left commented for convenience so casual runs use the
  `example_run_config.yaml`). See [main.py](main.py#L22) for the commented line.

## Outputs & artifacts

- Run artifacts are written under `results/` by default. Each run gets a
  `run_dir` (computed from `output` settings in the config).
- Per-task artifacts (conversations, usage metadata, graphs) are stored under
  each task's `artifacts/` folder. A `trace.jsonl` file is also created in the
  run directory for tracing events.

## Configuring the run

- The main config model is `configs/run_config.yaml`. See
  [configs/run_config.py](configs/run_config.py) for the schema used by the
  loader.
- Prompts live in `prompts/`. Use `prompts/main_user.md` and
  `prompts/main_system.md` to customize agent behavior.

## Notes

- SHACL validation is performed via `pyshacl`; ensure it is available in your
  environment (it is included in `requirements.txt` for the repository).
- If you use cloud LLMs, ensure any required API keys are set in your
  environment or `.env` file before running.