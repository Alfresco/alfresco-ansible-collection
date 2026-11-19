"""Tests for artifact filters."""

import pytest
from ansible.errors import AnsibleFilterError

from ansible_collections.alfresco.platform.plugins.filter.artifact_server import (
    artifact_server,
)
from ansible_collections.alfresco.platform.plugins.filter.artifact_url import (
    artifact_url,
)

BOUNDS = ["6.2.1", "7.3.9"]


class TestArtifactServer:
    @pytest.mark.parametrize(
        "version, expected",
        [
            ("7.3.9", "archive"),
            ("7.3.5", "archive"),
            ("7.4.0", "cloudsmith"),
            ("6.2.0", "archive"),
            ("6.3.0", "cloudsmith"),
            ("8.0.0", "cloudsmith"),
        ],
    )
    def test_release_versions(self, version, expected):
        assert artifact_server(version, BOUNDS) == expected

    @pytest.mark.parametrize("bounds", [[], None])
    def test_no_bounds(self, bounds):
        assert artifact_server("7.3.0", bounds) == "cloudsmith"

    @pytest.mark.parametrize(
        "version, expected",
        [
            ("7.3.9-RC1", "archive"),
            ("7.3.9-SNAPSHOT", "archive"),
            ("7.3.0-A1", "archive"),
            ("7.4.0-RC1", "cloudsmith"),
            ("7.4.0-SNAPSHOT", "cloudsmith"),
        ],
    )
    def test_pre_release_follows_base_version(self, version, expected):
        assert artifact_server(version, BOUNDS) == expected

    def test_float_version(self):
        assert artifact_server(7.3, BOUNDS) == "archive"

    def test_float_bound(self):
        assert artifact_server("7.2.0", [7.3]) == "archive"
        assert artifact_server("7.4.0", [7.3]) == "cloudsmith"

    def test_uncomparable_bound_raises(self):
        with pytest.raises(AnsibleFilterError, match="7.x"):
            artifact_server("7.3.0", ["7.x"])

    def test_dict_bounds_raises(self):
        with pytest.raises(AnsibleFilterError, match="list"):
            artifact_server("7.3.0", {7: "7.3.9"})


class TestArtifactUrl:
    @pytest.fixture
    def repos(self):
        return {
            "archive": {
                "release": "https://nexus.example/releases",
                "staging": "https://nexus.example/staging",
            },
            "cloudsmith": {
                "release": "https://cloudsmith.example/private/maven",
                "staging": "https://cloudsmith.example/internal/maven",
            },
        }

    def test_release_on_archive(self, repos):
        result = artifact_url("7.3.0", "org.alfresco", "alfresco-platform", BOUNDS, repos)
        url = "https://nexus.example/releases/org/alfresco/alfresco-platform/7.3.0/alfresco-platform-7.3.0.jar"
        assert result == {
            "server": "archive",
            "maturity": "release",
            "repo_url": "https://nexus.example/releases",
            "url": url,
            "checksum_url": url + ".sha1",
        }

    def test_release_on_cloudsmith(self, repos):
        result = artifact_url("7.4.0", "org.alfresco", "alfresco-platform", BOUNDS, repos)
        assert result["server"] == "cloudsmith"
        assert result["maturity"] == "release"
        assert result["url"] == (
            "https://cloudsmith.example/private/maven/org/alfresco/alfresco-platform/7.4.0/alfresco-platform-7.4.0.jar"
        )

    @pytest.mark.parametrize(
        "version, server", [("7.3.9-RC1", "archive"), ("7.4.0-RC1", "cloudsmith")]
    )
    def test_pre_release_uses_staging(self, repos, version, server):
        result = artifact_url(version, "org.alfresco", "alfresco-platform", BOUNDS, repos)
        assert result["server"] == server
        assert result["maturity"] == "staging"
        assert result["repo_url"] == repos[server]["staging"]

    def test_snapshot_raises(self, repos):
        with pytest.raises(AnsibleFilterError, match="SNAPSHOT"):
            artifact_url("7.4.0-SNAPSHOT", "org.alfresco", "alfresco-platform", BOUNDS, repos)

    def test_float_version(self, repos):
        result = artifact_url(24.4, "com.activiti", "activiti-app", ["24.4.1"], repos, ext="war")
        assert result["url"].endswith("/com/activiti/activiti-app/24.4/activiti-app-24.4.war")

    def test_dotted_group_id_and_ext(self, repos):
        result = artifact_url(
            "7.3.0", "com.example.org", "my-artifact", BOUNDS, repos, ext="zip"
        )
        assert result["url"] == (
            "https://nexus.example/releases/com/example/org/my-artifact/7.3.0/my-artifact-7.3.0.zip"
        )
        assert result["checksum_url"].endswith(".zip.sha1")

    def test_trailing_slash_stripped(self, repos):
        repos["archive"]["release"] += "/"
        result = artifact_url("7.3.0", "org.alfresco", "alfresco-platform", BOUNDS, repos)
        assert result["url"].startswith("https://nexus.example/releases/org/")

    def test_missing_server_raises(self, repos):
        del repos["cloudsmith"]
        with pytest.raises(AnsibleFilterError, match="cloudsmith"):
            artifact_url("7.4.0", "org.alfresco", "alfresco-platform", BOUNDS, repos)

    def test_missing_maturity_raises(self, repos):
        del repos["archive"]["staging"]
        with pytest.raises(AnsibleFilterError, match="staging"):
            artifact_url("7.3.0-RC1", "org.alfresco", "alfresco-platform", BOUNDS, repos)
