"""Shared helpers for the artifact filters."""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleFilterError
from ansible.module_utils.compat.version import LooseVersion

from ansible_collections.alfresco.platform.plugins.plugin_utils.components import (
    COMPONENTS,
)


def get_component(name):
    """Return the shipped metadata of a component."""
    if name not in COMPONENTS:
        raise AnsibleFilterError(
            "unknown component %s, expected one of: %s" % (name, ", ".join(sorted(COMPONENTS)))
        )
    return COMPONENTS[name]


def get_artifact_server(version, component):
    """Return "archive" if version is at or below the bound of its major, else "cloudsmith".

    component is a name from COMPONENTS, or an explicit list of bounds.
    """
    archive_bounds = component
    if isinstance(component, str):
        archive_bounds = get_component(component)["archive_last_versions"]
    if not archive_bounds:
        return "cloudsmith"
    if not isinstance(archive_bounds, list):
        raise AnsibleFilterError(
            "component must be a name or a list of versions, got %s" % type(archive_bounds).__name__
        )

    version = str(version)
    major = version.partition(".")[0]
    for bound in archive_bounds:
        bound = str(bound)
        if bound.partition(".")[0] != major:
            continue
        # Pre-releases precede their base version, unless the line uses suffixes as build numbers.
        compared = version if "-" in bound else version.partition("-")[0]
        try:
            return "archive" if LooseVersion(compared) <= LooseVersion(bound) else "cloudsmith"
        except (TypeError, ValueError) as e:
            raise AnsibleFilterError(
                "cannot compare version %s with archive bound %s: %s" % (version, bound, e)
            )
    return "cloudsmith"
