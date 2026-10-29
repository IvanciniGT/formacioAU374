
# Dependencias

El control de dependencias es CLAVE en un desarrollo.

Mi playbook dependerá de ciertos roles para funcionar y esos roles estarán dentro de colecciones.
A su vez, esas colecciones van a ir evolucionando con el tiempo:
- v1.0.0
- v1.1.0
- v1.1.1

de las colecciones.

Y ya vemos que en el galaxy.yaml he de meter la versión de la colección que estoy creando.
En el entorno de ejecución del playbook, meteré la versión de la colección de la que depende el playbook.

Coleccion paqueteria v1.0.0
        ^
Playbook servidor_web v1.0.0
 Y genero un entorno de ejecución (execution-environment) para mi playbook, incorporando la versión de la colección de la que depende en la versión correspondiente.
    execution-environment v1.0.0 -> Colección paqueteria v1.0.0

Mi playbook depende de esa colección porque necesita instalar paquetería.
Puede haber un fallo en la colección.. en uno de los roles: UN BUG, que en algún escenario no instala adecuadamente.
Y necesitaré generar una nueva versión de la colección que corrija ese fallo, por ejemplo:
Colección paqueteria v1.0.1
        ^
Playbook servidor_web v1.0.0
 Y genero un nuevo entorno de ejecución para mi playbook, incorporando la nueva versión de la colección.
    execution-environment v1.0.1 -> Colección paqueteria v1.0.1
    Esto implica: generar imagen nueva de contenedor
        Necesito subirla a un registry
        Necesito configurarla en AWX
        Y actualizar en AWX todos los playbooks para que a partir de este momento utilicen la nueva versión del execution-environment.

        TODO ESTO ES TRABAJO! Y no es poco!

Imaginemos que dentro de esa colección meten ahora un role para mandar_emails, que no tiene nada que ver con la instalación de paquetería.
Eso implica, que sale una nueva versión de la colección:
Colección paqueteria v1.1.0
        ^ (Necesito actualizar esta referencia?)
Playbook servidor_web v1.0.0
    Necesito generar nueva versión del entorno de ejecución para reflejar la nueva versión de la colección?
    Eso es una pregunta que me hago? Y que tengo que responder.
    Y como la respondo?
    - Mirando en la documentación de la colección qué ha cambiado.
    - Lo normal es que al lado del fichero README.md haya un fichero CHANGELOG.md donde se indique qué ha cambiado en cada versión.
    - Esos ficheros CHANGELOG también siguen un estandar: Keep a Changelog (https://keepachangelog.com/), donde se indica claramente qué ha cambiado en cada versión y si son cambios mayores, menores o parches.
          ESTO ES UN HUEVO DE CURRO!
          Pero se hace! El tiempo está aquí! No en rellenar 3 módulos de ansible.

El separar claramente funcionalidades en colecciones implica que cada colección tenga su propio ciclo de vida, su propio versionado y su propia documentación. Y que cuando algo cambie, impacte solamente a los que relamnete usan esa funcionalidad...
No a mi, que estoy instalando paquetes.. no mandando correos.
