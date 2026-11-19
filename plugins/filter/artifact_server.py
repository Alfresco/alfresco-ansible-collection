"""Artifact server filter for alfresco.platform collection."""

DOCUMENTATION = r"""
  name: artifact_server
  short_description: Pick the archive (Nexus) or Cloudsmith server for an artifact version
  version_added: 0.8.0
  author: Alfresco
  description:
    - Returns C(archive) when the version is at or below the archive bound of its major version, C(cloudsmith) otherwise.
    - A major version with no bound, or no bounds at all, returns C(cloudsmith).
    - Pre-release suffixes are ignored, so C(7.3.9-RC1) follows C(7.3.9).
    - Fails when a bound can't be compared with the version, instead of silently returning C(cloudsmith).
  options:
    _input:
      description: Artifact version, for example C(7.3.0) or C(7.4.0-RC1).
      type: str
      required: true
    archive_bounds:
      description:
        - Last version published on the archive server for each major version, for example C(['7.3.9', '23.4.2']).
        - Each version is matched with the bound that has the same major version.
      type: list
      elements: str
      required: true
"""

EXAMPLES = r"""
- name: Pick the server hosting the requested version
  ansible.builtin.set_fact:
    artifact_server: "{{ acs_version | alfresco.platform.artifact_server(['7.3.9', '23.4.2']) }}"
  # 7.3.9, 7.3.9-RC1 -> archive
  # 7.4.0, 25.1.0    -> cloudsmith
"""

RETURN = r"""
  _value:
    description: Server hosting the artifact, C(archive) or C(cloudsmith).
    type: str
    sample: archive
"""

from ansible_collections.alfresco.platform.plugins.plugin_utils.artifacts import (
    get_artifact_server,
)


def artifact_server(version, archive_bounds):
    """Return "archive" or "cloudsmith" for the given version."""
    return get_artifact_server(version, archive_bounds)


class FilterModule:
    def filters(self):
        return {"artifact_server": artifact_server}
