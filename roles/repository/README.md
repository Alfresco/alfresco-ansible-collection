# repository

This role configures authentication and user synchronization on an
already installed Alfresco Content Services repository (for example one
deployed with
[alfresco-ansible-deployment](https://github.com/Alfresco/alfresco-ansible-deployment)).
It does not install the repository, and it does not provision any KDC or
Active Directory resources.

It has two independent entrypoints. Each one configures a subsystem only when
its option is set, and fails when none is set:

* `authentication`: authentication subsystems.
  * `repository_authentication_kerberos`: Kerberos (SPNEGO) single sign-on.
    It writes `krb5.conf`, installs the keytab, writes the JAAS login
    configuration and the Kerberos authentication subsystem properties.
* `user_sync`: users and groups synchronization subsystems.
  * `repository_user_sync_ldap_ad`: synchronization from Active Directory. It
    writes the properties of an `ldap-ad` subsystem instance with LDAP
    authentication disabled.

Neither entrypoint changes `alfresco-global.properties`. Both set the
`repository_needs_restart` fact to `true` when they change a configuration
file or the keytab. Restarting the repository is up to the calling playbook.

See `meta/argument_specs.yml` for the full list of variables.

## Requirements

* The keytab and the service principal (for example `HTTP/alfresco.example.com`)
  must already exist in the KDC. The principal host must be the name users
  browse to (the load balancer name when the repository is behind a proxy).
* The keytab must hold AES keys (Java 17 and later reject RC4). With Active
  Directory, the principal must also be the service account's
  `userPrincipalName`, as set by `ktpass -mapuser`. Otherwise the repository
  fails to start.
* The repository JVM must be started with the options exposed in the
  `repository_authentication_java_opts` fact after running the
  `authentication` entrypoint (`-Djava.security.auth.login.config` and
  `-Djava.security.krb5.conf`). With alfresco-ansible-deployment, add them to
  `repository_acs_environment.JAVA_OPTS`, keeping its default entries (the
  variable is replaced as a whole).
* The calling playbook must set `authentication.chain`, listing the configured
  instances (synchronization only runs for instances in the chain). With
  alfresco-ansible-deployment, add it as a flat key to the existing
  `global_properties` in `playbooks/group_vars/repository.yml` (setting
  `global_properties` in the inventory is ignored, and with `-e` it replaces
  all the other properties), and do not deploy Keycloak (no hosts in the
  `identity` or `external_identity` groups), otherwise the playbook sets its
  own chain:

  ```yaml
  global_properties:
    # ...existing entries...
    authentication.chain: kerberos1:kerberos,ldap1:ldap-ad,alfrescoNtlm1:alfrescoNtlm
  ```

* Directories enforcing LDAP signing refuse simple binds over plain LDAP.
  Use an `ldaps://` URL and a truststore holding the directory CA, set through
  `repository_user_sync_ldap_ad.extra_properties` (see the example below).

## Dependencies

None.

## Example Playbook

Kerberos SSO with users synchronized from Active Directory:

```yaml
- hosts: repository
  tasks:
    - ansible.builtin.include_role:
        name: alfresco.platform.repository
        tasks_from: user_sync
      vars:
        repository_user_sync_ldap_ad:
          url: ldaps://ad.example.com:636
          bind_principal: svc-alfresco@example.com
          bind_password: "{{ vault_ldap_bind_password }}"
          user_search_base: ou=Users,dc=example,dc=com
          group_search_base: ou=Groups,dc=example,dc=com
          extra_properties:
            ldap.authentication.java.naming.security.protocol: ssl
            ldap.authentication.truststore.path: /etc/opt/alfresco/content-services/ldap-truststore.p12
            ldap.authentication.truststore.passphrase: "{{ vault_ldap_truststore_password }}"
            ldap.authentication.truststore.type: PKCS12

    - ansible.builtin.include_role:
        name: alfresco.platform.repository
        tasks_from: authentication
      vars:
        repository_authentication_kerberos:
          realm: EXAMPLE.COM
          kdcs:
            - ad.example.com
          principal: HTTP/alfresco.example.com
          keytab_src: files/alfresco.keytab
```

## Author Information

[Hyland](https://hyland.com) - Alfresco Ops-Readiness
