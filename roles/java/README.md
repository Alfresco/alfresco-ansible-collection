# java

This role installs the java JDK (OpenJDK) and optionally imports certificates
into the java keystore and generates security keys.

It will set the `java_needs_restart` fact to `true` when using the `keystores`
entrypoint (see example playbook below).

## Requirements

As the role has `allow_duplicates` set to `false`, you MUST make sure you call
the role with appropriate arguments BEFORE any other role may call it with
different arguments.

## Dependencies

This role relies on the `community.general` collection to manage java keystores.

## Example Playbook

Installing OpenJDK into the default location:

```yaml
- hosts: all
  roles:
    - alfresco.platform.java
```

Installing OpenJDK and importing a server certificate in the java keystore:

```yaml
- hosts: all
  roles:
    - alfresco.platform.java
  tasks:
    - ansible.builtin.include_role:
        name: alfresco.platform.java
        tasks_from: keystores
      vars:
        cert_containers:
          - path: snakeoil.p12
            pass: dummy
            add_to_trusted_ca: false
```

Installing OpenJDK, importing certificates and generating a security key:

```yaml
- hosts: all
  roles:
    - alfresco.platform.java
  tasks:
    - ansible.builtin.include_role:
        name: alfresco.platform.java
        tasks_from: keystores
      vars:
        cert_containers:
          - path: server-snakeoil.p12
            pass: dummy
            add_to_trusted_ca: false
          - path: client-server-snakeoil.p12
            pass: dummy
            add_to_trusted_ca: true
        seckeys:
          - name: mykey
            algorythm: AES
            length: 256
            pass: dummy
```

> Note: a single client/server cert may also be provided.

## Author Information

[Hyland](https://hyland.com) - Alfresco Ops-Readiness
