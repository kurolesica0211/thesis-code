import sys
from pathlib import Path
from typing import TypeAlias
from dotenv import load_dotenv
import re
from enum import Enum

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

from rdflib import XSD

literals = {name: getattr(XSD, name) for (name, _) in vars(XSD)["__annotations__"].items() if re.match("[a-z][a-zA-Z]*", name)}
GraphLiterals = Enum("GraphLiterals", literals)

def a(b: GraphLiterals):
    print(type(b.value))
    
print(literals["month"])
a(GraphLiterals.month)