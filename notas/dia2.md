
# Versionado de software

Usamos tradicionalmente en la industria del software lo que se llama el esquema de versionado semántico (Semantic Versioning: semVer).

vA.B.C
                 Cuándo suben?
A = MAYOR        Breaking changes! Cambio que rompe compatibilidad
                 Cuando quito algo de funcionalidad (con o sin reemplazo)
B = MINOR        Nueva funcionalidad
                 Se marca una funcionalidad como obsoleta (Deprecated)
                    (Opcionalmente puden venir arreglos de bugs)
C = PATCH        Arreglos de defectos (bugs) - Bugfixes

Oracle 11
Oracle 12
Oracle 19
       ^^
       MAYOR

       Puedo actualizar un servidor de BBDD con tranquilidad de Oracle 11 a Oracle 12? NO, ni de broma
       En cuanto instale la Oracle 12, hay cosas que ya no funcionan igual.
       Y Puede ser (caso que esas cosas se usasen por mi app) que mi aplicación deje de funcionar correctamente.
       Es necesario revisar profundamente la app, para ver si sigue funcionando o no sobre esa versión,
       y en su casohacer los cambios que sean necesarios para que siga funcionando correctamente.

Imaginad que tengo Oracle 11.7 y quiero pasar a Oracle 11.8. Puedo hacerlo con tranquilidad?
       Sin problema.. es compatible. Cómo lo se? Por el numerito.. es el mismo MAYOR!
       Quiero hacerlo? Depende. De qué depende?
       - Si necesito esa nueva funcionalidad... aunque si ya estaba trabajando con Oracle 11.7, es que mi sistema NO NECESITA NI USA esa nueva funcionalidad. Solo tendrá sentido si modifico el sistema para que ahora haga uso de esa nueva funcionaldiad.
         Sin modificar nada, esa nueva funcionalidad NO LA USARÉ. Y ojo... puede venir con nuevos BUGS! Que han tocado código!
       - Que se incluyan PARCHES (PATCH) que solucionen problemas gordos o críticos (seguridad...)
       - Acaba el soporte de esa versión! 
       - Por cojones! Hay un roadmap de actualización que tengo que seguir!

Lo que marca la funcionalidad de un sistema es la pareja MAJOR.MINOR
El PATCH me habla de la cantidad de bugs que se han ido resolviendo en esa versión MAJOR.MINOR.


ROLE - Instalación de paquetes

Al role le llegan / deben llegar estos datos:

```yaml
       paquete:              ""          # OBLIGATORIO. Nombre del paquete: nginx, git...
       version:              ""          # Del tipo a.b.c. Vacío: la última disponible
       operador_version:     "="         # =  >=  <=  >  <
       repositorio:          ""          # URL del repositorio. Vacío: los oficiales
       clave:                ""          # URL de la clave GPG del repositorio
       suite:                ""          # Solo Debian/Ubuntu. Vacía: la de la versión del host (noble, jammy...)
       componentes:                      # Solo Debian/Ubuntu: componentes del repositorio
                     - main
```
Qué repo pongo? el de debian o el de redhat?
Dependerá de donde se ejecute...


Se invoca desde un playbook que instala nginx sobre máquinas debian y redhat.
```yaml
    - name:               Asegurar que NGINX queda instalado en el host en la versión que me interesa
      ansible.builtin.include_role:
        name:             instalacion_paquetes
      vars:
        paquete:          nginx
        version:      
        operador_version: "="
        repositorio:  
        clave:        
        suite:        
        componentes:  
```

Qué datos debo pasar? Los de debian o los de rhel?
Depende del host donde ejecute el playbook... pero es que mi playbook se ejecuta en paralelo en hosts Debian y RHEL.
Hay que calcularlo para cada host.. si tiene que pasar los datos debian o los de RHEL.

Saber si tengo una máquina redhat o debian es fácil.
Hay una variable que me da la info: ansible_facts.os_family (que se rellena con el módulo setup.)
Pero de donde saco los repos de debian y los de redhat?
Quién / dónde define esa información?
Quién (qué ser humano) decide qué repos se usan en el caso del debian y en caso del redhat para nuestro playbook del nginx? El que ha hecho la web / el que vaya a ejecutar el playbook!
Esos datos pueden incluso cambiar con el tiempo.

Quien ejecute el playbook tendrá que decir:
- paquete: nginx (Este ya lo sabemos.. no lo tiene que dar)
- version
- repositorio redhat
- repositorio debian

---
Es responsabilidad de quien ejecuta el playbook decidir sobre qué sistema operativo corre su playbook?
- Si el nginx se instalará en un debian o en un redhat? NO ES SU REPONSABILIDAD. 
  DE QUIEN ES ESA RESPONSABILIDAD? De los administradores de INFRA DE LA COMPAÑIA!
       - Producción RHEL
       - Desarrollo Debian
- Quien despliega una web decide esto? Tiene algo que opinar ahí?

---

En este sistema que estamos desasrrollando (Despliegue de un nginx con una web), qué actores (qué personas/departamentos) hay involucrados?
                                   RESPONSABILIDAD
- Desarrollo WEB            -      Crear la web 
  - Negocio                 -      Quien decide cuándo se despliega

- Desarrollo del playbook
- Infraestructura HOSTS            Tener másquinas preparaditas con SO receptoras de la aplicación/nginx/web
- Infraestructura REDES            Que esas máquinas tengan comunicación, A nivel físico, lógico... puertos (firewalls)
- Storage
- Seguridad

YO, desarrollador del playbook, decido los SO?, las versionesde NGINX? de que repos tiro al hacer la instalación? NO
Pero... NECESITO ESOS DATOS. Cuando se ejecute el playbook ME LOS DEBEN SUMINISTRA -> ARGUMENTOS del playbook (variables de entrada)

Yo soy especialista en qué disciplina? Desarrollo de playbooks de ansible.
Evidentemente necesito tener background de muchas cosas:
- De todo!
- Necesito saber de desarrollo de webs?
  - Yo no voy a montar HTMLS. Pero necesito saber que para desarrollar una web hacen falta ficheros HTML, JS, que se dejan en un repositorio de GIT, que luego hay que montar eso en un servidor web.
- Necesito conceptos de instalación de paquetería en hosts linux? Evidentemente.. y no un mínimo.. un máximo.
- Necesito saber cositas de comunicaciones? y en concreto aplciadas a servidores web?
  -  Que los servidores web hablan por HTTP(s), puertos por defecto 80,443. Que para probar una web lanzo una petición RHTTP REQUEST con un determinado VERBO (GET, POST, PUT) ... que la salida dara un HTTP STATUS CODE (200, 300, 400, 500) Que en la respuesta de un RESQTUEST HTTP hay un BODY con o que devuelve la ruta a la que llamo.
  -  Que los desarrolaldores deben montar unos endpoints (rutas) en su web para que se puedan hacer las peticiones HTTP de pruebas, para verificar que el despliegue esta funcionando.

QUE NOMBRE RECIBE ESTE PERFIL? EL YO CREADOR DEL PLAYBOOK? Devops.
Y por qué se le llama así. Porque tiene que saber de todo (DEV y OPS)
Tiene que ser exerto en DEV? NO, pero sí debe entender lo suficiente para poder automatizar los despliegues y configuraciones necesarias.
Tiene que ser experto en OPS? NO, pero sí bastante como para ser capaz de realizar algunas tareas operativas básicas y debe entender lo suficiente para poder automatizar los despliegues y configuraciones necesarias.

Mi trabajo no es tomar DECISIONES! Hay gente que se encarga de eso (desarrollo, arquitectura, infra, redes), yo solo ejecuto lo que se decide y automatizo los procesos necesarios. Quizás tome alguna decisión también.

Pero lo que si tengo son necesidades para hacer mi trabajo.
Con respecto a la instalación de nginx, qué necesidades tengo?

Necesito saber:
1- La versión (exacta o al menos) que se debe instalar
2- En qué tipo de SO se va a instalar
3- Qué repos/claves deben usarse para cada uno de ellos

Qué si decido y, como creador del playbook? 
- Cómo hacerlo...
- Cómo quiero que me pasen esa información que me hace falta!

> Cómo quiero que me los den?

Dato a priori (en desarrollo) : CONSTANTE
- los so soportados. Esto me lo dan en tiempo de ejecución? NO.. el playbook LO DESARROLLO para unos determinados SO... 

Como argumentos:
- version_nginx
- operador_version_nginx
- repo_debian
- clave_debian
- repo_redhat
- clave_redhat

Si el día de mañana hay más sistemas operativos, tendré: más argumentos
- repo_<nuevo_so>
- clave_<nuevo_so>

> Pregunta: La version de nginx que voy a montar es la misma en todos los SO? No es mi responsabilidad. Por lo tanto qué asumo? No tiener por qué ser la misma:
- version_nginx_debian
- version_nginx_redhat

---

Quién rellenará esos argumentos? Quién ejecute el playbook... que en el mejor escenario posible sería?
- JENKINS! Gitlab CI/CD, AWX, Ansible Controller
- De donde sacan esos datos el JENKINS? VEte a saber.. algunops los da INFRA, COMUNICACIONEs, ARQUITECTURA O DESARROLLO. O un acuerdo entre ellos!

Pero alguién debe decidir al final.. y no soy yo.
Se va a poner contento al rellenar esos 15 argumentos que he definido? NO
Puedo hacerle más feliz?
Hay una manera mejor de hacer que me pase esos datos? Que mediante argumentos sueltos por linea de comandos?

> $ ansible-playbook install_nginx.yml -e version_nginx_debian=1.18.0 \
>                                      -e version_nginx_redhat=1.18.0 \
>                                      -e repo_debian=http://example.com/debian \
>                                      -e clave_debian=ABC123 \
>                                      -e repo_redhat=http://example.com/redhat \
>                                      -e clave_redhat=XYZ789

En lugar de parametritos sueltos, podría? Un fichero donde tenga todos:

> $ ansible-playbook install_nginx.yml -e @config.yml
> - Cuántos de esos ficheros de configuración habrá? 500
>   - Este playbook se usará para desplegar la app1, la app2, app 17, en producción, en desarrollo, en preproducción
>   - En todos los entornos monto la misma verisón de nginx? NO

Hay gente en las empresas que su misión es rellenar estos ficheros y dar a play!
Y esos ficheros de configuración los quiero en GIT, sometidos a control de versiones.. independientes del GIT de la WEB,
Independientes del GIT de playbook!

       Instalo la version 1.0.0 de la web, usando el iknstalador (playbook) v1.0.0 sobre el entorno desarrollo, con la configuración v1.0.0.
       Mañana sale nueva verisón de la web: 1.1.0, que instalo con la misma versión del instalador (playbook) v1.0.0 sobre el entorno desarrollo, con la configuración v1.0.0.
       Pero pasado se decide subir el nginx de versión, e instalo la misma versión de la web v1.1.0, con la misma del instalador (playbook) v1.0.0 sobre el entorno desarrollo, con la configuración v1.1.0.
       Pero identifico un error en el playbook... no está generando los logs bien el nginx. No está bien la configuración de nginx que genera el playbook.
       Y lo instalo de nuevo, la misma versión de la web: v1.1.0, con la nueva versión del playbook v1.0.1 sobre el entorno desarrollo, con la configuración v1.1.0.

Esto es llevar un control SERIO DE CONFIGURACION en unn entorno de producción empresarial, no un control de CUÑAO!

Este es el objetivo. Aqí es donde la BASH hace agua! Esto es otra de las cosas que aporta Ansible.
Ansible no es aprender una sintaxis, es cambiar la cultura de trabajo. Esto es gradual!

Por cierto, cómo se llama a ese concepto que he usado en el ejempo anterior? IaC (Infrastructure as Code)
IaC no es usar terraform... ni tener en ficheros recurso. 
Es tratar la infra como si fuera código, lo primero SOMETIDA CONTROL DE VERSIONES!

DECISION: Argumentos en un fichero:
Estructura del fichero:

```yaml
# Escriba aquí la versión de nginx que desea instalar... Si es la misma en todos los sistemas operativos, puede usar la misma versión global.
version_nginx:                     1.18.0
operador_version_nginx:            ABC123
# Información del repositorio debian
repo_debian:                       http://example.com/debian
clave_debian:                      ABC123
# Información del repositorio redhat
repo_redhat:                       http://example.com/redhat
clave_redhat:                      XYZ789
# Información del repositorio windows
repo_windows:                      http://example.com/nuevo_so
clave_windows:                     ABC123
# Escriba aquí la versión de nginx específica para cada sistema operativo si es diferente de la global.
version_nginx_debian:              1.18.0   # En este caso sobreescribe la versión global para Debian
version_nginx_redhat:              1.18.0   # En este caso sobreescribe la versión global para RedHat
version_nginx_windows:             1.18.0   # En este caso sobreescribe la versión global para Windows

# Además de esto, tendremos:
# - versión de la web
# - repo de la web
# - Pruebas que hay que hacer a la web
# - ...

# Este fichero acabará con 50-200 argumentos.
```

Probabilidad de que me olvide de un parametro? o que me equivoque en un nombre?    1-10 -> 0
Probabilidad de que me olvide de actualizar un valor cuando llegue un cambio?       1-10 -> 0


# Alternativa:
```yaml
# Escriba aquí la versión de nginx que desea instalar... Si es la misma en todos los sistemas operativos, puede usar la misma versión global.

nginx:
       default: 
              version: 
                     name:         1.18.0
                     operator:     ">="
       redhat:
              #version: # Quiere versión default
              #       name:         1.18.0
              #       operator:     ">="
              repo:
                     url:          http://example.com/redhat
                     key:          XYZ789
       debian:
              version:
                     name:         1.18.1
                     operator:     ">="
       ubuntu: {} # Repos oficiales y versión default
---
# Esto es lo que me pasan a mi, en tiempo de ejecución. A mi, el creador del playbook.
# Pero ojo! Otra cosa es lo que YO creador del playbook tengo que pasar al ROLE que instala!
# Eso es lo que espera el ROLE que instala?

paquete:              ""          # nginx
version:              ""          # la version.name del SO concreto sobre el vaya a instalar
                                  # OJO si hay una especificada. Si no la hay, cuál paso? el de default
                                  # Si no hay en default... ninguna... y que se monte la ultima!
operador_version:     "="         # LA MISMA MIERDA!
repositorio:          ""          # El del SO concreto sobre el que vaya a instalar.. si es que lo hay.. si no, ninguno
clave:                ""          # La que me corresponde según el repositorio del SO concreto... si es que lo hay.. si no, ninguna
---
# Quizás para un paquete concreto (curl):

curl: {}
git:
       default:
              version:
                     name:         1.7.1
                     operator:     ">="
# Esto me da juego!
```


Da igual cuál coja... Lo imprtante no es cuál. Es:
- Entender que hay muchas opciones!
- Qué tengo que tomar una decisión
- Y qué tengo que vivir con ella! (Yo al crear el playbook)
- Y qué muchas personas tendrán que vivir con ella! (a los que crean los 500 ficheros de configuración)


Variable que yo leo:
- En tiempo de ejecucion se mira cual de esos es el que tengo en la máquina donde debo instalar
               familia_so (lo saco yo)


---

> Qué será más sencillo al desarrollar el playbook?

Tener variables sueltas (ejemplo 1)
Tener una variable agrupada (ejemplo 2)






¿QUIÉN DECIDE LA VERSION NGINX? Acuerdo entre Desarrollo en Infra/Arquitectura
       Si lo da Infra/Arquitectura, Desarrollo debe ajustarse a la funcionalidad de esa versión.
       Si lo da Desarrollo, Infra/Arquitectura debe asegurarse de que la versión elegida cumple con los requisitos de infraestructura, compatibilidad, seguridad y soporte.



# Desarrollo de software

Cómo empieza un proyecto de desarrollo de software. Qué es lo primero que necesitamos hacer?

- Definir los casos de uso: Qué actores hay y qué hace cada uno (cuál es su responsabilidad sobre el sistema?)
- Toma de requisitos

---


ROLE 1: Instala un paquete en una versión concreta usando un repositorio concreto en base al sistema operativo concreto que teng un host concreto. ESTE ES EL QUE HAY!

ROLE 2: Instala un paquete en una versión dependiente del SO dinamicamente, usando un repo elegido dinamicamente según el sistema operativo del host concreto.

PLAYBOOK: Uso el role 2. y mi playbook queda mucho mas sencillo.
          En varios sitios además, que estoy usando eso.
          Y de paso, los 17 playbooks que montaré mañana: mysqkl, apache, nginx, redis, postgresql, memcached, rabbitmq, elasticsearch, kibana, logstash, prometheus, grafana, vault, consul, nomad, traefik, coredns,
          también van a quedar mucho más sencillos.

Si el día de mañana hay que dar soporte a una nueva distro de so, en cuántos sitios debo tocar? ROLE 1

Si el día de mañana quiero que cambié la lógica de cómo se elige un repo u otro... solo toco el ROLE 2.
Por ejemplo... Tengo en mi empresa un SATELLITE de Red Hat que gestiona los repositorios de los distintos sistemas operativos que usamos. Con los paquetes que he aprobado. Y quiero que si no me especifican repo, se tire automáticamente del repo gestionado por el SATELLITE.


Esto es lo mejora la mantenibilidad y la VIABILIDAD del sistema a largo plazo!

Y por cierto... Ya tengo 2 ROLES que se encargan de cosas similares...
De hecho están íntimamente relacionados. El ROLE 2, requiere el ROLE 1.
Uno instala un paquete en una versión concreta usando un repositorio concreto según el sistema operativo del host.
El otro instala un paquete en una versión dependiente del SO dinámicamente, usando un repo elegido dinámicamente según el sistema operativo del host concreto.

Qué tendría sentido hacer con ellos? UNIRLOS EN UNA COLECCION: "miempresa.instalaciones", igual que está la colección "ansible.builtin".
Y cada vez que alguien en mi empresa tenga que instalar un paquete, solo tendrá que usar la colección "miempresa.instalaciones" y elegir el role adecuado según sus necesidades.
Y esto tiene otra ventaja adicional:
TODOS LOS FICHEROS DE CONFIGRUACION DE TODOS LOS PLAYBOOKS TENDRAN LA MISMA ESTRUCTURA.
Y si muevo a alguien de un dpto a otro, lo que se encontrará será algo con lo que sienta totalmente familiarizado, sin tener que aprender estructuras diferentes para cada playbook.

---

# Estructura de un role:

rolename/
  defaults/                 Argumentos de nuestro role. Lo que me dara un usuario al usar el role.
    main.yml
  files/                    Archivos que nuestro role lea y copie a los remotos.
  handlers/                 El listado de posibles handlers que se ejecutarán si son alctivados por las tareas del role.
    main.yml
  meta/                     Información /metadatos adicionales del playbook:
                            - Quien es el autor, licencia, descripción del role.
                            - Dependencias con otros roles si las hubiera.
    main.yml                  
  tasks/
    main.yml                El listado de tareas que ejecutará el role.
  templates/                Archivos que nuestro role lea y copie a los remotos, transformándolos en el proceso.
                            Plantillas, que se se rellenarán con valores concretos. Se escriben en formato jinja.
                            La extensión de estos archivos es .j2
  vars/                     Constantes de nuestro role. Datos que necesita,definidos en tiempo de desarrollo.
    main.yml

La estructura de un role viene impuesta por Ansible. Esas carpetas y ess archivos no los puedo llamar como me de la gana.
Cuando importamos un role, dentro de un playbook, ansible busca en automático esas carpetas y archivos siguiendo la estructura que hemos visto.
Si puedo, si no uso alguna de esas carpetas borrarla. No es obligatorio tener todas las carpetas, solo las que realmente necesite el role.

# Por donde empiezo a trabajar cuando creo un role?

- Los datos que me tienen que pasar!, lo que metemos en defaults/main.yml.
  En paralelo, definir funcionalmente que debe hacer el role. 
- Listado de tareas