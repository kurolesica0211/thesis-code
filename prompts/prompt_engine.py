def format_prompt(prompt_path: str, **kwargs):
    with open(prompt_path, "r") as f:
        text = f.read()
    return text.format(**kwargs)

def get_prompt(prompt_path: str):
    with open(prompt_path, "r") as f:
        text = f.read()
    return text