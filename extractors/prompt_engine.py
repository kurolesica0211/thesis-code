import os
from typing import List
from models.data_models import Schema, TaskEntry

def format_prompt(prompt_path: str, **kwargs):
    with open(prompt_path, "r") as f:
        text = f.read()
    return text.format(**kwargs)