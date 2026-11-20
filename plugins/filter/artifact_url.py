"""Artifact URL filter for alfresco.platform collection."""

DOCUMENTATION = r"""
  name: artifact_url
  short_description: Build the download URL of a Maven artifact on the archive or Cloudsmith server
  version_added: 0.8.0
  author: Alfresco
  description:
    - Builds the download and checksum URLs of a Maven artifact, picking the server with the
      R(artifact_server filter,ansible_collections.alfresco.platform.artifact_server_filter) logic.
    - A version with a pre-release suffix (for example C(7.4.0-RC1)) uses the C(staging) repository, any other the C(release) one.
    - The suffix starts at C(-), unless the component sets C(prerelease_separator) to C(None) in its metadata
      because it has no pre-releases and uses C(-) for release build numbers (C(transformers_pdf) C(1.3.0-86)).
    - C(-SNAPSHOT) versions are rejected, since their file names are timestamped and need C(maven-metadata.xml) to resolve.
    - Returns the selected C(server) too, so the caller can pick matching credentials.
    - For components that ship their Maven coordinates and repositories (for example C(aps_app) and C(aps_admin)),
      the component name is enough. Any option passed overrides the shipped value, for example C(repos) to use a mirror.
  options:
    _input:
      description: Artifact version, for example C(7.3.0) or C(7.4.0-RC1).
      type: str
      required: true
    component:
      description:
        - Component name from C(plugins/plugin_utils/components.py), or an explicit list of last archive versions as in the artifact_server filter.
        - With a list, or a component that doesn't ship them, C(repos), C(group_id) and C(artifact_id) are required.
      type: raw
      required: true
    repos:
      description:
        - Base repository URLs, keyed by server and then maturity. Defaults to the component's shipped repositories.
        - 'Structure: C({"archive": {"release": url, "staging": url}, "cloudsmith": {"release": url, "staging": url}}).'
      type: dict
    group_id:
      description: Maven group ID, for example C(com.activiti). Defaults to the component's shipped value.
      type: str
    artifact_id:
      description: Maven artifact ID, for example C(activiti-app). Defaults to the component's shipped value.
      type: str
    ext:
      description: File extension. Defaults to the component's shipped value, or C(jar).
      type: str
"""

EXAMPLES = r"""
- name: Download the APS war from the server that hosts the requested version
  vars:
    aps_artifact: "{{ aps_version | alfresco.platform.artifact_url('aps_app') }}"
  ansible.builtin.get_url:
    url: "{{ aps_artifact.url }}"
    checksum: "sha1:{{ aps_artifact.checksum_url }}"
    dest: /tmp/activiti-app.war
    url_username: "{{ credentials[aps_artifact.server].username }}"
    url_password: "{{ credentials[aps_artifact.server].password }}"

- name: Build the URL of an artifact the collection doesn't describe
  ansible.builtin.set_fact:
    my_artifact: >-
      {{ my_version | alfresco.platform.artifact_url(['1.4.2'], repos=my_repos,
         group_id='org.example', artifact_id='my-app', ext='zip') }}
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
    get_artifact_server,
    get_component,
    get_prerelease_separator,
)


def artifact_url(version, component, repos=None, group_id=None, artifact_id=None, ext=None):
    """Return the server, maturity, repo, download and checksum URLs of a Maven artifact."""
    shipped = get_component(component) if isinstance(component, str) else {}
    repos = repos or shipped.get("repos")
    group_id = group_id or shipped.get("group_id")
    artifact_id = artifact_id or shipped.get("artifact_id")
    ext = ext or shipped.get("ext", "jar")
    missing = [k for k, v in (("repos", repos), ("group_id", group_id), ("artifact_id", artifact_id)) if not v]
    if missing:
        raise AnsibleFilterError("%s: pass %s, the collection doesn't ship them" % (component, ", ".join(missing)))

    version = str(version)
    if version.endswith("-SNAPSHOT"):
        raise AnsibleFilterError(
            "%s: SNAPSHOT versions are not supported, their file names are timestamped" % version
        )
    separator = get_prerelease_separator(component)
    maturity = "staging" if separator and separator in version else "release"
    server = get_artifact_server(version, component)

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
