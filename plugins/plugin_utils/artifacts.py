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


def get_prerelease_separator(component):
    """Return the string that starts a pre-release suffix, or None if the component has none."""
    if isinstance(component, str):
        return get_component(component).get("prerelease_separator", "-")
    return "-"


def _version_key(version, separator):
    """Order key where a pre-release precedes the GA version of the same base."""
    if not separator or separator not in version:
        return (LooseVersion(version), 1, LooseVersion("0"))
    base, _sep, suffix = version.partition(separator)
    return (LooseVersion(base), 0, LooseVersion(suffix))


def get_artifact_server(version, component):
    """Return "archive" if version is at or below the bound of its major, else "cloudsmith".

    component is a name from COMPONENTS, or an explicit list of bounds.
    """
    archive_bounds = component
    if isinstance(component, str):
        archive_bounds = get_component(component)["archive_last_versions"]
    if archive_bounds is not None and not isinstance(archive_bounds, list):
        raise AnsibleFilterError(
            "component must be a name or a list of versions, got %s" % type(archive_bounds).__name__
        )
    if not archive_bounds:
        return "cloudsmith"

    separator = get_prerelease_separator(component)
    version = str(version)
    major = version.partition(".")[0]
    for bound in archive_bounds:
        bound = str(bound)
        if bound.partition(".")[0] != major:
            continue
        try:
            at_or_below = _version_key(version, separator) <= _version_key(bound, separator)
        except (TypeError, ValueError) as e:
            raise AnsibleFilterError(
                "cannot compare version %s with archive bound %s: %s" % (version, bound, e)
            )
        return "archive" if at_or_below else "cloudsmith"
    return "cloudsmith"
