"""Artifact server filter for alfresco.platform collection."""

DOCUMENTATION = r"""
  name: artifact_server
  short_description: Pick the archive (Nexus) or Cloudsmith server for an artifact version
  version_added: 0.8.0
  author: Alfresco
  description:
    - Returns C(archive) when the version is at or below the last archive version of its major version, C(cloudsmith) otherwise.
    - The collection ships the last archive versions of each Alfresco component, selected by name.
    - A major version with no bound, or no bounds at all, returns C(cloudsmith).
    - Pre-release suffixes are ignored, so C(7.3.9-RC1) follows C(7.3.9), unless the bound has a suffix too (build numbers such as C(1.3.0-86)).
    - Fails when a bound can't be compared with the version, instead of silently returning C(cloudsmith).
  options:
    _input:
      description: Artifact version, for example C(7.3.0) or C(7.4.0-RC1).
      type: str
      required: true
    component:
      description:
        - Component name, for example C(repository), C(search_enterprise) or C(aps_app).
          Its last archive versions come from C(plugins/plugin_utils/archive_versions.py). An unknown name fails.
        - Can also be an explicit list of last archive versions, one per major version, for example C(['7.3.9', '23.4.2']).
      type: raw
      required: true
"""

EXAMPLES = r"""
- name: Pick the server hosting the requested version
  ansible.builtin.set_fact:
    artifact_server: "{{ acs_version | alfresco.platform.artifact_server('repository') }}"
  # 7.4.2.6, 23.7.3 -> archive
  # 7.4.3, 23.8.0   -> cloudsmith

- name: Pick the server with explicit bounds
  ansible.builtin.set_fact:
    artifact_server: "{{ my_version | alfresco.platform.artifact_server(['7.3.9', '23.4.2']) }}"
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


class FilterModule:
    def filters(self):
        return {"artifact_server": get_artifact_server}
