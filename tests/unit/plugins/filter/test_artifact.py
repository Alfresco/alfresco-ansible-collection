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
        pytest.param("26.3.0-M1", "aps_app", "archive", id="shipped-aps-last-milestone"),
        pytest.param("26.3.0", "aps_app", "cloudsmith", id="shipped-aps-after-last-milestone"),
        pytest.param("26.3.0-M2", "aps_app", "cloudsmith", id="shipped-aps-later-milestone"),
        pytest.param("1.3.0-90", "transformers_pdf", "cloudsmith", id="shipped-build-number-above"),
    ],
)
def test_artifact_server(version, component, expected):
    assert artifact_server(version, component) == expected


@pytest.mark.parametrize(
    "component, match",
    [
        pytest.param(["7.x"], "7.x", id="uncomparable-bound"),
        pytest.param({7: "7.3.9"}, "list", id="dict-bounds"),
        pytest.param({}, "list", id="empty-dict-bounds"),
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


COORDS = {"group_id": "org.alfresco", "artifact_id": "alfresco-platform"}


def test_artifact_url(repos):
    url = "https://nexus.example/releases/org/alfresco/alfresco-platform/7.3.0/alfresco-platform-7.3.0.jar"
    assert artifact_url("7.3.0", BOUNDS, repos=repos, **COORDS) == {
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
    result = artifact_url(version, BOUNDS, repos=repos, **COORDS)
    assert (result["server"], result["maturity"]) == (server, maturity)
    assert result["repo_url"] == repos[server][maturity]


def test_artifact_url_release_build_number(repos):
    result = artifact_url("1.3.0-86", "transformers_pdf", repos=repos, **COORDS)
    assert (result["server"], result["maturity"]) == ("archive", "release")
    assert result["repo_url"] == repos["archive"]["release"]


def test_artifact_url_layout(repos):
    repos["archive"]["release"] += "/"
    result = artifact_url(24.4, ["24.4.1"], repos=repos, group_id="com.example.org", artifact_id="my-artifact", ext="war")
    assert result["url"] == "https://nexus.example/releases/com/example/org/my-artifact/24.4/my-artifact-24.4.war"


@pytest.mark.parametrize(
    "version, url",
    [
        pytest.param(
            "24.6.0",
            "https://artifacts.alfresco.com/nexus/repository/activiti-enterprise-releases"
            "/com/activiti/activiti-app/24.6.0/activiti-app-24.6.0.war",
            id="nexus-release",
        ),
        pytest.param(
            "26.4.0",
            "https://artifacts.hyland.dev/basic/alfresco-private/maven"
            "/com/activiti/activiti-app/26.4.0/activiti-app-26.4.0.war",
            id="cloudsmith-release",
        ),
        pytest.param(
            "26.4.0-RC1",
            "https://artifacts.hyland.dev/basic/alfresco-internal/maven"
            "/com/activiti/activiti-app/26.4.0-RC1/activiti-app-26.4.0-RC1.war",
            id="cloudsmith-staging",
        ),
    ],
)
def test_artifact_url_shipped_component(version, url):
    assert artifact_url(version, "aps_app")["url"] == url


def test_artifact_url_overrides_shipped_values(repos):
    result = artifact_url("24.6.0", "aps_admin", repos=repos, ext="zip")
    assert result["url"] == "https://nexus.example/releases/com/activiti/activiti-admin/24.6.0/activiti-admin-24.6.0.zip"


@pytest.mark.parametrize(
    "component, match",
    [
        pytest.param("repository", "group_id", id="shipped-without-coordinates"),
        pytest.param(BOUNDS, "repos", id="explicit-bounds-without-repos"),
        pytest.param("aps_ap", "aps_ap", id="unknown-component"),
    ],
)
def test_artifact_url_missing_metadata_raises(component, match):
    with pytest.raises(AnsibleFilterError, match=match):
        artifact_url("7.4.0", component)


def test_artifact_url_snapshot_raises():
    with pytest.raises(AnsibleFilterError, match="SNAPSHOT"):
        artifact_url("26.1.0-SNAPSHOT", "aps_app")


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
        artifact_url(version, BOUNDS, repos=repos, **COORDS)
