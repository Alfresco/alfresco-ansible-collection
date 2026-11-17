"""Shared utilities for artifact filters."""

from ansible.module_utils.compat.version import LooseVersion


def get_artifact_server(version, archive_bounds):
    """
    Determine which server hosts the artifact based on version and bounds.

    Args:
        version: Version string (e.g., "7.3.0", "7.4.0-SNAPSHOT")
        archive_bounds: Dict with major versions as keys (integers or strings that parse as integers)
                       and upper bounds as values (strings).
                       E.g., {7: "7.3.9"} or {"7": "7.3.9"} means major version 7 uses archive if <= 7.3.9
                       Keys are normalized to integers.

    Returns:
        "archive" if version matches a bound and is <= the bound value
        "cloudsmith" otherwise (unknown major or not within bounds)
    """
    if not archive_bounds:
        return "cloudsmith"

    # Extract major version from version string (before first dot or suffix)
    major_str = version.split(".")[0]
    try:
        major = int(major_str)
    except ValueError:
        return "cloudsmith"

    # Normalize bounds keys to integers to handle both {7: ...} and {"7": ...}
    normalized_bounds = {}
    for key, value in archive_bounds.items():
        try:
            normalized_bounds[int(key)] = value
        except (ValueError, TypeError):
            # Skip keys that can't be converted to int
            pass

    if major not in normalized_bounds:
        return "cloudsmith"

    bound_version = normalized_bounds[major]
    try:
        if LooseVersion(version) <= LooseVersion(bound_version):
            return "archive"
    except (ValueError, TypeError):
        pass

    return "cloudsmith"


def get_artifact_maturity(version):
    """
    Determine maturity from version suffix.

    Args:
        version: Version string (e.g., "7.3.0", "7.4.0-SNAPSHOT", "7.3.0-RC1")

    Returns:
        "snapshot" for -SNAPSHOT suffix
        "staging" for other suffixes (e.g., -RC1, -Beta)
        "release" for no suffix
    """
    if version.endswith("-SNAPSHOT"):
        return "snapshot"
    elif "-" in version:
        return "staging"
    return "release"
