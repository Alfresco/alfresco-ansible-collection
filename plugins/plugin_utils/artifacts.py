"""Shared helpers for the artifact filters."""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleFilterError
from ansible.module_utils.compat.version import LooseVersion

from ansible_collections.alfresco.platform.plugins.plugin_utils.archive_versions import (
    ARCHIVE_LAST_VERSIONS,
)


def get_artifact_server(version, component):
    """Return "archive" if version is at or below the bound of its major, else "cloudsmith".

    component is a name from ARCHIVE_LAST_VERSIONS, or an explicit list of bounds.
    """
    archive_bounds = component
    if isinstance(component, str):
        if component not in ARCHIVE_LAST_VERSIONS:
            raise AnsibleFilterError(
                "unknown component %s, expected one of: %s"
                % (component, ", ".join(sorted(ARCHIVE_LAST_VERSIONS)))
            )
        archive_bounds = ARCHIVE_LAST_VERSIONS[component]
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
