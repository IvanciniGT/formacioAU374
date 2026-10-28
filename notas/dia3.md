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

              vars:
    paquetes:                             "{{ paquete_actual.value | combine({'nombre': paquete_actual.key}) }}"
  loop:                                   "{{ dependencias | dict2items }}"
  # La variable dependencias es un mapa:
  # dependencias:
  #   git:
  #     version:
  #         name:          "1.7.1"
  #         operator:      ">="
  #   rsync:                 {}
  #   curl:                  {}

   #dict2items, la treansforma en una. lista, para poder usarlo en un loop:
   #   - key: git
   #     value:
   #       version:
   #           name:          "1.7.1"
   #           operator:      ">="
   #   - key: rsync
   #     value: {}
   #   - key: curl
   #     value: {}

  # Eso es un filtro jinja..
  loop_control:
    loop_var:                             paquete_actual
    label:                                "{{ paquete_actual.key }}"
---

Tengo ahora un playbook, llamado "servidor_web".
Ese playbook, para ejecutarse necesita de 2 roles (instalador_paquetes y instalador_paquete)
A su vez, instalador_paquete necesita de otro role: instalador_paquete_concreto.

Dónde busca ansible esos roles (las carpetas con las tasks, defaults, vars..., filtros customizados, etc.):
1. En una subcarpeta dentro del playbook: llamada como el role, o dentro de la carpeta "roles" del playbook.

    servidor_web/
        instalador_paquete/
        roles/
            instalador_paquetes/
            instalador_paquete_concreto/

    Evidentemente esto no es lo que quiero...Los roles deben ser reutilizables entre varios playbooks, por lo que conviene tenerlos en una ubicación centralizada, como una carpeta "roles"en otro sitio.
2. En una ubicación centralizada, como por ejemplo:
    Ansible los busca en automático:
    - /etc/ansible/roles
    - /usr/share/ansible/roles
    - ~/.ansible/roles
3. O en una carpeta a mi elección: /mis_roles
   Pero en este caso, le tengo que decir a Ansible dónde buscar esos roles. Y hay varias formas:
   - Fichero de configuración de Ansible (ansible.cfg), usando la opción roles_path: 
    ```ansible.cfg
    [defaults]
    roles_path = /mis_roles
    ```
   - Variable de entorno ANSIBLE_ROLES_PATH: /mis_roles
   - O usando la opción -p al ejecutar ansible-playbook:
     ```bash
     ansible-playbook -p /mis_roles servidor_web.yml
     ```
Formas hay muchas... PERO TODAS DAN POR SUPUESTO UNA COSA:
   Que esas carpetas existen en el entorno donde voy a ejecutar ANSIBLE!
   Y existirán? Alguien las tiene que haber copiado allí!

Dónde se va a ejecutar el playbook? En mi máquina? En un entorno centralizado en la empresas disponible 24x7
Qué necesito en ese entorno/servidor central de la empresa? Qué tiene que haber instalado?
- Ansible-Core y su configuración
- Python
- Playbooks
- Roles que usen los playbooks
- Inventario
- Los módulos que hemos usado en el playbook, en Ansible se agrupan en ? Colecciones
  Colecciones que necesite nuestro playbook:
    - ansible.builtin
    - ansible.posix
    - community.general
  Ansible core trae esas colecciones?
    ansible.builtin : SI
    ansible.posix : NO
    community.general : NO
        // Esto se instala con un comando :
            ansible-galaxy collection install community.general
            ansible-galaxy collection install ansible.posix
- Dependencias de paquetes en el servidor, como en nuestro caso curl!

Podemos dar por supuesto que todo eso existirá en el entorno de ejecución de Ansible que me ha hecho la empresa?
EVIDENTEMENTE NO!

Solución: Antes de ejecutar / pasar un playbook a producción, abrir un ticket en JIRA para pedir al dpto de Ansible de sistemas que installen toda la mierda que necesito en el entorno de ansible! :) XDDDDDDDDD

- Espera de brazos cruzados de 1 a 3 meses... para que al final te digan QUE NO!
  Que esas no son las colecciones aprobadas oficiales.. y que hay que iniciar un proceso de validación de que esas lirberías no rompen el servidor..
  Además, resulta que Menchu tiene también su playbook... pero el playbook de menchu necesita:
                           Menchu            Yo
    - Ansible                2.7             2.20
    - community.general      3.0             3.5
    - ansible.posix          1.2             1.2.3
    - curl                   -               7.9

Hay que mirarlo... es delicado... Ya te contaremos! QUE NO!

Cómo lo vemos?
Necesito montar yo el entorno.... Y me dejan montar a mi un entorno en los servidores centrales de la empresa? NO

Pero... eso es lo que hace AWX / Ansible Controller por nosotros. Que le tenemos allí infiltrado!

Le vamos a DEFINIR / DECLARAR (paradigma declarativo) a AWX/Ansible Controller como queremos que sea un entorno de ejecución para nuestros playbooks, incluyendo todas las colecciones, dependencias y configuraciones necesarias, versiones que YO NECESITO!

Y amablemete AWX/Ansible Controller se encargará de montar ese entorno de ejecución tal y como lo he definido, sin necesidad de que yo toque los servidores centrales directamente.


Desde hace 3 años, ha cambiado mucho la forma en que gestionamos los entornos de ejecución para Ansible.
Antes dependíamos completamente del equipo de sistemas para instalar y configurar todo, lo que generaba retrasos y complicaciones.

Ahora definimos el entorno de ejecución de nuestro playbook en un fichero, con una sintaxis que me ofrece ANSIBLE!
Mi entregable no es solo el playbook.
Cuando entrego un playbook, entrego junto con él una definición del entorno de ejecución que necesita, incluyendo todas las colecciones, dependencias y configuraciones necesarias.

Muchas veces un mismo entorno me puede servir para varios playbooks que compartan las mismas dependencias y configuraciones, evitando tener que redefinirlo cada vez.

De hecho en la práctica CADA PLAYBOOK se ejecuta en un entorno INDEPENDIENTE.
De hecho, en la práctica, CADA EJECUCION DE CADA PLAYBOOK se ejecuta en un entorno independiente.
AWX/Ansible Controller crea entornos EFIMEROS. De usar y tirar, como os Kleenex.

Que hay que ejecutar un playbook, AWX/Ansible Controller crea y levanta un entorno efímero basado en la definición/especificación que le hemos proporcionado, ejecutará el playbook dentro de ese entorno y luego lo destruirá automáticamente.

En ese entornoo, en automático copia mi playbook y el inventario.

Más vale, que las dependencias (paquetes, roles, colecciones...) Que necesite mi playbook las HAYA PUESTO YO en la definición del entorno de ejecución, porque AWX no las pone por mi. No me pone NI ANSIBLE, para que yo tenga la oportunidad de definir exactamente el ansible que necesito (versión).


Ansible define los ficheros `execution-environment.yml` para describir los entornos de ejecución que necesita cada playbook. En este fichero especifico las colecciones, dependencias, configuraciones y la versión de Ansible que mi playbook requiere.


Esos entornos, se crean realmente como CONTENEDORES!
A efectos prácticos (por dentro no se parecen en nada) nos ofrecen las mismas funcionalidades (más o menos) que una máquina virtual. Cual es la principal diferencia entre un contenedor y una MV? 
- Las VM incluyen un sistema operativo completo y requieren más recursos (CPU/MEMORIA/ALMACENAMIENTO).
- Los contenedores usan el núcleo del sistema operativo del host. No llevan su propio sistema operativo completo. No pueden llevarlo.

Eso implica que cuando creo una MV, uso una imagen .iso de varios GBs que contiene todo el sistema operativo + luego mis mierdas!
En cambio, cuando creo un contenedor, solo pongo mis mierdas! Y ocupa Unos cuantos MB.

Se crea más rápido, funciona más rápido,. arranca casi instantáneamente. Y se borran más rápido también.
IDEAL PARA ENTORNOS EFÍMEROS Y DE USO TEMPORAL, COMO LOS QUE CREA AWX/ANSIBLE CONTROLLER PARA CADA EJECUCIÓN DE PLAYBOOK.

Los contenedores se crean desde IMAGENES DE CONTENEDOR (similar al concepto de IMAGEN ISO), que contienen todo lo necesario para ejecutar mis playbooks (ansible+colecciones+roles+dependencias+configuraciones).

En ansible, esas IMAGENES DE CONTENEDOR SE GENERAN EN AUTOMÁTICO a partir del fichero `execution-environment.yml` que hemos definido... casi.

Necesito darle a PLAY!

$ ansible-builder build -f execution-environment.yml -t registro.miempresa.com/mi_entorno_efimero:latest

Esto genera EN LA MAQUINA donde se ejecute una imagen de contenedor.
Esa imagen después debe subirse al registry de imagenes de contenedor de mi empresa:

$ docker push registro.miempresa.com/mi_entorno_efimero:latest

Posteriormente en AWX/Ansible Controller doy de alta un ENTORNO DE EJECUCION:
    - nombre: MiEntorno
      imagen: registro.miempresa.com/mi_entorno_efimero:latest

Cuando doy de alta en AWX/Ansible Controllermi playbook, le pongo un dato adicional, el ENTORNO DE EJECUCION que debe usar:

    - nombre: MiPlaybook
      entorno: MiEntorno      <---- QUE IMAGEN DE CONTENEDOR DEBE USAR

Cuando ejecuto el playbook AWX/Ansible Controller levantará un contenedor usando la imagen asociada al ENTORNO DE EJECUCION que he especificado. Esto asegura que mi playbook se ejecute en un entorno consistente y controlado, con todas las dependencias y configuraciones necesarias. Cuando acaba la ejecución, el contenedor se destruye automáticamente, dejando el sistema limpio y sin residuos.


Lo único que si debo hacer yo es:
- Construir la imagen de contenedor usando `ansible-builder build`.
- Subir la imagen al registry de contenedores de mi empresa.

LO NORMAL EN LAS EMPRESAS! LO GUAY! LO QUE DEBERIAMOS TENER y si no lo tenemos ya, en algún momento estará:
- Un pipeline de ENTREGA CONTINUA! (Jenkins, GitlabCI/CD, etc.), que:
  - Cuando un desarrollador de playbook sube su playbook a git, en automático:
    - Constrya la imagen de contenedor usando `ansible-builder build`. (para no tener que hacerlo yo manualmente)
    - La suba al registry de contenedores de la empresa. (para no tener que hacerlo yo manualmente)
    - Lo registre en AWX/Ansible Controller como un ENTORNO DE EJECUCION disponible. (para no tener que hacerlo yo manualmente)

Si eso no existe ún... ME TOCA HACERLO A MANO!
