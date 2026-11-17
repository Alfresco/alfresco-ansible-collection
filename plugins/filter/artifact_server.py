"""Artifact server filter for alfresco.platform collection."""

DOCUMENTATION = r"""
  name: artifact_server
  short_description: Determine artifact server based on version and bounds
  author: Alfresco
  description:
    - Determines which server should host an artifact based on the version and archive version bounds.
    - Versions up to and including the bound for their major version use "archive" (Nexus).
    - Versions beyond the bound or unknown major versions use "cloudsmith" (Cloudsmith).
  options:
    version:
      description: The version string (e.g., "7.3.0", "7.4.0-SNAPSHOT")
      type: string
      required: true
    archive_bounds:
      description:
        - Dictionary with major versions as keys (integers) and upper bounds as values (strings).
        - 'Example: C({"7": "7.3.9"}) means major version 7 uses archive if version <= 7.3.9.'
        - If a major version is not in the dict, it defaults to cloudsmith.
      type: dict
      required: true
"""

EXAMPLES = r"""
# Determine server for a release version at the bound
- name: Archive version at bound
  ansible.builtin.debug:
    msg: "{{ '7.3.9' | alfresco.platform.artifact_server({7: '7.3.9'}) }}"
  # Result: "archive"

# Determine server for a release version below the bound
- name: Archive version below bound
  ansible.builtin.debug:
    msg: "{{ '7.3.0' | alfresco.platform.artifact_server({7: '7.3.9'}) }}"
  # Result: "archive"

# Determine server for a newer version
- name: Cloudsmith version above bound
  ansible.builtin.debug:
    msg: "{{ '7.4.0' | alfresco.platform.artifact_server({7: '7.3.9'}) }}"
  # Result: "cloudsmith"

# Version with snapshot suffix
- name: Snapshot version
  ansible.builtin.debug:
    msg: "{{ '7.3.0-SNAPSHOT' | alfresco.platform.artifact_server({7: '7.3.9'}) }}"
  # Result: "archive"

# Use in a playbook
- name: Set artifact server fact
  ansible.builtin.set_fact:
    artifact_server: "{{ acs_version | alfresco.platform.artifact_server(archive_bounds) }}"
"""

RETURN = r"""
  _value:
    description: The name of the artifact server
    type: string
    returned: always
    sample: "archive"
"""

from ansible_collections.alfresco.platform.plugins.module_utils.artifacts import (
    get_artifact_server,
)


def artifact_server(version, archive_bounds):
    """
    Determine which server hosts the artifact based on version and bounds.

    Args:
        version: Version string (e.g., "7.3.0", "7.4.0-SNAPSHOT")
        archive_bounds: Dict with major versions as keys and upper bounds as values.
                       E.g., {7: "7.3.9"} means major version 7 uses archive if <= 7.3.9

    Returns:
        "archive" if version matches a bound and is <= the bound value
        "cloudsmith" otherwise (unknown major or not within bounds)
    """
    return get_artifact_server(version, archive_bounds)


class FilterModule:
    """FilterModule for artifact_server filter."""

    def filters(self):
        """Return filter functions."""
        return {
            "artifact_server": artifact_server,
        }
