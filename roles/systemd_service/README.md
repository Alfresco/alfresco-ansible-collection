# systemd_service

Install and configure systemd services.

## Requirements

None.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  tasks:
    - name: Install my systemd service
      ansible.builtin.include_role:
        name: systemd_service
        apply:
          become: true
      vars:
        systemd_service_unit_name: "my-java-app"
        systemd_service_unit_description: "My Java Application"
        systemd_service_exec_start: "/opt/java/bin/java -jar /opt/myapp/myapp.jar $JAVA_OPTS"
        systemd_service_user: "myapp"
        systemd_service_environment:
          JAVA_OPTS: "-Xms512m -Xmx512m -XX:MaxMetaspaceSize=256m"
```

## License

Apache-2.0

## Author

Alfresco Ops Readiness
