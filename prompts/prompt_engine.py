"""Simple prompt loading and templating utilities.

Prompts are plain text files in the `prompts/` directory. `format_prompt`
performs Python-style `.format(...)` substitution on the loaded text.
"""


def format_prompt(prompt_path: str, **kwargs):
    """Load a prompt file and format it with `kwargs`.

    Returns the rendered string.
    """
    with open(prompt_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text.format(**kwargs)


def get_prompt(prompt_path: str):
    """Return the raw contents of a prompt file as a string."""
    with open(prompt_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text