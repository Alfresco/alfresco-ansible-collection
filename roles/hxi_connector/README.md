# hxi_connector

Install and configure Hx Insights Connector

## Requirements

None.

## Dependencies

This role requires an openjdk installation to be present on the target system
and provided as `hxi_connector_java_bin_path` variable.

The role `alfresco.platform.java` is recommended to install the openjdk.

## Example Playbook

```yaml
- name: Converge Hx Insight Hosts
  hosts: hxi
  tasks:
    - name: Include java role
      ansible.builtin.include_role:
        name: alfresco.platform.java
      vars:
        java_version: 17.0.14+7

    - name: Include main role
      ansible.builtin.include_role:
        name: alfresco.platform.hxi_connector
      vars:
        hxi_connector_java_bin_path: "/opt/openjdk-17.0.14/bin/java"
        hxi_connector_remote_ingestion_url: "https://hxinsight.alfresco.com/ingestion"
        hxi_connector_remote_prediction_url: "https://hxinsight.alfresco.com/predictions"
        hxi_connector_remote_token_url: "https://hxinsight.alfresco.com/token"
        hxi_connector_remote_client_id: "client-id"
        hxi_connector_remote_client_secret: "client-secret"
        hxi_connector_remote_environment_key: "environment-key"
        hxi_connector_alfresco_sfs_url: "https://sfs.alfresco.com"
        hxi_connector_alfresco_activemq_url: "nio://activemq.alfresco.com:61616"
        hxi_connector_service_user: "alfresco"
        hxi_connector_application_sourceid: "some-uuid-1234ab"

- name: Converge Alfresco Repository hosts
  hosts: repository
  tasks:
    - name: Include repository-extension
      ansible.builtin.include_role:
        name: alfresco.platform.hxi_connector
        tasks_from: repository-extension
      vars:
        hxi_connector_repository_extension_artifact_path: "/opt/alfresco/content-services-25.1/modules/acs-platform/hxi-repository-extension.jar"
        hxi_connector_repository_extension_properties_snippet_path: "/opt/alfresco/content-services-25.1/modules/acs-platform-config/alfresco/module/alfresco-hxinsight-connector-hxinsight-extension/alfresco-global.properties"
        hxi_connector_alfresco_service_name: "alfresco-content-monitored-startup" # set to empty string to disable automatic restart
        # Uncomment to use an existing custom handler
        # hxi_connector_alfresco_service_existing_handler_name: "Restart alfresco-content"
        hxi_connector_remote_discovery_url: "https://hxinsight.alfresco.com/discovery"
        hxi_connector_remote_client_id: "client-id"
        hxi_connector_remote_client_secret: "client-secret"
        hxi_connector_remote_environment_key: "environment-key"
        hxi_connector_remote_prediction_url: "https://hxinsight.alfresco.com/predictions"
        hxi_connector_remote_token_url: "https://hxinsight.alfresco.com/token"
        hxi_connector_application_sourceid: "some-uuid-1234ab"
```

Please note that the extension configuration leverages the new
`acs-platform-config` folder recently introduced in the upstream Alfresco
Ansible Playbooks. The extension can still be configured manually using the the
main `alfresco-global.properties` file, after setting
`hxi_connector_repository_extension_properties_snippet_path` to empty string.

The following properties are required in the `alfresco-global.properties` file:

```properties
hxi.discovery.base-url=https://example.com
hxi.auth.providers.hyland-experience.token-uri=https://example.com
hxi.auth.providers.hyland-experience.environment-key=
hxi.auth.providers.hyland-experience.client-id=
hxi.auth.providers.hyland-experience.client-secret=
hxi.auth.providers.hyland-experience.grant-type=client_credentials
hxi.knowledge-retrieval.url=https://example.com
hxi.connector.source-id=
```

More information can be found in the official [Alfresco Connector for Content
Intelligence](https://support.hyland.com/p/contentintel) docs.

## License

Apache-2.0

## Author

Alfresco Ops Readiness
