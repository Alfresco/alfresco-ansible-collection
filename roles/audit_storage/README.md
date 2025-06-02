# audit_storage

Install and configure Alfresco Audit Storage

## Requirements

For this role to function as intended, the following prerequisites must be met:

* An **ActiveMQ instance** must be running and accessible by the target host
  where the audit storage service will be deployed.
* An **Elasticsearch (or OpenSearch) instance** must be running and accessible
  by the target host for both read & **write** index operations.
* Access to [Alfresco's artifacts repository](https://nexus.alfresco.com/nexus)
  (or other artifact repository) to pull Alfresco Audit Storage application artifacts from.

## Dependencies

This role requires an openjdk installation to be present on the target system
and provided as `audit_storage_java_home_path` variable.

The role `alfresco.platform.java` is recommended to install the openjdk.

You also need user and group created on host

## Example Playbook

```yaml
- name: Converge Audit Storage Hosts
  hosts: audit_storage
  vars:
    username: alfresco
    group_name: alfresco
  tasks:
    - name: Add an application group
      become: true
      ansible.builtin.group:
        name: "{{ group_name }}"
        system: true

    - name: Add an application user
      become: true
      ansible.builtin.user:
        name: "{{ username }}"
        system: true
        group: "{{ group_name }}"

    - name: Include java role
      ansible.builtin.include_role:
        name: alfresco.platform.java
      vars:
        java_version: 17.0.14+7

    - name: Include main role
      ansible.builtin.include_role:
        name: alfresco.platform.audit_storage
      vars:
        audit_storage_java_home_path: "/opt/openjdk-17.0.14"
        audit_storage_nexus_username: "{{ lookup('env', 'NEXUS_USERNAME') }}"
        audit_storage_nexus_password: "{{ lookup('env', 'NEXUS_PASSWORD') }}"
        audit_storage_username: "{{ username }}"
        audit_storage_group_name: "{{ group_name }}"
        audit_storage_broker_url: failover:(tcp://activemq:61616)
        audit_storage_broker_username: admin
        audit_storage_broker_password: admin
        audit_storage_opensearch_url: http://elasticsearch:9200
        audit_storage_opensearch_username: admin
        audit_storage_opensearch_password: admin

```

> **Note:** While this component can run independently, an operational
> **Alfresco Content Services (ACS) instance** is required for it to function
> meaningfully. Without ACS, no audit events will be produced, and therefore
> nothing will be indexed into the Elasticsearch instance.

## License

Apache-2.0

## Author

Alfresco Ops Readiness
