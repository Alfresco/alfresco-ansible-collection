# utils

Download and verify checksum

## Requirements

None.

## Role Variables

`artifact` A dictionary defining the artifact to download and verify.
The role automatically downloads the checksum file by appending the checksum type as an extension to the artifact URL (for example, .sha1 or .sha256).

Both Maven-style (checksum only) and legacy common-format (checksum followed by filename) checksum files are supported.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  tasks:
    - name: Download application artifact using utils role
      ansible.builtin.include_role:
        name: alfresco.platform.utils
        tasks_from: download_verify_checksum
      vars:
        artifact:
          url: https://nexus-dev.alfresco.com/repository/maven-releases/org/alfresco/alfresco-control-center/10.3.0/alfresco-control-center-10.3.0.zip
          dest: /tmp/artifacts
          checksum_type: sha256 # optional
          username: nexus_username        # optional
          password: nexus_password    # optional
```

## License

Apache-2.0

## Author

Alfresco Ops Readiness
