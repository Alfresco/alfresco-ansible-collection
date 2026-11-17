# Collections Plugins Directory

This directory contains plugins for the alfresco.platform collection.

## Filters

This collection provides the following filters:

- **`artifact_server`** - Determine which server (archive or cloudsmith) should host an artifact based on version and bounds.
- **`maven_artifact`** - Build a Maven artifact descriptor with server, URL, and checksum URL information.

For detailed documentation, parameter information, and additional examples, please refer to the [generated collection documentation](https://alfresco.github.io/alfresco-ansible-collection/).

### Quick Examples

**artifact_server filter:**

```yaml
- name: Set artifact server
  ansible.builtin.set_fact:
    server: "{{ acs_version | alfresco.platform.artifact_server({7: '7.3.9'}) }}"
```

**maven_artifact filter:**

```yaml
- name: Get artifact descriptor
  ansible.builtin.set_fact:
    artifact: "{{ acs_version | alfresco.platform.maven_artifact('org.alfresco', 'alfresco-platform', {7: '7.3.9'}, repos) }}"
  vars:
    repos:
      archive:
        release: "https://artifacts.alfresco.com/nexus/release"
        staging: "https://artifacts.alfresco.com/nexus/staging"
        snapshot: "https://artifacts.alfresco.com/nexus/snapshot"
      cloudsmith:
        release: "https://dl.cloudsmith.io/release"
        staging: "https://dl.cloudsmith.io/staging"
        snapshot: "https://dl.cloudsmith.io/snapshot"
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
