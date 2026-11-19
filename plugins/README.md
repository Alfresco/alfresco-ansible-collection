# Collections Plugins Directory

This directory contains plugins for the alfresco.platform collection.

## Filters

- **`artifact_server`** returns `archive` (Nexus) or `cloudsmith` for an artifact version, based on the last version published on Nexus for each major version. The collection ships those versions for each component in [`plugin_utils/archive_versions.py`](plugin_utils/archive_versions.py), so callers pass a component name. An explicit list of versions also works.
- **`artifact_url`** builds the download and checksum URLs of a Maven artifact on the server `artifact_server` picks. It returns the selected `server` too, so the caller can pick matching credentials. `-SNAPSHOT` versions are not supported.

See the [collection documentation](https://alfresco.github.io/alfresco-ansible-collection/) for all options.

```yaml
- name: Pick the server hosting the requested version
  ansible.builtin.set_fact:
    server: "{{ acs_version | alfresco.platform.artifact_server('repository') }}"

- name: Build the APS war URL
  ansible.builtin.set_fact:
    aps_artifact: "{{ aps_version | alfresco.platform.artifact_url('com.activiti', 'activiti-app', 'aps_app', repos, ext='war') }}"
  vars:
    repos:
      archive:
        release: https://artifacts.alfresco.com/nexus/repository/activiti-enterprise-releases
        staging: https://artifacts.alfresco.com/nexus/repository/activiti-enterprise-staging
      cloudsmith:
        release: https://artifacts.hyland.dev/basic/alfresco-private/maven
        staging: https://artifacts.hyland.dev/basic/alfresco-internal/maven
```

## Standard Plugin Directory Structure

This directory can contain various plugin types. Here is the standard directory layout:

```sh
└── plugins
    ├── action
    ├── become
    ├── cache
    ├── callback
    ├── cliconf
    ├── connection
    ├── filter
    ├── httpapi
    ├── inventory
    ├── lookup
    ├── module_utils
    ├── modules
    ├── netconf
    ├── shell
    ├── strategy
    ├── terminal
    ├── test
    └── vars
```

A full list of plugin types can be found at [Working With Plugins](https://docs.ansible.com/ansible-core/2.16/plugins/plugins.html).
