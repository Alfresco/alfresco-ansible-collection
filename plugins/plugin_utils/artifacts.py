"""Shared helpers for the artifact filters."""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleFilterError
from ansible.module_utils.compat.version import LooseVersion


def get_artifact_server(version, archive_bounds):
    """Return "archive" if version is at or below the bound of its major, else "cloudsmith"."""
    if not archive_bounds:
        return "cloudsmith"
    if not isinstance(archive_bounds, list):
        raise AnsibleFilterError(
            "archive_bounds must be a list of versions, got %s" % type(archive_bounds).__name__
        )

    # Pre-releases precede their base version, so they ship from the same server.
    base = str(version).partition("-")[0]
    major = base.partition(".")[0]
    for bound in archive_bounds:
        bound = str(bound)
        if bound.partition(".")[0] != major:
            continue
        try:
            return "archive" if LooseVersion(base) <= LooseVersion(bound) else "cloudsmith"
        except (TypeError, ValueError) as e:
            raise AnsibleFilterError(
                "cannot compare version %s with archive bound %s: %s" % (version, bound, e)
            )
    return "cloudsmith"


def get_artifact_maturity(version):
    """Return "staging" for a suffixed version, "release" otherwise. Snapshots are rejected."""
    version = str(version)
    if version.endswith("-SNAPSHOT"):
        raise AnsibleFilterError(
            "%s: SNAPSHOT versions are not supported, their file names are timestamped" % version
        )
    return "staging" if "-" in version else "release"
