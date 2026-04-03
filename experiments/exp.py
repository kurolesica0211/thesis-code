import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers import strip_uri, strip_ns

print(f"AAA: {[1,2,3]}")