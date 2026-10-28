instalador_paquete
=========

Este role instala un paquete, en máquinas con distribución de GNU/Linux:
- Redhat
- Debian

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

Ejemplo:

```yaml
paquete:
  nombre: "nginx"
  version:
          name: "1.26.2"
          operator: ">="
  redhat:
       version:
              name: "1.26.2-1.el9.ngx"
              operator: ">="
       repo:
              url: "https://nginx.org/packages/rhel/$releasever/$basearch/"
              key: "https://nginx.org/keys/nginx_signing.key"
  debian:
       version:
              name: "1.26.2-1~noble"
              operator: "="
       repo:
              url: "https://nginx.org/packages/ubuntu"
              key: "https://nginx.org/keys/nginx_signing.key"
              suite: "noble"
              components:
                - "nginx"
```

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
