"""Maven artifact filter for alfresco.platform collection."""

DOCUMENTATION = r"""
  name: maven_artifact
  short_description: Build a Maven artifact descriptor with server, URL, and checksum URL
  author: Alfresco
  description:
    - Builds a complete Maven artifact descriptor including the server (archive or cloudsmith),
      repository URL, full artifact URL, and checksum URL.
    - Maturity is determined from the version suffix (SNAPSHOT, staging, or release).
    - The server is determined using the L(artifact_server filter, artifact_server.rst) logic.
  options:
    version:
      description: Version string (e.g., "7.3.0", "7.4.0-SNAPSHOT")
      type: str
      required: true
    group_id:
      description: Maven group ID (e.g., "org.alfresco")
      type: str
      required: true
    artifact_id:
      description: Maven artifact ID (e.g., "alfresco-platform")
      type: str
      required: true
    archive_bounds:
      description:
        - Dictionary for artifact_server logic (major version -> bound version).
        - See L(artifact_server filter, artifact_server.rst) for format.
      type: dict
      required: true
    repos:
      description:
        - Repository configuration with archive and cloudsmith URLs per maturity.
        - 'Structure: C({"server": {"release": url, "staging": url, "snapshot": url}}).'
        - Both C(archive) and C(cloudsmith) keys must be present with all three maturity levels.
      type: dict
      required: true
    ext:
      description: File extension (default "jar")
      type: str
      default: jar
"""

EXAMPLES = r"""
# Build artifact descriptor for a release version
- name: Get artifact descriptor for archive release
  ansible.builtin.set_fact:
    artifact: "{{ '7.3.0' | alfresco.platform.maven_artifact(
        'org.alfresco',
        'alfresco-platform',
        {7: '7.3.9'},
        repos
      ) }}"
  vars:
    repos:
      archive:
        release: "https://artifacts.alfresco.com/nexus/release"
        staging: "https://artifacts.alfresco.com/nexus/staging"
        snapshot: "https://artifacts.alfresco.com/nexus/snapshot"
      cloudsmith:
        release: "https://dl.cloudsmith.io/public/alfresco/alfresco-public/maven/"
        staging: "https://dl.cloudsmith.io/public/alfresco/alfresco-public/maven/"
        snapshot: "https://dl.cloudsmith.io/public/alfresco/alfresco-public/maven/"

# Access the artifact URL
- name: Show artifact URL
  ansible.builtin.debug:
    msg: "Download from {{ artifact.url }}"
  vars:
    artifact: "{{ '7.3.0' | alfresco.platform.maven_artifact(
        'org.alfresco',
        'alfresco-platform',
        {7: '7.3.9'},
        repos
      ) }}"
    repos:
      archive:
        release: "https://artifacts.alfresco.com/nexus/release"
        staging: "https://artifacts.alfresco.com/nexus/staging"
        snapshot: "https://artifacts.alfresco.com/nexus/snapshot"
      cloudsmith:
        release: "https://dl.cloudsmith.io/public/alfresco/alfresco-public/maven/"
        staging: "https://dl.cloudsmith.io/public/alfresco/alfresco-public/maven/"
        snapshot: "https://dl.cloudsmith.io/public/alfresco/alfresco-public/maven/"
"""

RETURN = r"""
  _value:
    description: Artifact descriptor dictionary
    type: dict
    returned: always
    contains:
      server:
        description: The artifact server name
        type: str
        sample: "archive"
      maturity:
        description: Version maturity level
        type: str
        sample: "release"
      repo_url:
        description: Base repository URL
        type: str
        sample: "https://artifacts.alfresco.com/nexus/release"
      url:
        description: Full artifact URL
        type: str
        sample: "https://artifacts.alfresco.com/nexus/release/org/alfresco/alfresco-platform/7.3.0/alfresco-platform-7.3.0.jar"
      checksum_url:
        description: Checksum URL (artifact URL with .sha1 appended)
        type: str
        sample: "https://artifacts.alfresco.com/nexus/release/org/alfresco/alfresco-platform/7.3.0/alfresco-platform-7.3.0.jar.sha1"
"""

from ansible.errors import AnsibleFilterError

from ansible_collections.alfresco.platform.plugins.module_utils.artifacts import (
    get_artifact_maturity,
    get_artifact_server,
)


def maven_artifact(version, group_id, artifact_id, archive_bounds, repos, ext="jar"):
    """
    Build a Maven artifact descriptor with server, URL, and checksum URL.

    Args:
        version: Version string (e.g., "7.3.0", "7.4.0-SNAPSHOT")
        group_id: Maven group ID (e.g., "org.alfresco")
        artifact_id: Maven artifact ID (e.g., "alfresco-platform")
        archive_bounds: Dict for artifact_server logic
        repos: Dict with structure {
                 "archive": {"release": url, "staging": url, "snapshot": url},
                 "cloudsmith": {"release": url, "staging": url, "snapshot": url}
               }
        ext: File extension (default "jar")

    Returns:
        Dict with keys: "server", "maturity", "repo_url", "url", "checksum_url"

    Raises:
        AnsibleFilterError: If repos lacks the selected server or maturity
    """
    # Determine maturity based on version suffix
    maturity = get_artifact_maturity(version)

    # Determine which server to use
    server = get_artifact_server(version, archive_bounds)

    # Validate repos structure
    try:
        repo_url = repos[server][maturity]
    except KeyError as e:
        raise AnsibleFilterError(
            f"repos missing key: {e}. Expected repos['{server}']['{maturity}']"
        )

    # Ensure repo_url does not end with slash (caller may add trailing slash)
    repo_url = repo_url.rstrip("/")

    # Build artifact URL
    group_path = group_id.replace(".", "/")
    url = f"{repo_url}/{group_path}/{artifact_id}/{version}/{artifact_id}-{version}.{ext}"
    checksum_url = f"{url}.sha1"

    return {
        "server": server,
        "maturity": maturity,
        "repo_url": repo_url,
        "url": url,
        "checksum_url": checksum_url,
    }


class FilterModule:
    """FilterModule for maven_artifact filter."""

    def filters(self):
        """Return filter functions."""
        return {
            "maven_artifact": maven_artifact,
        }
