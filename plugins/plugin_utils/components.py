"""Where each Alfresco component is published: Maven coordinates, repositories and last Nexus versions."""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

NEXUS = "https://artifacts.alfresco.com/nexus/repository"
CLOUDSMITH = "https://artifacts.hyland.dev/basic"

APS_REPOS = {
    "archive": {
        "release": NEXUS + "/activiti-enterprise-releases",
        "staging": NEXUS + "/activiti-enterprise-staging",
    },
    "cloudsmith": {
        "release": CLOUDSMITH + "/activiti-enterprise-releases/maven",
        "staging": CLOUDSMITH + "/activiti-enterprise-staging/maven",
    },
}

# archive_last_versions: last version of each release line on Nexus. Nexus gets no new releases, so they are final.
# prerelease_separator: what starts a pre-release suffix, "-" by default; None when "-" only carries release build numbers.
# Components without coordinates and repos only support artifact_server for now.
COMPONENTS = {
    "repository": {"archive_last_versions": ["6.2.2.25", "7.4.2.6", "23.7.3", "25.5.2", "26.2.4"]},
    "community_repository": {"archive_last_versions": ["6.1.1", "7.4.2", "23.4.1", "25.3.0", "26.2.0"]},
    "api_explorer": {"archive_last_versions": ["1.4", "5.2.4", "6.3.0", "7.4.0", "23.7.0", "25.5.0", "26.2.0"]},
    "amp_googledrive_repo": {"archive_last_versions": ["3.4.2", "4.1.1", "5.0.0"]},
    "community_amp_googledrive_repo": {"archive_last_versions": ["3.4.2", "4.1.1", "5.0.0"]},
    "amp_googledrive_share": {"archive_last_versions": ["3.4.2", "4.1.1", "5.0.0"]},
    "amp_device_sync": {"archive_last_versions": ["2.2.3", "3.11.3", "4.0.1", "5.3.7"]},
    "amp_aos_module": {"archive_last_versions": ["1.6.3", "2.0.1", "3.4.3"]},
    "transformers_aio": {"archive_last_versions": ["2.6.0", "3.1.2", "4.0.1", "5.4.5"]},
    "transformers_pdf": {"archive_last_versions": ["0.10", "1.3.0-86"], "prerelease_separator": None},
    "trouter": {"archive_last_versions": ["0.5.2", "1.5.3", "2.1.2", "3.0.1", "4.4.5"]},
    "sfs": {"archive_last_versions": ["0.16.1", "1.5.3", "2.1.2", "3.0.1", "4.4.5"]},
    "search": {"archive_last_versions": ["1.4.3.4", "2.0.23"]},
    "search_enterprise": {"archive_last_versions": ["0.0.4", "3.3.3", "4.2.0", "5.9.0"]},
    "search_community": {"archive_last_versions": ["5.9.0"]},
    "acc": {"archive_last_versions": ["8.4.0", "10.5.0", "11.0.0"]},
    "adw": {"archive_last_versions": ["1.6", "2.9.1", "3.1.1", "4.4.1", "5.3.0", "6.0.0", "7.5.0", "8.0.0"]},
    "sync": {"archive_last_versions": ["3.11.3", "4.0.1", "5.3.7"]},
    "audit_storage": {"archive_last_versions": ["0.0.11", "1.3.5"]},
    "cic_connector": {"archive_last_versions": ["1.0.3"]},
    "aps_app": {
        "group_id": "com.activiti",
        "artifact_id": "activiti-app",
        "ext": "war",
        "repos": APS_REPOS,
        "archive_last_versions": ["24.7.1", "25.5.0", "26.3.0-M1"],
    },
    "aps_admin": {
        "group_id": "com.activiti",
        "artifact_id": "activiti-admin",
        "ext": "war",
        "repos": APS_REPOS,
        "archive_last_versions": ["24.7.1", "25.5.0", "26.3.0-M1"],
    },
}
