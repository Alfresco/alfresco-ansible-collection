# Collections Plugins Directory

This directory contains plugins for the alfresco.platform collection.

## Filters

- **`artifact_server`** returns `archive` (Nexus) or `cloudsmith` for an artifact version, based on the last version published on Nexus for each major version. The collection ships those versions for each component in [`plugin_utils/components.py`](plugin_utils/components.py), so callers pass a component name. An explicit list of versions also works.
- **`artifact_url`** builds the download and checksum URLs of a Maven artifact on the server `artifact_server` picks. It returns the selected `server` too, so the caller can pick matching credentials. For components that ship their Maven coordinates and repositories (APS so far), the component name is enough: `aps_version | alfresco.platform.artifact_url('aps_app')`. Callers can override any shipped value, for example `repos` to use a mirror. `-SNAPSHOT` versions are not supported.

See the [collection documentation](https://alfresco.github.io/alfresco-ansible-collection/) for all options.

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
