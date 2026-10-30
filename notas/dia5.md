
> Cúal es el motivo importante para trabajar con ramas en los roles/colecciones/playbooks que vamos creando?

Tendremos 2 entornos donde ir ejecutanto los playbooks/roles..
- Uno de producción, donde solo queremos aplicar cambios que ya han sido probados y validados.
- Otro, donde probaremos los cambios antes de pasarlos a producción.

En AWX/Ansible Controller necesitamos dejar los 2 preparados.
Esto es independiente de que haga pruebas en mi máquina.
No siempre voy a poder hacer pruebas realistas en mi máquina, depende del playbook.

Al dar de alta el proyecto (repositorio) en AWX/Ansible Controller, usaremos ramas diferentes, para distinguir entre la versión que estoy probando y la versión que está aprobada para su ejecución.

El problema no es el día 1.
El día 1 solo pongo el playbook en el entorno de pruebas (AWX de pruebas). Cuando funcione, lo pongo en el entorno de producción (AWX de producción). Y ahi no hay problema.. porque trabajo secuencialmente:
1º Pongo el playbook en el entorno de pruebas y lo ejecuto allí, hasta que funcione correctamente.
2º Una vez que funciona en el entorno de pruebas, lo pongo en el entorno de producción y lo ejecuto allí.

El problema es cuando ese playbook ya está ejecutándose.... y necesito hacer un cambio.
Ahí, en ese escenario, hay una divergencia, al menos durante el tiempo en que estoy haciendo cambios y probando.
- Por un lado está la versión que funciona en producción.
- Por otro lado está la versión en la que estoy haciendo cambios y probando en el entorno de pruebas.

Y la forma que tengo en AWX para controlar las 2 versiones es mediante:
- ramas diferentes en el repositorio.
- Poniendo una versión concreta!
  Esto es incómodo.  Cada vez que hago una prueba tengo que actualizar la versión concreta en AWX, lo cual puede ser tedioso y propenso a errores.

Lo mejor es que ponga en AWX una rama. 
- En el de pruebas-> RAMA: desa
  Esto me asegura que siempre, cuando ejecuto, se coja la última versión (commit) de la rama de desarrollo.
  Me evita problemas y me agiliza el trabajo.
  - Solo hago cambio
  - Hago commit/push
  - AWX: Ejecuto.

Luego está producción.. y ahí puedo:
- Trabajar con versión concreta: Si quiero un nivel de control más grande.
- Poner la rama main: Si quiero que producción siempre tenga la última versión estable de la rama principal.

Si hago bien las cosas, en general es más cómodo trabajar con lo último que hay en main.
- Entro en AWX y configuro la rama main para el proyecto de producción. Esto asegura que siempre se ejecute la última versión (commit) estable de la rama principal.

> Cómo haría si quiero poner una versión concreta?

Según voy haciendo commits en GIT , a algunos de esos commits les puedo poner un TAG.
Esos tags me ayudan a identificar commits concretos dentro del historial de commits.

                      TAG: v1.0.1
                       v
    C1 -> C2 -> C3 -> C4
          ^
          TAG: v1.0.0

A nivel de comando:
    $ git tag v1.0.0 -m "Versión 1.0.0"
    $ git push --tags

En AWX puedo poner también esas etiquetas.

> Me interesa esto? O pasamos de esto y solo usamos ramas?

En AWX, configuramos ramas o tags? Qué interesa?
- Si configuro tags, cada vez que hay un cambio, tengo que acordarme de ir a cambiar el tag en el proyecto.
  Lo acepto? NO
  Para eso está el concepto de las ramas:
  - MAIN: Donde lo que hay se considera apto para producción 
  - DESA: Donde se hacen los cambios y pruebas antes de pasar a producción

Entonces, nos interesa esto de los tags? SI, tiene sus casos de uso.

En general, solo vamos a trabajar con RAMA -> práctico, cómodo, me asegura que siempre se ejecute la última versión de la rama correspondiente.

Pero... hago un cambio en un playbook. Lo pruebo en mi entorno de pruebas... va guay. Paso a producción (subo el commit a rama main).
Y en producción peta (una configuración en un entorno diferente que no he tenido en cuenta)!
Acciones:
- Quiero ir marcha atrás <- En este momento es lo más importante!
  Cómo hago esto? En este caso uso un tag de versión de commit anterior. 
- Iré arregando aquello

Ayer hablaba de imágenes de contenedor... y decíamos que la URL de una imagen tiene:
    registry/repo:tag

    Y dijimos que hay 2 tipos de tags:
    - Fijos:            v1.1.0
    - Variables:        latest

Es el mismo concepto en git. De hecho en git, una rama es solo un TAG que se mueve con cada nuevo commit.
Las ramas son TAGS variables.
Otra cosa es yo ponga (con el comandito $ git tag) un tag fijo en un commit concreto.

Los conceptos son los mismos.

---

# Control avanzado de la ejecucion del playbook

Yo monto mi playbook... con la funcionalidad que necesite.. yeso da lugar a una sere de tareas.
Pero cuando acabo de montar el playbook, tengo que pararme... y pensar, en cómo quiero ejecutar ese playbook:
- Rendimiento
- Controlando la HA (Alta Disponibilidad) de los servicios

Esto no tiene que ver con el funcional. Es algo aparte.

- Estrategias de ejecución: linear, free
- Forks: Número de procesos paralelos que Ansible puede usar para ejecutar tareas en los hosts. RENDIMIENTO (inter-nodos)!
         Viene limitado principalmente por la capacidad del controlador y la red.
- serial/max_fail_percentage: Número de hosts que se ejecutan en serie antes de pasar al siguiente grupo de hosts. Útil para controlar la HA y evitar sobrecargar los servicios.
- async/poll (async_status [until, retries, delay]): RENDIMIENTO / PARALISMO (intra nodo)
- throttle: Limita el número de hosts que pueden ejecutar tareas simultáneamente. Útil para controlar la carga en los servicios y evitar saturar la infraestructura.
- ansible.builti.meta: end-play, end-host
- any_errors_fatal: Hace que cualquier error en cualquier host detenga la ejecución del playbook. Útil para garantizar consistencia y control de la HA.

Nota final:
- Una cosa es arrglar algo que hemos jodido en producción (rescue)
- Otra cosa es evitar que ese algo impacte en servicio (cuando ocurre un error). Que ese error no afecte al servicio.

---

# Apliquemos esto a nuestro playbook del servidor_web.

## Rendimiento intra-nodo

¿Qué me planteo aquí? ¿Por dónde empiezo?
- Lo primero IDENTIFICAR LAS TAREAS QUE TARDAN MUCHO! Y ver si puedo lanzarlas en paralelo con otras tareas.

## Impacto en servicio en caso de fallo
- No hablamos de meter el rescue

Si tengo un cluster de nginx, y el playbook falla... quiero que se siga ejecutando en el resto de nodos? NO
- Como empiezo?
  Lo más burdo: 
    ```yaml
    serial: 1                    # Ejecutar de uno en uno todo el play
    max_fail_percentage: 0       # Detener el play si algún host falla
    ```
  Qué haría? En cuanto falle un host (y los proceso de uno en uno, que pare).
  Qué problema tiene esto? Impacta mucho en rendimiento. En el tiempo total que tarda el cluster en actualizarse.

  ME IMPORTA? Quizás no! Y estoy bien. Tengo 10 máquinas.. no 500.

  Si quiero ir más fino:
    ```yaml
    serial: [1, 2, 100%]                    # Ejecutar de uno en uno, luego de dos en dos, y finalmente todos los hosts
    max_fail_percentage: 30                 # Detener el play si más del 30% de los hosts fallan
    ```
  Mejora rendimiento.
  Y habitualmente con esto vale.


---


mirar si el proceso a nivel de so está funcionando:
ps aux | grep nginx

mirar si el puerto esta abierto (desde la máquina): 80???
netstat -tuln | grep 80

curl http://localhost:80 -> 200

Ver si el dns está bien (resuelve correctamente el dominio)
getent hosts dominio.com   

Ver si el puerto está abierto desde una maquina externa (firewall)
nc -zv <host_externo> 80
telnet <host_externo> 80

Probar la web desde fuera:
curl http://dominio.com:80 -> 200

--
Realmente tenía sentido hacer todas esas pruebas, o habría servido con la última?
Evidentement... el hacer 6 pruebas... tarda mucho más tiempo que hacer solo la última.
QUIERO METER LAS 6 realmente en el playbook de producción? LAS 6. Por qué?
- Las pruebas sirven para muchas cosas.
  - Una cosa es saber si funciona! La sexta es la me dice si funciona.
  - Pero también sirven para que si NO FUNCIONA, saber exactamente dónde está el problema.

El playbook un día fallará. Y ese día tendré que mirar por qué?
Es decir, hacer las 6 pruebas!

Las prefiero hacer cuando falle en producción, con los usuarios metiendo presión o las prefiero hacer cuando creo el playbook?
CUANDO CREO EL PLAYBOOK!

---

1. Crear un repo de github PRIVADO
2. Clonar mi repo -> Actualizar
3. Vincularlo vuestro repo clonado local a vuestro repo remoto privado
   Desvincularlo del mio
4. Cambio en el playbook
5. Vamos a subirlo a github. a vuestro repo privado
6. Crear credenciales en AWX.
7. Registrar nuevo proyecto/repo en AWX. 
8. Ejecutar el playbook desde AWX.