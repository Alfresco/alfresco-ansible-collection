"""Tests for artifact filters."""

import pytest
from ansible.errors import AnsibleFilterError

from ansible_collections.alfresco.platform.plugins.filter import artifact_server as server_module
from ansible_collections.alfresco.platform.plugins.filter import artifact_url as url_module

artifact_server = server_module.FilterModule().filters()["artifact_server"]
artifact_url = url_module.FilterModule().filters()["artifact_url"]

BOUNDS = ["6.2.1", "7.3.9"]


@pytest.mark.parametrize(
    "version, component, expected",
    [
        pytest.param("7.3.9", BOUNDS, "archive", id="at-bound"),
        pytest.param("7.3.5", BOUNDS, "archive", id="below-bound"),
        pytest.param("7.4.0", BOUNDS, "cloudsmith", id="above-bound"),
        pytest.param("6.2.0", BOUNDS, "archive", id="other-major-below"),
        pytest.param("6.3.0", BOUNDS, "cloudsmith", id="other-major-above"),
        pytest.param("8.0.0", BOUNDS, "cloudsmith", id="unknown-major"),
        pytest.param("7.3.0", [], "cloudsmith", id="empty-bounds"),
        pytest.param("7.3.0", None, "cloudsmith", id="no-bounds"),
        pytest.param("7.3.9-RC1", BOUNDS, "archive", id="pre-release-at-bound"),
        pytest.param("7.3.9-SNAPSHOT", BOUNDS, "archive", id="snapshot-at-bound"),
        pytest.param("7.3.0-A1", BOUNDS, "archive", id="pre-release-below"),
        pytest.param("7.4.0-RC1", BOUNDS, "cloudsmith", id="pre-release-above"),
        pytest.param("7.4.0-SNAPSHOT", BOUNDS, "cloudsmith", id="snapshot-above"),
        pytest.param(7.3, BOUNDS, "archive", id="float-version"),
        pytest.param("7.2.0", [7.3], "archive", id="float-bound-below"),
        pytest.param("7.4.0", [7.3], "cloudsmith", id="float-bound-above"),
        pytest.param("1.3.0-86", ["1.3.0-86"], "archive", id="build-number-at-bound"),
        pytest.param("1.3.0-90", ["1.3.0-86"], "cloudsmith", id="build-number-above"),
        pytest.param("1.2.0", ["1.3.0-86"], "archive", id="build-number-bound-below"),
        pytest.param("7.4.2.6", "repository", "archive", id="shipped-at-bound"),
        pytest.param("7.4.3", "repository", "cloudsmith", id="shipped-above"),
        pytest.param("23.4.1", "community_repository", "archive", id="shipped-other-component"),
        pytest.param("1.3.0-86", "transformers_pdf", "archive", id="shipped-build-number"),
        pytest.param("27.1.0", "repository", "cloudsmith", id="shipped-unknown-major"),
    ],
)
def test_artifact_server(version, component, expected):
    assert artifact_server(version, component) == expected


@pytest.mark.parametrize(
    "component, match",
    [
        pytest.param(["7.x"], "7.x", id="uncomparable-bound"),
        pytest.param({7: "7.3.9"}, "list", id="dict-bounds"),
        pytest.param("repositroy", "repositroy", id="unknown-component"),
    ],
)
def test_artifact_server_invalid_component(component, match):
    with pytest.raises(AnsibleFilterError, match=match):
        artifact_server("7.3.0", component)


@pytest.fixture
def repos():
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


def test_artifact_url(repos):
    url = "https://nexus.example/releases/org/alfresco/alfresco-platform/7.3.0/alfresco-platform-7.3.0.jar"
    assert artifact_url("7.3.0", "org.alfresco", "alfresco-platform", BOUNDS, repos) == {
        "server": "archive",
        "maturity": "release",
        "repo_url": "https://nexus.example/releases",
        "url": url,
        "checksum_url": url + ".sha1",
    }


@pytest.mark.parametrize(
    "version, server, maturity",
    [
        ("7.4.0", "cloudsmith", "release"),
        ("7.3.9-RC1", "archive", "staging"),
        ("7.4.0-RC1", "cloudsmith", "staging"),
    ],
)
def test_artifact_url_repo_selection(repos, version, server, maturity):
    result = artifact_url(version, "org.alfresco", "alfresco-platform", BOUNDS, repos)
    assert (result["server"], result["maturity"]) == (server, maturity)
    assert result["repo_url"] == repos[server][maturity]


def test_artifact_url_layout(repos):
    repos["archive"]["release"] += "/"
    result = artifact_url(24.4, "com.example.org", "my-artifact", ["24.4.1"], repos, ext="war")
    assert result["url"] == "https://nexus.example/releases/com/example/org/my-artifact/24.4/my-artifact-24.4.war"


def test_artifact_url_snapshot_raises(repos):
    with pytest.raises(AnsibleFilterError, match="SNAPSHOT"):
        artifact_url("7.4.0-SNAPSHOT", "org.alfresco", "alfresco-platform", BOUNDS, repos)


@pytest.mark.parametrize(
    "server, maturity, version",
    [("cloudsmith", None, "7.4.0"), ("archive", "staging", "7.3.0-RC1")],
)
def test_artifact_url_missing_repo_raises(repos, server, maturity, version):
    if maturity:
        del repos[server][maturity]
    else:
        del repos[server]
    with pytest.raises(AnsibleFilterError, match=maturity or server):
        artifact_url(version, "org.alfresco", "alfresco-platform", BOUNDS, repos)
