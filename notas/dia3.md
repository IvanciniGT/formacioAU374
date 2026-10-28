# Principio DRY

El principio DRY (Don't Repeat Yourself) establece que no debemos repetir código o lógica en nuestro proyecto. En lugar de duplicar, debemos abstraer y reutilizar componentes, funciones o roles para mantener el código más limpio, mantenible y menos propenso a errores.

# Ejecución de los playbooks

PLAYBOOK1 - PLAY1
Y lo ejecutamos contra un inventario que tiene 2 HOSTS: host1 y host2.

```bash
ansible-playbook -i inventario playbook1.yml --tags "tag1" --exclude-tags "tag2"
```

Cuántas ejecuciones del play habrá? 2 (una por cada host)

Y lo importante a entender es que CADA HOST / CADA EJECUCION DEL PLAY tiene su propio JUEGO DE VARIABLES!
Esas variables están disponibles a lo largo de la ejecución del play!


Nuestro play tiene:
- TAREA1 - módulo setup -> (distribution) -> 
              ansible_facts:
                distribution
                os_family
                version
- TAREA2
- INCLUDE_TASKS (fichero que define otras 3 tareas)
  - SUBTAREA1
  - SUBTAREA2
  - SUBTAREA3
- TAREA3
- INCLUDE_ROLE (rol define 2 tareas)
  - SUBTAREA_ROLE_1
  - SUBTAREA_ROLE_2 ---> Necesitamos rellenar el dato repositorio. Pero para ello necesito la os_family.
                         Tengo aqui la os_family? Esta rellena esa variable? La han calculado antes?
                         Y la respuesta es NPI

Una variable que haya sido establecida por la tarea 1 estará disponible para todas las tareas siguientes dentro del mismo play.

Cada HOST tiene su propio juego de variables!
Es decir, la tarea 1 se ha ejecutado 2 veces. Una vez para host1 y otra vez para host2.
En la ejecución del host 1, existe una variable llamada ansible_facts.
Pero en la ejecución del host 2, también existe una variable llamada ansible_facts, independiente de la del host 1.


---

# Combine filetr jinja

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

paquete[ansible_facts.os_family | lower] # En el caso de Redhat

          version:
                  name: "1.26.2-1.el9.ngx"
                  operator: ">="
          repo:
                  url: "https://nginx.org/packages/rhel/$releasever/$basearch/"
                  key: "https://nginx.org/keys/nginx_signing.key"

paquete | combine(paquete[ansible_facts.os_family | lower], recursive=true)

      nombre: "nginx"
      
      version:
            name: "1.26.2-1.el9.ngx"
            operator: ">="
      repo:
            url: "https://nginx.org/packages/rhel/$releasever/$basearch/"
            key: "https://nginx.org/keys/nginx_signing.key"