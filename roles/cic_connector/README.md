# cic_connector

Install and configure the Content Intelligence Connector.

The Content Intelligence Connector replaces the previous Hx Insight Connector.
It ships three services:

* **Live Ingester** - consumes real-time repository events from ActiveMQ and
  ingests documents into Content Intelligence.
* **Bulk Ingester** - reads directly from the Alfresco database to batch
  ingest existing content, publishing events for the Live Ingester to consume.
  Only installed when `cic_connector_alfresco_db_url` is set, and is deployed
  as a `oneshot` systemd service that is not started automatically.
* **Nucleus Sync** - synchronises Alfresco users and groups into Nucleus on a
  schedule.

Unlike the Hx Insight Connector, this connector requires **no ACS repository
extension**: repository events are consumed directly from the
`alfresco.repo.event2` ActiveMQ topic.

## Requirements

None.

## Dependencies

This role requires an openjdk installation to be present on the target system
and provided as `cic_connector_java_bin_path` variable.

The role `alfresco.platform.java` is recommended to install the openjdk.

The connector artifacts are pulled from Alfresco's Nexus `enterprise-releases`
repository, which requires Alfresco Enterprise credentials. Provide them via
`cic_connector_artifact_username` and `cic_connector_artifact_password`.

## Example Playbook

```yaml
- name: Converge Content Intelligence Connector Hosts
  hosts: cic
  tasks:
    - name: Include java role
      ansible.builtin.include_role:
        name: alfresco.platform.java
      vars:
        java_version: 17.0.19+10

    - name: Include main role
      ansible.builtin.include_role:
        name: alfresco.platform.cic_connector
      vars:
        cic_connector_java_bin_path: "/opt/openjdk-17.0.19/bin/java"
        cic_connector_artifact_username: "{{ lookup('env', 'NEXUS_USERNAME') }}"
        cic_connector_artifact_password: "{{ lookup('env', 'NEXUS_PASSWORD') }}"
        cic_connector_remote_ingestion_url: "https://hxinsight.alfresco.com/ingestion"
        cic_connector_remote_token_url: "https://hxinsight.alfresco.com/token"
        cic_connector_remote_client_id: "client-id"
        cic_connector_remote_client_secret: "client-secret"
        cic_connector_remote_environment_key: "environment-key"
        cic_connector_alfresco_base_url: "https://alfresco.example.com"
        cic_connector_alfresco_username: "admin"
        cic_connector_alfresco_password: "admin"
        cic_connector_alfresco_sfs_url: "https://sfs.alfresco.com"
        cic_connector_alfresco_activemq_url: "nio://activemq.alfresco.com:61616"
        cic_connector_service_user: "alfresco"
        cic_connector_application_sourceid: "some-uuid-1234ab"
        cic_connector_nucleus_idp_base_url: "https://idp.nucleus.example.com"
        cic_connector_nucleus_base_url: "https://nucleus.example.com"
        cic_connector_nucleus_system_id: "some-system-id"
        # Set to enable the Bulk Ingester (installed but not started automatically)
        # cic_connector_alfresco_db_url: "jdbc:postgresql://postgres:5432/alfresco"
        # cic_connector_alfresco_db_username: "alfresco"
        # cic_connector_alfresco_db_password: "alfresco"
        # cic_connector_bulk_ingester_node_to_id: 20000000000
```

The Live Ingester's dead-letter queue, redelivery policy, durable event
subscription and transactional JMS behaviour ship with production-safe
defaults and can be tuned via the corresponding `cic_connector_*` variables
(see `meta/argument_specs.yml` for the full list).

More information can be found in the
[Alfresco Content Intelligence Connector](https://github.com/Alfresco/alfresco-cic-connector)
docs.

## License

Apache-2.0

## Author

Alfresco Ops Readiness
