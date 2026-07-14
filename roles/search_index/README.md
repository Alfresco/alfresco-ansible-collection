# search_index

Install and configure the Alfresco Elasticsearch Batch Indexing service.

Batch Indexing is a Spring Boot service (shipped with ACS 26.2) that continuously
indexes Alfresco content into Elasticsearch by polling the repository database and
retrieving content over HTTP from ACS. It does **not** require ActiveMQ.

This role refuses to run on ACS versions earlier than 26.2.

## Requirements

For this role to function as intended, the following prerequisites must be met:

* An **Elasticsearch instance** must be running and accessible by the target host
  for both read & **write** index operations.
* The **ACS repository database** must be reachable from the target host so the
  service can read node metadata.
* A running **ACS 26.2+ repository** reachable at `search_index_acs_url` so content
  can be retrieved and transformed.
* Access to [Alfresco's artifacts repository](https://artifacts.alfresco.com/nexus)
  (or another artifact repository) to pull the Batch Indexing distribution from.

## Dependencies

This role requires an openjdk installation to be present on the target system and
provided as `search_index_java_home_path`.

The role `alfresco.platform.java` is recommended to install the openjdk.

You also need a user and group created on the host.

## Example Playbook

```yaml
- name: Converge Batch Indexing Hosts
  hosts: search_index
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
        java_version: 17.0.18+8

    - name: Include main role
      ansible.builtin.include_role:
        name: alfresco.platform.search_index
      vars:
        search_index_acs_version: "26.2.0"
        search_index_java_home_path: "/opt/openjdk-17.0.18"
        search_index_nexus_username: "{{ lookup('env', 'NEXUS_USERNAME') }}"
        search_index_nexus_password: "{{ lookup('env', 'NEXUS_PASSWORD') }}"
        search_index_username: "{{ username }}"
        search_index_group_name: "{{ group_name }}"
        search_index_elasticsearch_url: http://elasticsearch:9200
        search_index_elasticsearch_username: admin
        search_index_elasticsearch_password: admin
        search_index_db_url: jdbc:postgresql://postgres:5432/alfresco
        search_index_db_username: alfresco
        search_index_db_password: alfresco
        search_index_acs_url: http://alfresco:8080
        search_index_content_transform_shared_secret: mysecret
```

Continuous-reindexing behaviour can be tuned by adding the corresponding Spring Boot
environment variables (e.g. `ALFRESCO_REINDEX_CONTINUOUS_POLLINGINTERVAL`) via
`search_index_environment`.

> **Note:** While this component can be installed independently, an operational
> **Alfresco Content Services (ACS) 26.2+ instance** is required for it to function
> meaningfully. Without ACS and its populated database, no content will be indexed.

## License

Apache-2.0

## Author

Alfresco Ops Readiness
