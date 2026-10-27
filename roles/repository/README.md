# repository

This role configures authentication and user synchronization on an
already installed Alfresco Content Services repository (for example one
deployed with
[alfresco-ansible-deployment](https://github.com/Alfresco/alfresco-ansible-deployment)).
It does not install the repository, and it does not provision any KDC or
Active Directory resources.

It has two independent entrypoints:

* `kerberos`: Kerberos (SPNEGO) single sign-on. It writes `krb5.conf`,
  installs the keytab, writes the JAAS login configuration and the Kerberos
  authentication subsystem properties, and sets the `authentication.chain`
  in `alfresco-global.properties`.
* `ldap_sync`: users and groups synchronization from Active Directory. It
  writes the properties of an `ldap-ad` subsystem instance with LDAP
  authentication disabled. It does not change the authentication chain.

Both entrypoints set the `repository_needs_restart` fact to `true` when they
change a configuration file or the keytab. Restarting the repository is up to
the calling playbook.

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
  `repository_kerberos_java_opts` fact after running the `kerberos`
  entrypoint (`-Djava.security.auth.login.config` and
  `-Djava.security.krb5.conf`).
* The synchronization only runs for subsystem instances listed in the
  authentication chain: add the `ldap_sync` instance (for example
  `ldap1:ldap-ad`) to `repository_authentication_chain`.
* Directories enforcing LDAP signing refuse simple binds over plain LDAP.
  Use an `ldaps://` URL and a truststore holding the directory CA, set through
  `repository_ldap_sync_extra_properties` (see the example below).
* With alfresco-ansible-deployment, run the `kerberos` entrypoint after each
  deployment (it regenerates `alfresco-global.properties`) and leave
  `repository_identity_url` unset.

## Dependencies

None.

## Example Playbook

Kerberos SSO with users synchronized from Active Directory:

```yaml
- hosts: repository
  tasks:
    - ansible.builtin.include_role:
        name: alfresco.platform.repository
        tasks_from: ldap_sync
      vars:
        repository_ldap_sync_url: ldaps://ad.example.com:636
        repository_ldap_sync_bind_principal: svc-alfresco@example.com
        repository_ldap_sync_bind_password: "{{ vault_ldap_bind_password }}"
        repository_ldap_sync_user_search_base: ou=Users,dc=example,dc=com
        repository_ldap_sync_group_search_base: ou=Groups,dc=example,dc=com
        repository_ldap_sync_extra_properties:
          ldap.authentication.java.naming.security.protocol: ssl
          ldap.authentication.truststore.path: /etc/opt/alfresco/content-services/ldap-truststore.p12
          ldap.authentication.truststore.passphrase: "{{ vault_ldap_truststore_password }}"
          ldap.authentication.truststore.type: PKCS12

    - ansible.builtin.include_role:
        name: alfresco.platform.repository
        tasks_from: kerberos
      vars:
        repository_kerberos_realm: EXAMPLE.COM
        repository_kerberos_kdcs:
          - ad.example.com
        repository_kerberos_principal: HTTP/alfresco.example.com
        repository_kerberos_keytab_src: files/alfresco.keytab
        repository_authentication_chain:
          - kerberos1:kerberos
          - ldap1:ldap-ad
          - alfrescoNtlm1:alfrescoNtlm
```

## Author Information

[Hyland](https://hyland.com) - Alfresco Ops-Readiness
