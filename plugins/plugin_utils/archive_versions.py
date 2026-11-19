"""Last version of each release line published on the archive server (Nexus), per component."""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

# Nexus no longer receives releases, so these values are final.
ARCHIVE_LAST_VERSIONS = {
    "repository": ["6.2.2.25", "7.4.2.6", "23.7.3", "25.5.2", "26.2.4"],
    "community_repository": ["6.1.1", "7.4.2", "23.4.1", "25.3.0", "26.2.0"],
    "api_explorer": ["1.4", "5.2.4", "6.3.0", "7.4.0", "23.7.0", "25.5.0", "26.2.0"],
    "amp_googledrive_repo": ["3.4.2", "4.1.1", "5.0.0"],
    "community_amp_googledrive_repo": ["3.4.2", "4.1.1", "5.0.0"],
    "amp_googledrive_share": ["3.4.2", "4.1.1", "5.0.0"],
    "amp_device_sync": ["2.2.3", "3.11.3", "4.0.1", "5.3.7"],
    "amp_aos_module": ["1.6.3", "2.0.1", "3.4.3"],
    "transformers_aio": ["2.6.0", "3.1.2", "4.0.1", "5.4.5"],
    "transformers_pdf": ["0.10", "1.3.0-86"],
    "trouter": ["0.5.2", "1.5.3", "2.1.2", "3.0.1", "4.4.5"],
    "sfs": ["0.16.1", "1.5.3", "2.1.2", "3.0.1", "4.4.5"],
    "search": ["1.4.3.4", "2.0.23"],
    "search_enterprise": ["0.0.4", "3.3.3", "4.2.0", "5.9.0"],
    "search_community": ["5.9.0"],
    "acc": ["8.4.0", "10.5.0", "11.0.0"],
    "adw": ["1.6", "2.9.1", "3.1.1", "4.4.1", "5.3.0", "6.0.0", "7.5.0", "8.0.0"],
    "sync": ["3.11.3", "4.0.1", "5.3.7"],
    "audit_storage": ["0.0.11", "1.3.5"],
    "cic_connector": ["1.0.3"],
    # TODO: placeholders from the alfresco-devops-ansible molecule pins, replace with the last Nexus versions.
    "aps_app": ["2.4.8", "24.6.0", "25.3.0"],
    "aps_admin": ["2.4.8", "24.6.0", "25.3.0"],
}
