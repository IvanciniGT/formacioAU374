instalador_paquete
=========

Este role instala un paquete, en máquinas con distribución de GNU/Linux:
- Redhat
- Debian

Realmente es un wrapper sobre el role `instalador_paquete_concreto` que facilita la instalación de paquetes específicos con sus repositorios y versiones correspondientes a la distribución de GNU/Linux en uso en el servidor concreto.

Role Variables
--------------

| Variable | Descripción |
|----------|-------------|
| paquete  | Diccionario con la información del paquete a instalar, incluyendo nombre, versión y configuración específica para cada distribución. | 
| paquete.nombre | Nombre del paquete a instalar. |
| paquete.version | Versión del paquete a instalar. |
| paquete.version.name | Nombre de la versión del paquete a instalar. |
| paquete.version.operator | Operador de comparación de la versión del paquete a instalar. Puede ser : `=`, `>=`, `<=`, `>`, `<` |
| paquete.redhat | Configuración específica para la distribución Redhat. |
| paquete.redhat.version | Versión del paquete para la distribución Redhat. |
| paquete.redhat.version.name | Nombre de la versión del paquete para la distribución Redhat. |
| paquete.redhat.version.operator | Operador de comparación de la versión del paquete para la distribución Redhat. Puede ser : `=`, `>=`, `<=`, `>`, `<` |
| paquete.redhat.repo | Repositorio del paquete para la distribución Redhat. |
| paquete.redhat.repo.url | URL del repositorio del paquete para la distribución Redhat. |
| paquete.redhat.repo.key | Clave del repositorio del paquete para la distribución Redhat. |
| paquete.debian | Configuración específica para la distribución Debian. |
| paquete.debian.version | Versión del paquete para la distribución Debian. |
| paquete.debian.version.name | Nombre de la versión del paquete para la distribución Debian. |
| paquete.debian.version.operator | Operador de comparación de la versión del paquete para la distribución Debian. Puede ser : `=`, `>=`, `<=`, `>`, `<` |
| paquete.debian.repo | Repositorio del paquete para la distribución Debian. |
| paquete.debian.repo.url | URL del repositorio del paquete para la distribución Debian. |
| paquete.debian.repo.key | Clave del repositorio del paquete para la distribución Debian. |
| paquete.debian.repo.suite | Suite del repositorio del paquete para la distribución Debian. |
| paquete.debian.repo.components | Componentes del repositorio del paquete para la distribución Debian. |


Dependencies
------------

Este role necesita de otro role para funcionar.
El role requerido es `instalador_paquete_concreto`.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
    - hosts: servers
      ansible.builtin.include_role:
        name: instalador_paquete
        vars:
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

License
-------

MIT-0

Author Information
------------------

Si necesitas una mano con el role, te cobro un café: <ivan.osuna.ayuste@gmail.com>
