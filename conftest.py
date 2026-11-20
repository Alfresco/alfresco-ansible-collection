"""Expose the repo as ansible_collections.alfresco.platform so unit tests can import plugins without a collections tree."""

import sys
from pathlib import Path
from types import ModuleType

for name, path in [
    ("ansible_collections", None),
    ("ansible_collections.alfresco", None),
    ("ansible_collections.alfresco.platform", Path(__file__).parent),
]:
    module = ModuleType(name)
    if path:
        module.__path__ = [str(path)]
    sys.modules[name] = module
