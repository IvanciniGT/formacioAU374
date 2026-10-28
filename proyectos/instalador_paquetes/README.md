instalador_paquetes
=========

Este role instala un conjunto de paquetes, en máquinas con distribución de GNU/Linux:
- Redhat
- Debian

Realmente es un wrapper sobre el role `instalador_paquete` que facilita la instalación de lotes de paquetes en un solo playbook.

Role Variables
--------------

| Variable | Descripción |
|----------|-------------|
| paquetes  | Diccionario con cada paquete a instalar, donde la clave es el nombre del paquete y el valor es un diccionario con su configuración. |
| paquetes.<nombre_paquete>.nombre | Nombre del paquete a instalar. |
| paquetes.<nombre_paquete>.version | Versión del paquete a instalar. |
| paquetes.<nombre_paquete>.version.name | Nombre de la versión del paquete a instalar. |
| paquetes.<nombre_paquete>.version.operator | Operador de comparación de la versión del paquete a instalar. Puede ser : `=`, `>=`, `<=`, `>`, `<` |
| paquetes.<nombre_paquete>.redhat | Configuración específica para la distribución Redhat. |
| paquetes.<nombre_paquete>.redhat.version | Versión del paquete para la distribución Redhat. |
| paquetes.<nombre_paquete>.redhat.version.name | Nombre de la versión del paquete para la distribución Redhat. |
| paquetes.<nombre_paquete>.redhat.version.operator | Operador de comparación de la versión del paquete para la distribución Redhat. Puede ser : `=`, `>=`, `<=`, `>`, `<` |
| paquetes.<nombre_paquete>.redhat.repo | Repositorio del paquete para la distribución Redhat. |
| paquetes.<nombre_paquete>.redhat.repo.url | URL del repositorio del paquete para la distribución Redhat. |
| paquetes.<nombre_paquete>.redhat.repo.key | Clave del repositorio del paquete para la distribución Redhat. |
| paquetes.<nombre_paquete>.debian | Configuración específica para la distribución Debian. |
| paquetes.<nombre_paquete>.debian.version | Versión del paquete para la distribución Debian. |
| paquetes.<nombre_paquete>.debian.version.name | Nombre de la versión del paquete para la distribución Debian. |
| paquetes.<nombre_paquete>.debian.version.operator | Operador de comparación de la versión del paquete para la distribución Debian. Puede ser : `=`, `>=`, `<=`, `>`, `<` |
| paquetes.<nombre_paquete>.debian.repo | Repositorio del paquete para la distribución Debian. |
| paquetes.<nombre_paquete>.debian.repo.url | URL del repositorio del paquete para la distribución Debian. |
| paquetes.<nombre_paquete>.debian.repo.key | Clave del repositorio del paquete para la distribución Debian. |
| paquetes.<nombre_paquete>.debian.repo.suite | Suite del repositorio del paquete para la distribución Debian. |
| paquetes.<nombre_paquete>.debian.repo.components | Componentes del repositorio del paquete para la distribución Debian. |


Dependencies
------------

Este role necesita de otro role para funcionar.
El role requerido es `instalador_paquete`.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
    - hosts: servers
      ansible.builtin.include_role:
        name: instalador_paquetes
        vars:
          paquetes:
                nginx:
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
                curl:   {}
```

License
-------

MIT-0

Author Information
------------------

Si necesitas una mano con el role, te cobro un café: <ivan.osuna.ayuste@gmail.com>
