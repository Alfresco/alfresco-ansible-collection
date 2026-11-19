"""Artifact URL filter for alfresco.platform collection."""

DOCUMENTATION = r"""
  name: artifact_url
  short_description: Build the download URL of a Maven artifact on the archive or Cloudsmith server
  version_added: 0.8.0
  author: Alfresco
  description:
    - Builds the download and checksum URLs of a Maven artifact, picking the server with the
      R(artifact_server filter,ansible_collections.alfresco.platform.artifact_server_filter) logic.
    - A version with a C(-) suffix (for example C(7.4.0-RC1)) uses the C(staging) repository, any other the C(release) one.
    - C(-SNAPSHOT) versions are rejected, since their file names are timestamped and need C(maven-metadata.xml) to resolve.
    - Returns the selected C(server) too, so the caller can pick matching credentials.
  options:
    _input:
      description: Artifact version, for example C(7.3.0) or C(7.4.0-RC1).
      type: str
      required: true
    group_id:
      description: Maven group ID, for example C(org.alfresco).
      type: str
      required: true
    artifact_id:
      description: Maven artifact ID, for example C(alfresco-platform).
      type: str
      required: true
    archive_bounds:
      description: Last version published on the archive server for each major version, as in the artifact_server filter.
      type: list
      elements: str
      required: true
    repos:
      description:
        - Base repository URLs, keyed by server and then maturity.
        - 'Structure: C({"archive": {"release": url, "staging": url}, "cloudsmith": {"release": url, "staging": url}}).'
      type: dict
      required: true
    ext:
      description: File extension.
      type: str
      default: jar
"""

EXAMPLES = r"""
- name: Download the APS war from the server that hosts the requested version
  vars:
    aps_artifact: "{{ aps_version | alfresco.platform.artifact_url('com.activiti', 'activiti-app', ['2.4.8', '24.4.1'], repos, ext='war') }}"
    repos:
      archive:
        release: https://artifacts.alfresco.com/nexus/repository/activiti-enterprise-releases
        staging: https://artifacts.alfresco.com/nexus/repository/activiti-enterprise-staging
      cloudsmith:
        release: https://artifacts.hyland.dev/basic/alfresco-private/maven
        staging: https://artifacts.hyland.dev/basic/alfresco-internal/maven
  ansible.builtin.get_url:
    url: "{{ aps_artifact.url }}"
    checksum: "sha1:{{ aps_artifact.checksum_url }}"
    dest: /tmp/activiti-app.war
    url_username: "{{ credentials[aps_artifact.server].username }}"
    url_password: "{{ credentials[aps_artifact.server].password }}"
"""

RETURN = r"""
  _value:
    description: Artifact descriptor.
    type: dict
    contains:
      server:
        description: Server hosting the artifact, C(archive) or C(cloudsmith).
        type: str
        sample: archive
      maturity:
        description: Repository maturity, C(release) or C(staging).
        type: str
        sample: release
      repo_url:
        description: Base repository URL, without trailing slash.
        type: str
        sample: https://artifacts.alfresco.com/nexus/repository/activiti-enterprise-releases
      url:
        description: Artifact download URL.
        type: str
        sample: https://artifacts.alfresco.com/nexus/repository/activiti-enterprise-releases/com/activiti/activiti-app/24.4.1/activiti-app-24.4.1.war
      checksum_url:
        description: SHA-1 checksum URL of the artifact.
        type: str
        sample: https://artifacts.alfresco.com/nexus/repository/activiti-enterprise-releases/com/activiti/activiti-app/24.4.1/activiti-app-24.4.1.war.sha1
"""

from ansible.errors import AnsibleFilterError

from ansible_collections.alfresco.platform.plugins.plugin_utils.artifacts import (
    get_artifact_maturity,
    get_artifact_server,
)


def artifact_url(version, group_id, artifact_id, archive_bounds, repos, ext="jar"):
    """Return the server, maturity, repo, download and checksum URLs of a Maven artifact."""
    version = str(version)
    maturity = get_artifact_maturity(version)
    server = get_artifact_server(version, archive_bounds)

    try:
        repo_url = repos[server][maturity].rstrip("/")
    except KeyError:
        raise AnsibleFilterError("repos has no URL for repos['%s']['%s']" % (server, maturity))

    url = "%s/%s/%s/%s/%s-%s.%s" % (
        repo_url, group_id.replace(".", "/"), artifact_id, version, artifact_id, version, ext
    )
    return {
        "server": server,
        "maturity": maturity,
        "repo_url": repo_url,
        "url": url,
        "checksum_url": url + ".sha1",
    }


class FilterModule:
    def filters(self):
        return {"artifact_url": artifact_url}
