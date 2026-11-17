"""Tests for artifact filters."""

import pytest
from ansible.errors import AnsibleFilterError

from ansible_collections.alfresco.platform.plugins.filter.artifact_server import (
    artifact_server,
)
from ansible_collections.alfresco.platform.plugins.filter.maven_artifact import (
    maven_artifact,
)


class TestArtifactServer:
    """Test artifact_server filter."""

    def test_version_at_bound(self):
        """Test version exactly at the bound."""
        assert artifact_server("7.3.9", {7: "7.3.9"}) == "archive"

    def test_version_below_bound(self):
        """Test version below the bound."""
        assert artifact_server("7.3.5", {7: "7.3.9"}) == "archive"

    def test_version_above_bound(self):
        """Test version above the bound."""
        assert artifact_server("7.4.0", {7: "7.3.9"}) == "cloudsmith"

    def test_unknown_major_version(self):
        """Test unknown major version goes to cloudsmith."""
        assert artifact_server("8.0.0", {7: "7.3.9"}) == "cloudsmith"

    def test_empty_bounds(self):
        """Test empty bounds defaults to cloudsmith."""
        assert artifact_server("7.3.0", {}) == "cloudsmith"

    def test_none_bounds(self):
        """Test None bounds defaults to cloudsmith."""
        assert artifact_server("7.3.0", None) == "cloudsmith"

    def test_snapshot_version_at_bound(self):
        """Test SNAPSHOT version at bound is treated as above bound."""
        assert artifact_server("7.3.9-SNAPSHOT", {7: "7.3.9"}) == "cloudsmith"

    def test_snapshot_version_below_bound(self):
        """Test SNAPSHOT version below bound."""
        assert artifact_server("7.3.0-SNAPSHOT", {7: "7.3.9"}) == "archive"

    def test_staging_version_at_bound(self):
        """Test staging version at bound is treated as above bound."""
        assert artifact_server("7.3.9-RC1", {7: "7.3.9"}) == "cloudsmith"

    def test_staging_version_below_bound(self):
        """Test staging version below bound."""
        assert artifact_server("7.3.0-RC1", {7: "7.3.9"}) == "archive"

    def test_multiple_majors_in_bounds(self):
        """Test bounds with multiple major versions."""
        bounds = {6: "6.2.1", 7: "7.3.9"}
        assert artifact_server("6.2.0", bounds) == "archive"
        assert artifact_server("6.3.0", bounds) == "cloudsmith"
        assert artifact_server("7.3.0", bounds) == "archive"
        assert artifact_server("7.4.0", bounds) == "cloudsmith"
        assert artifact_server("8.0.0", bounds) == "cloudsmith"

    def test_string_bounds_keys(self):
        """Test bounds with string keys (from JSON or extra-vars)."""
        # String keys should be normalized to integers
        bounds_str = {"7": "7.3.9", "6": "6.2.1"}
        assert artifact_server("7.3.0", bounds_str) == "archive"
        assert artifact_server("7.4.0", bounds_str) == "cloudsmith"
        assert artifact_server("6.2.0", bounds_str) == "archive"
        assert artifact_server("6.3.0", bounds_str) == "cloudsmith"


class TestMavenArtifact:
    """Test maven_artifact filter."""

    @pytest.fixture
    def repos(self):
        """Fixture for repos structure."""
        return {
            "archive": {
                "release": "https://artifacts.alfresco.com/nexus/release",
                "staging": "https://artifacts.alfresco.com/nexus/staging",
                "snapshot": "https://artifacts.alfresco.com/nexus/snapshot",
            },
            "cloudsmith": {
                "release": "https://dl.cloudsmith.io/release",
                "staging": "https://dl.cloudsmith.io/staging",
                "snapshot": "https://dl.cloudsmith.io/snapshot",
            },
        }

    def test_release_version_archive(self, repos):
        """Test release version on archive server."""
        result = maven_artifact(
            "7.3.0",
            "org.alfresco",
            "alfresco-platform",
            {7: "7.3.9"},
            repos,
        )
        assert result["server"] == "archive"
        assert result["maturity"] == "release"
        assert result["repo_url"] == "https://artifacts.alfresco.com/nexus/release"
        assert (
            result["url"]
            == "https://artifacts.alfresco.com/nexus/release/org/alfresco/alfresco-platform/7.3.0/alfresco-platform-7.3.0.jar"
        )
        assert result["checksum_url"] == result["url"] + ".sha1"

    def test_release_version_cloudsmith(self, repos):
        """Test release version on cloudsmith server."""
        result = maven_artifact(
            "7.4.0",
            "org.alfresco",
            "alfresco-platform",
            {7: "7.3.9"},
            repos,
        )
        assert result["server"] == "cloudsmith"
        assert result["maturity"] == "release"
        assert result["repo_url"] == "https://dl.cloudsmith.io/release"
        assert (
            result["url"]
            == "https://dl.cloudsmith.io/release/org/alfresco/alfresco-platform/7.4.0/alfresco-platform-7.4.0.jar"
        )

    def test_snapshot_version(self, repos):
        """Test snapshot version."""
        result = maven_artifact(
            "7.3.0-SNAPSHOT",
            "org.alfresco",
            "alfresco-platform",
            {7: "7.3.9"},
            repos,
        )
        assert result["maturity"] == "snapshot"
        assert result["server"] == "archive"
        assert (
            result["url"]
            == "https://artifacts.alfresco.com/nexus/snapshot/org/alfresco/alfresco-platform/7.3.0-SNAPSHOT/alfresco-platform-7.3.0-SNAPSHOT.jar"
        )

    def test_staging_version(self, repos):
        """Test staging version."""
        result = maven_artifact(
            "7.3.0-RC1",
            "org.alfresco",
            "alfresco-platform",
            {7: "7.3.9"},
            repos,
        )
        assert result["maturity"] == "staging"
        assert result["server"] == "archive"

    def test_dotted_group_id(self, repos):
        """Test dotted group ID conversion to path."""
        result = maven_artifact(
            "7.3.0",
            "com.example.org.alfresco",
            "my-artifact",
            {7: "7.3.9"},
            repos,
        )
        assert (
            result["url"]
            == "https://artifacts.alfresco.com/nexus/release/com/example/org/alfresco/my-artifact/7.3.0/my-artifact-7.3.0.jar"
        )

    def test_custom_extension(self, repos):
        """Test custom file extension."""
        result = maven_artifact(
            "7.3.0",
            "org.alfresco",
            "alfresco-platform",
            {7: "7.3.9"},
            repos,
            ext="zip",
        )
        assert result["url"].endswith(".zip")
        assert result["checksum_url"].endswith(".zip.sha1")

    def test_missing_server_key(self, repos):
        """Test missing server in repos raises error."""
        incomplete_repos = {
            "archive": {
                "release": "https://artifacts.alfresco.com/nexus/release",
                "staging": "https://artifacts.alfresco.com/nexus/staging",
                "snapshot": "https://artifacts.alfresco.com/nexus/snapshot",
            }
        }
        with pytest.raises(AnsibleFilterError, match="repos missing key"):
            maven_artifact(
                "7.4.0",
                "org.alfresco",
                "alfresco-platform",
                {7: "7.3.9"},
                incomplete_repos,
            )

    def test_missing_maturity_key(self, repos):
        """Test missing maturity in repos raises error."""
        incomplete_repos = {
            "archive": {
                "release": "https://artifacts.alfresco.com/nexus/release",
                "staging": "https://artifacts.alfresco.com/nexus/staging",
            },
            "cloudsmith": {
                "release": "https://dl.cloudsmith.io/release",
                "staging": "https://dl.cloudsmith.io/staging",
                "snapshot": "https://dl.cloudsmith.io/snapshot",
            },
        }
        with pytest.raises(AnsibleFilterError, match="repos missing key"):
            maven_artifact(
                "7.3.0-SNAPSHOT",
                "org.alfresco",
                "alfresco-platform",
                {7: "7.3.9"},
                incomplete_repos,
            )

    def test_all_maturity_types_on_both_servers(self, repos):
        """Test all maturity types work on both servers."""
        archive_bounds = {7: "7.3.9"}

        # Archive server - all maturities
        for version, expected_maturity in [
            ("7.3.0", "release"),
            ("7.3.0-RC1", "staging"),
            ("7.3.0-SNAPSHOT", "snapshot"),
        ]:
            result = maven_artifact(
                version,
                "org.alfresco",
                "alfresco-platform",
                archive_bounds,
                repos,
            )
            assert result["server"] == "archive"
            assert result["maturity"] == expected_maturity

        # Cloudsmith server - all maturities
        for version, expected_maturity in [
            ("7.4.0", "release"),
            ("7.4.0-RC1", "staging"),
            ("7.4.0-SNAPSHOT", "snapshot"),
        ]:
            result = maven_artifact(
                version,
                "org.alfresco",
                "alfresco-platform",
                archive_bounds,
                repos,
            )
            assert result["server"] == "cloudsmith"
            assert result["maturity"] == expected_maturity

    def test_repo_url_trailing_slash_stripped(self, repos):
        """Test that trailing slashes in repo_url are stripped."""
        repos_with_slash = {
            "archive": {
                "release": "https://artifacts.alfresco.com/nexus/release/",
                "staging": "https://artifacts.alfresco.com/nexus/staging/",
                "snapshot": "https://artifacts.alfresco.com/nexus/snapshot/",
            },
            "cloudsmith": {
                "release": "https://dl.cloudsmith.io/release/",
                "staging": "https://dl.cloudsmith.io/staging/",
                "snapshot": "https://dl.cloudsmith.io/snapshot/",
            },
        }
        result = maven_artifact(
            "7.3.0",
            "org.alfresco",
            "alfresco-platform",
            {7: "7.3.9"},
            repos_with_slash,
        )
        # Should not have double slashes
        assert "//" not in result["url"].replace("https://", "")
        assert (
            result["url"]
            == "https://artifacts.alfresco.com/nexus/release/org/alfresco/alfresco-platform/7.3.0/alfresco-platform-7.3.0.jar"
        )
