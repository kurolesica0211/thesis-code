import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pydantic import BaseModel, Field, create_model
from typing import Annotated, List

Model = create_model("Model", __doc__="AAA")
print(Model().__doc__)