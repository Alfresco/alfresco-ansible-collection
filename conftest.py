"""Pytest configuration for ansible collection testing.

This conftest sets up the import path so that tests can import from
ansible_collections.alfresco.platform.* without requiring the repo to be
checked out in the standard ansible_collections directory structure.

It uses sys.modules to create virtual packages without creating actual
directories in the repository.
"""

import sys
from pathlib import Path
from types import ModuleType


def _make_module(name, path=None):
    """Create and register a module in sys.modules."""
    mod = ModuleType(name)
    mod.__file__ = None
    if path:
        mod.__path__ = [str(path)]
        mod.__file__ = str(path / "__init__.py")
    sys.modules[name] = mod
    return mod


# Get the repository root
repo_root = Path(__file__).parent

# Add repo root to sys.path to find our packages
sys.path.insert(0, str(repo_root))

# Create virtual packages for ansible_collections.alfresco.platform
# This allows imports like: from ansible_collections.alfresco.platform.plugins.filter.artifact_server
_make_module("ansible_collections")
_make_module("ansible_collections.alfresco")
_make_module("ansible_collections.alfresco.platform", repo_root)
_make_module("ansible_collections.alfresco.platform.plugins", repo_root / "plugins")
_make_module("ansible_collections.alfresco.platform.plugins.filter", repo_root / "plugins" / "filter")
_make_module("ansible_collections.alfresco.platform.plugins.module_utils", repo_root / "plugins" / "module_utils")
