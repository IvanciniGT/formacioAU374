
# Ansible Automation Platform

No es un programa en realidad.. son muchos los que ofrece Redhat para la automatizaciones.
- Ansible core (quien ofrece un lenguaje para definir automatizaciones e inventarios)
- Ansible Tower / AWX / Ansible Controller (interfaz web y gestión centralizada de automatizaciones/inventarios + Api REST)
- Ansible Galaxy (trabajo con roles y colecciones reutilizables)
- Ansible navigator / Ansible builder (Trabajar en local, siguiendo las mejores prácticas de desdarrollo de playbooks)
- ...

## Sobre el curso

- Primero trabajaremos en profundidad sobre Ansible Core + Galaxy, para desarrollo de playbooks, roles y colecciones avanzados.
- Luego abordaremos Ansible Tower / AWX para la gestión centralizada y la automatización a gran escala + Navigator para definir entornos de ejecución reusables

---

## Ansible Core

### Sobre los playbooks

En Ansible creamos playbooks, que son conjuntos / secuencias de tareas que se ejecutan sobre uno o varios entornos definidos en un inventario.

Entornos:
- Hosts físicos
- Máquinas virtuales
- Contenedores
- Equipos de red
- Cabinas de almacenamiento
- ...

Es decir: SCRIPTS.

En el mundo de sistemas NOS HAN CAMBIADO EL CONTRATO!
Ya no opero/administro sistemas sino que me han convertido en un PROGRAMADOR.
Mi trabajo ahora es CREAR PROGRAMAS que operen / administren los sistemas de manera automatizada.

## Automatizar

Automatizar es crear una máquina (o cambiar el comportamiento de una mediante PROGRAMAS) que haga lo que antes hacía un humano de manera manual.

LAVADORA es una máquina que automatiza el lavado de la ropa. A la lavadora le puedo cambiar su comportamiento mediante PROGRAMAS DE LAVADO (diferentes ciclos, temperaturas, velocidades, etc.)

En nuestro caso, la máquina existe: COMPUTADOR. A la computadora le podemos cambiar su comportamiento mediante PROGRAMAS (scripts, playbooks, etc.) que automatizan tareas que antes hacíamos manualmente.

Esto implica que deo comenzar a pensar en los mismos términos que un desarrollador de software: Modularidad, reutilización, abstracción, pruebas, mantenimiento, etc.
Y que vamos a hacer uso de las mismas herramienats que usan los desarrolladores de software: editores de código, sistemas de control de versiones, entornos de prueba, herramientas de integración continua, etc.

### Sobre automatizar

#### Automatizar es CARO!

Muy caro! Y solo tiene sentido en tareas que se repiten con frecuencia y que requieren precisión o consistencia que un humano no puede garantizar de manera eficiente. Tardo mucho menos y tengo que poner mucho menos esfuerzo en ejecutar un procedimiento de forma manual. Solo cuando algo se vaya a ejecutar muchas veces/sobre muchos entornos... vale la pena invertir en automatización.

#### Automatizar exige conocimiento mucho más profundo que hacer las cosas a mano.

Usar herramientas como ANSIBLE NO ME PONEN LAS COSAS FACILES. ME LAS COMPLICAN MUCHO!
Y no hablo de Ansible... y su lenguaje (eso es muy simple)
Sino del conocimiento profundo que se requiere sobre los sistemas/tareas que estamos automatizando: cómo funcionan, cómo se configuran, cómo se interrelacionan, cómo se depuran los errores, etc.

Cuando hago algo a mano, en muchos casos, tengo la oportunidad de aprender sobre la marcha.

Para automatizar con éxito tengo que traer ya ese conocimiento de casa! Y MUCHO... Y MUY PROFUNDO.
No hay oportunidad de ir aprendiendo sobre la marcha!

#### Tareas vs procesos.

Puedo automatizar tareas, y puedo automatizar procesos.
Son dos cosas separadas... aunque para automatizar procesos es necesario primero automatizar las tareas individuales que lo componen.
Luego hay que tener en cuenta otra cosa... y es que hay procesos de distinto nivel. Hay jerarquias de procesos.. y subprocesos.

La lavadora automatiza EL PROCESO O LA TAREA?

- Proceso de lavado de la ropa... Implica muchos TRABAJOS:
  - Separar la ropa por colores y tipos de tejido.
  - Cargar la lavadora con la ropa y el detergente.
  - Seleccionar el ciclo de lavado adecuado.
  - Iniciar la lavadora y esperar a que termine.
  - Sacar la ropa y tenderla o ponerla en la secadora.
  - Doblar y guardar la ropa limpia.

Pero a su vez muchos de esos trabajos se descomponen en tareas más pequeñas. Por ejemplo:
  - Iniciar la lavadora y esperar a que termine... pero eso hace muchas cosas:
    - Coger agua y calentarla
    - Comenzar a mojar la ropa
    - Echarle detergente a la ropa
    - Girar la ropa dentro del tambor para asegurar que se lave de manera uniforme.
    - ...

Cada uno de esos trabajos es una TAREA.

El proceso es lo que hemos descrito arriba del todo...
Pero luego tenemos ese TRABAJO(s) INTERMEDIO(s):
    Iniciar la lavadora y esperar a que termine / lavar la ropa. ?? QUE NOMBRE LE PONEMOS A ESTO?
    Desde el punto de vista del proceso de lavado.. es una tarea de ese proceso.
    Desde el punto de vista propio, es un subproceso que engloba muchas tareas individuales necesarias para completar ese trabajo intermedio.

#### Sobre las automatizaciones con ANSIBLE

Lo que vamos a automatizar con Ansible, desde nuestro punto de vista son PROCESOS! Procesos que consisten en una serie de tareas individuales que deben ejecutarse de manera ordenada y consistente para lograr un objetivo específico.

PERO HAY UNA COSA QUE NO PUEDO PERDER DE VISTA. Esos "PROCESOS" que automatizaré, posiblemente sean "TAREAS"/"SUBPROCESOS" de otros PROCESOS DE NIVEL SUPERIOR.

> Por ejemplo: El ejemplo del que vamos a partir:
>        Asegurar que unos entornos (Ubuntu/RHEL) tienen una determinada versión de nginx instalado
>        Configurar ese nginx
>        Desplegarle una web, extraída desde un repositorio Git
>        Configura servicios
>        Verificar que todo queda funcionando correctamente

Hay tareas muy pequeñas... individuales.. atómicas en ese playbook.. por ejemplo: 
  - Crear una carpeta donde desplegar la web.
  - Descargar una copia del repositorio Git donde se encuentra la web.
  - Hacer un backup del despliegue anterior que existiese...

El playbook en si es un proceso COMPLEJO!

Pero a su vez, ese playbook puede considerarse una tarea más de otro proceso de nivel superior en la empresa, por ejemplo , de un pipeline de CD (Despliegue Continuo) que automatiza todo el flujo de entrega de la web.

    Desarrollador de la web (commit / nueva versión de la web)
    - Revisión del código automatizada
    - Escaneo en busca de debilidades/problemas de seguridad
    - Hay un proceso(subproceso) que se lanza con terraform, para provisionar la infraestructura necesaria para desplegar la web.
    - Una vez provisionada la infraestructura, se ejecuta el playbook de Ansible que hemos descrito antes para configurar nginx y desplegar la web.

Mi trabajo es centrarme en "PROCESO/SUBPROCES/TRABAJO" que voy a hacer en Ansible, pero sin perder de vist, que seguramente (al 100%) forme parte de un proceso de nivel superior en la empresa.

---

# Que ofrece Ansible Core con ese "lenguaje" ?

Es decir ... venimos creando automatizaciones desde hace décadas (bash, ps1, python...). Para qué otro lenguaje?

- Funcionalidad. Tanto la bash, como ps1, como python son lenguajes de propósito general que permiten crear cualquier tipo de programa. No hay problemas de que haya cosas que no pueda hacer con ellos.
- Multiplataforma:
  - Python es multiplataforma y puede ejecutarse en diferentes sistemas operativos sin necesidad de modificar el código.
  - Los playbooks de ansible, por defecto SON TOTALMENTE DEPENDIENTES DEL ENTORNO EN EL QUE SE EJECUTAN. Un playbook creado para Redhat no funciona en UBUNTU. Si quiero soporte de múltiples sistemas operativos, me lo tengo que currar.

## Lo que cambia es la forma en la que usamos el lenguaje: PARADIGMA DE PROGRAMACION

Un paradigma de programación es la forma en la que un programador usa un lenguaje para expresarse.
No es algo propio de los lenguajes de programación, en los lenguajes humanos (naturales) también existe el concepto.

> Menchu, mete la ropa a la lavadora      IMPERATIVO

Imperativo también es uno de los grandes paradgmas de programación. En este paradigma, se le indica al ordenador paso a paso qué hacer. Le damos ORDENES.
Y estamos muy acostumbrados al uso de lenguaje IMPERATIVO: BASH, PYTHON, PS1... Todos ellos principalmente me llevan al uso de paradigma imperativ (DAR ORDENES)

> $ mkdir lavadora
  # make directory lavadora              IMPERATIVO

El paradigma imperativo es un problemón.

Qué pasaría si la lavadora ya está llena de ropa cuando le digo a Menchu que meta la ropa? Qué me dice Menchu?
- NoLeftSpaceOnDevice
- InvalidArgumentException
- 404 - Bad Request
- Exit code 127

No puedo meter la ropa porque la lavadora ya está llena.

Ésto nos obliga/nos lleva al guarreo típico de los progrmas escritos con paradigma imperativo.
> Menchu: IF puerta is CLOSED: THEN 
>   OPEN the door                        Imperativo!
> Menchu: IF (Condicional al canto) any in lavadora THEN
>   SACALO!                               Imperativo!
> Menchu, mete la ropa a la lavadora      IMPERATIVO

COMENTARIO AL AMRGEN: Y esta forma de crear programas de hecho, es la culpable de que muchos(as) de vosotros(as) hayaís acabado en el mundo de sistemas.

Claro... lo que pasa es que hay otras formas de expresarse.
Pero antes de eso.. un comentario.. ¿Por qué estoy escribiendo ese "programa" a Menchu, con todos esos CONDICIONALES?

- Contemplar todos los posibles ESCENARIOS que puede encontrase MENCHU! Para que con independencia de la situación, menchu pueda hacer su trabajo.

A ese concepto en INFORMATICA le llamamos IDEMPOTENCIA!

Idempotenci (en el mundo IT) se refiere a la propiedad de que un programa pueda ejecutarse múltiples veces sin cambiar el resultado más allá de la primera ejecución. Visto de otra forma: que con indepen del estado inicial, el resultado final será el mismo.

-> Mi objetivo es que la ropa quede en la lavadora.
   No me importa si la lavadora estaba llena o si la puerta estaba cerrada.
   Solo quiero que al final la ropa esté dentro.

        En nuestro ejemplo: Potenciales estados iniciales:
            - Lavadora vacia con puerta abierta
            - Lavadora vacia con puerta cerrada
            - Lavadora llena con puerta abierta
            - Lavadora llena con puerta cerrada
        Y quiero que con idnependencia de cuál sea el estado inicial, al final la ropa nueva que quiero lavar esté dentro de la lavadora.

El problema es que a Menchu no le he dado MI OBJETIVO. Le he ido diciendo lo que tenía que hacer en distintos escenarios.

> Menchu, necesito la ropa sucia en la lavadora. Es tu responsabilidad.    IMPERATIVO? NO LO ES
> Solo le EXPONGO, le EXPLICO cómo SON LAS COSAS.                          ES DECLARATIVO

Y el paradigma declarativo es muy bonito. Ha cambiado el concepto. Ya no le digo a Menchu lo que debe hacer. Sino lo que yo quiero conseguir!
Como consecuencia, acabo de delegar la responsabilidad de cómo conseguir lo que quiero conseguir a Menchu, sin preocuparme por los detalles de cada escenario.

Los detalles son suyos! Los condicionales son SUYOS! Que los escriba ELLA! Que haga lo que tenga que hacer para AL FINAL conseguir lo que yo quiero.

Digo que es bonito.. porque expresarnos de forma DECLARATIVA, implica en automático: LA IDEMPOTENCIA.

Yo quiero PROGRAMAS IDEMPOTENTES, que con independencia de cuál sea el estado inicial, siempre consigan el resultado deseado.
Puedo trabajarlos yo, con condicionales por un tubo y muchas ORDENES!
O puedo dejar a Menchu la responsabilidad de conseguir lo que quiero, sin preocuparme por los detalles de cada escenario.

> Qué lenguaje prefiero esar:

 OPCION 1: IMPERATIVO?
    > Menchu: IF puerta is CLOSED: THEN 
    >   OPEN the door                        Imperativo!
    > Menchu: IF (Condicional al canto) any in lavadora THEN
    >   SACALO!                               Imperativo!
    > Menchu, mete la ropa a la lavadora      IMPERATIVO

 OPCION 2: DECLARATIVO?
    > Menchu, necesito la ropa sucia en la lavadora. Es tu responsabilidad.    DECLARATIVO!

Esto es lo que da Ansible? NO Los scripts de Ansible son IMPERATIVOS!
Los scritps de Ansible son 100% IMPERATIVOS!

Entonces dónde está la gracia?

Ansible realmente NO SABE HACER LA "O" con un canuto!
Cualquier tarea que le pido la delega en un MODULO.
Los módulos son programas (ESCRITOS EN PYTHON, con lenguaje IMPERATIVO) que saben hacer tareas concretas. MUY ESPECIALIZADOS:
    Ejemplos:
        - Copiar archivos
        - Instalar paquetes
        - Configurar servicios
        - Reiniciar servidores

Muchos de esos módulos (la inmensa mayoría - NO TODOS) ofrecen lenguaje declarativo, y por ende IDEMPOTENCIA es su tarea concreta.

El SCRIPT/PROCESO de Ansible es IMPERATIVO, pero cada tarea concreta se ejecuta por un MODULO. Y en su inmensa mayoría son DECLARATIVOS y ofrencen IDEMPOTENCIA. Pero ojo: NO TODOS!

Hay tareas que puedo expresar de forma DECLARATIVA, y otras que (por su naturaleza) solo puedo expresar de forma IMPERATIVA.

    > Asegurar que el puerto de la web está abierto en el firewall, si hay uno activo?
         Qué pido? Que se asegure de que el puerto esté abierto. Esto implica que:
            - si está abierto?: No hacer nada
            - si está cerrado?: Abrir el puerto
    > Abre el puerto en el firewall, si hay uno activo?
         Qué pido? Que se abra un puerto.. y si ya estuviera abierto? ERROR!

> Pero el ejemplo... me ha encantado... porque tiene truco!

La frase tiene una segunda parte: "si hay uno activo?"
Que es eso? CONDICIONAL

La tarea la explicito de forma DECLARATIVA. 
El módulo QUE ABRE PUERTOS EN EL FIREWALL es capaz de determinar si es necesario abrir el puerto o no, en base a si ya está abierto o no.
Lo que pasa es que YO NO QUIERO QUE ESA TAREA SE EJECUTE SIEMPRE, solo quiero que se ejecute si hay un firewall activo.

Mi programa/script, llamará a esa tarea (MODULO) solo si se cumple la condición de que hay un firewall activo.

Esto implica que la lógica del programa la manejo yo, de forma IMPERATIVA (con mis condicionales), mientras que la tarea concreta de abrir el puerto sigue siendo DECLARATIVA e IDEMPOTENTE.

Y este es el mundo de ANSIBLE!

Si entendemos esto, Ansible será un paseo!
Si no entendemos esto, Ansible se nos puede volver un dolor de cabeza.

Y estas cosas son las que desgraciadamente no nos explican tan bien cuando aprendemos Ansible por primera vez, ni las que aprendo (o le doy imortancia) cuando aprendo Ansible por mi cuenta.
Porque esto parece una chorrada.. y a veces leemos IDEMPOTENTE, DECLARATIVO... y pasamos corriendo al ejemplo de instalar un paquete que es lo que a mi me hace falta.

---


# Terminos en Ansible:

- Playbook: Un conjunto de plays
- Play: Script que define un conjunto de tareas a ejecutar sobre unos entornos remotos.
- Tarea: Una acción concreta que se ejecuta dentro de un host remoto. Son ejecutadas por módulos.
- Módulo: Programa especializado (generalmente escrito en Python) que realiza una tarea concreta. Habitualmente escritos para que podamos usarlos mediante un paradigma declarativo. En ansible hay MILES de módulos disponibles para diferentes tareas.
  Son pequeñas "funciones" que ya nos dan desarrolladas.

    Para manajear ficheros en ansible usamos el módulo "file":
    Me permite creear, borrar, ficheros, directorios, enlaces simbólicos, y cambiar permisos y propietarios de los mismos.

    ```yaml
    - name: Asegurar que el directorio existe   # Nombre de la tarea
      file:                                     # Módulo que hará el trabajo, y al que le doy las instrucciones (MENCHU!)
        # Configuración del módulo. Lo que detalla el trabajo que le pido a Menchu
        path:  /ruta/al/directorio              # Le indico una ruta
        state: directory                        # Lo que quiero tener (el estado final)
                                                # OJO, no es lo que quiero que haga! NO ES IMPERATIVO
                                                # De hecho el nombre de la tarea está mal puesto.
                                                # No puede ser: Crear directorio
                                                # La tarea mira si el directorio existe:
                                                # Si no existe, lo crea.
                                                # Si ya existe, no hace nada.
                                                # Esto es lo que significa que sea idempotente.
        mode: '0755'                            # Permisos del directorio (opcional)
        owner: usuario                          # Propietario del directorio (opcional)
        group: grupo                            # Grupo del directorio (opcional)
    ```

    Qué puede hacer esta tarea (en tiempo de ejecución)? Posibilidades:
    - Si la carpeta no existe, la crea con los permisos que le digo, el propietario y el grupo especificados
    - Si existe:
      - Si tiene permisos distintos a los especificados, los cambia
      - Si tiene propietario distinto al especificado, lo cambia
      - Si tiene grupo distinto al especificado, lo cambia
    
    Equivalente en bash:

    ```bash
    if [ ! -d /ruta/al/directorio ]; then
        mkdir -p /ruta/al/directorio
    fi
    chmod 0755 /ruta/al/directorio
    chown usuario:grupo /ruta/al/directorio
    ```


    Los módulos son los que tienen dentro los IFs y el código imperativo.
    Yo al módulo le digo:
        Quiero que esto sea un directorio con estas características. ES TU RESPONSABILIDAD!
    Yo no me preocupo de cómo lo haces, solo del estado final: `state: directory`

    Hay miles de módulos. Nuestro objetivo NI DE LEJOS ES APRENDER MODULOS DE ANSIBLE! Alguos veremos al crear los playbooks... 
    Pero para eso está la DOCUMENTACION!

    NOTA: Este módulo funcionaría en máquinas LINUX y máquinas Windows? NO, solo en Linux.
    Para windows, hay otro módulo llamado `win_file` que cumple una función similar.

    Si quiero que mi programa funcione en windows y linux, debo usar las 2 tareas (los 2 módulos) con condicionales QUE PONGO YO!
    Por ejemplo:

    ```yaml
    - name: Asegurar que el directorio existe en Linux
    file:
        path: /ruta/al/directorio
        state: directory
    when: ansible_os_family == "Linux"                  
                                                            # Este es el IF... y este le pongo yo!
                                                            # El módulo por dentro pone muchos IFs
                                                            # Pero... si llamo O NO al módulo, es una decisión mía.. Y ESE CONDICIONAL ES MIO!

    - name: Asegurar que el directorio existe en Windows
    win_file:
        path: C:\ruta\al\directorio
        state: directory
    when: ansible_os_family == "Windows"
    ``` 

- Role   Es lo que en otros lenguajes de programación llamamos una FUNCION o PROCEDIMIENTO.
         Agrupa tareas que quiero ejecutar bajo un único nombre.    
         Me permite:
            - Reutilizar un conjunto de tareas.
            - Montar un playbook más organizado --> Para que cualquier pueda entenderlo de la forma más fácil posible.
              Y para qué querría yo que cualquiera pueda entenderlo?
              - Para usar un playbook necesito entenderlo? NO... tengo que mirar su documentación.
              - Para mantener y actualizar un playbook en el futuro !!!!

- Colección

    Una colección es un conjunto de roles, módulos y plugins que se agrupan bajo un mismo nombre.
    Permite distribuir y reutilizar paquetes de componentes.

    Es un nivel más en la jerarquía. Es lo que en programación tardiucional sería una LIBRERIA o una BIBLIOTECA!
    Es decir, una colección agrupa varios roles, módulos y plugins que pueden ser reutilizados en diferentes proyectos.

    En ansible hay MILES de colecciones disponibles. 
        - Algunas oficiales (que crea redhat).
        - Otras creadas por fabricantes concretos de Software/hardware.
          - Kubernetes: Contiene roles, módulos y plugins específicos para gestionar clústeres de Kubernetes.
          - AWS: Contiene roles, módulos y plugins específicos para gestionar servicios de Amazon Web Services.
          - CISCO: Contiene roles, módulos y plugins específicos para gestionar dispositivos de red de Cisco.
        - Colecciones creadas por la comunidad
        - Colecciones que creamos en las empresas (privadas, con mis mierdas! que no le interesan a nadie más que a mi!)
Uno de los objetivos fundamentales de este curso es aprender a:
- Aprender funcionalidades avanzadas de los playbooks
  - Se supone que llegados aquñi ya sabemos crear playbooks como el del ejemplo anterior.
  - Cosas complejas que si vemos en este curso:
    - Quiero hacer una actualización de unos entornos en producción. Tengo un cluster de X máquinas.
      Quiero que se ejecute el playbook en todas a la vez? 
      - O quiero hacer un canary (probando solo en una o 2)
      - Si va bien, empiezo la actualización... 
      - Asegurando que mantengo siempre un mínimo de entornos estables en producción.
    - Las tareas de los playbooks por defecto se ejecutan secuencialmente!
      Me interesa eso? Posiblemente en la mayoría de los casos NO!
        - Habrá tareas que si... pero muchas que no!
        Un playbook puede tardar minutos (muchos) en ejecutarse.
        Y lo que me interesa es que tarde lo menos posible!

        > Por ejemplo: El ejemplo del que vamos a partir:
        >        Asegurar que unos entornos (Ubuntu/RHEL) tienen una determinada versión de nginx instalado
        >        Configurar ese nginx
        >        Desplegarle una web, extraída desde un repositorio Git
        >        Configura servicios
        >        Verificar que todo queda funcionando correctamente
        
        Necesito hacer esas tareas secuencialmente?
        - Podrías paralelizar algunas:
          - 1. Instalación del nginx
          - 2. Configuración del nginx
          - 3. Despliegue de la web desde Git
        - Otra cosa es que cuando acabe esas:
          - Configuración de servicios (Lo cual implica ponerlo en pie si no lo está ya)
          - Verificación del funcionamiento correcto

            Lo que no tiene sentido es que ejecute 1, 2 y 3 en secuencial.
            La CPU de máquina aburrida, mis usuarios aburridos esperando, máquinas que entran después aburridas esperando.

        Aquí ya no hablamos del trabajo que hay que hacer a nivel funcional (que el coche ande)!
        Pero... anda guay? O le puedo mejorar un poquito aún? Y no hablo a nivel funcional!
        Hablo de:
        - Más rápido        \
        - Más reusable       > A este tipo de tareas, que hacemos una vez que nuestro programa YA HACE LO QUE TIENE QUE HACER le llamamos:
        - Más mantenible    /    REFACTORIZAR EL CODIGO

            En desarrollo tenemos claro que:

                    Desarrollo activo (pico código) <> Pruebas -> OK -> Refactorización <> Pruebas -> OK -> LIBERO!
                    <--------------- 50% del trabajo -------------->   <--- 50% del trabajo -------------->
                                8 horas                                            8 horas

        Y antiguamente no hacíamos lo segundo: la refactorización. Solo nos preocupábamos de que el programa funcionara, y eso genera: DEUDA TÉCNICA... 
            Y como toda deuda, habrá que pagarla, en algún momento.
            Y como toda deuda, cuánto más tarde la pagues, más intereses tendrás que pagar.
                Adecentar algo ahora, que lo acabo de hacer YO, me cuesta muy poco.
                Adecentar algo que hizo otra persona hace un año... es un trabajón.
                Y Encima hacerlo cuando surja un problema en producción es un desastre.

        Ansible NO ES SOLO CAMBIAR UN LENJUAGE POR OTRO!
        Es cambiar una CULTURA DE TRABAJO, no solo un lenguaje.

        Para qué hemos creado este script/playbook? 
        > Por ejemplo: El ejemplo del que vamos a partir:
        >        Asegurar que unos entornos (Ubuntu/RHEL) tienen una determinada versión de nginx instalado
        >        Asegurar que el nginx tiene la configuración correcta
        >        Asegurar que la ultima versión de la web está desplegada
        >        Asegurar que los servicios necesarios están configurados correctamente
        >        Verificar que todo queda funcionando correctamente        IMPERATIVO
        Para qué sirve?  O dicho de otra forma, CUANDO SE VA A EJECUTAR?
        - Para levantar una web (BIEN)
        - Ir actualizando el nginx con el paso del tiempo (cuando salgan parches)
        - Ir actualizando la web
        - Cambios en la configuración de la web/servicios
        - Monitorizar: Chequear si la web está funcionando correctamente
          Quizás ese playbook se ejecuta luego desde un DATADOG! solo para monitorizar el estado de la web.
          Y el playbook si no ha pasado nada con ella, no hará ningún CAMBIO: ES IDEMPOTENTE!

- Crear roles 
- Crear colecciones
- Gestionar roles/colecciones


    ### NOTA: 
        Cuando Creo un playbook NO LO CREO PARA MI!
        Quizás ANECDOTICAMENTE lo ejecute yo hoy en día... Pero eso cambiará!
        El playbook lo creo para un tercero, que no soy ni yo, ni mi equipo presente ni futuro.
        Los usuarios de mi playbook no seremos nosotros! O si!
        Pero no lo creo para mi!

        Incluso aunque sea para mi, me pondré 2 cascos/gorros diferentes:
        - El YO, creador del playbook
        - El YO, usuario del playbook
        Antes dije que yo automatizaré un PROCESO con mi playbook... pero que ese proceeso SEGURO será un elabón más dentro de una cadena más grande. PARTE DE UN PROCESO MAS AMPLIO.

            Ese proceso, a día de hoy NO EXISTIRA DE FORMA AUTOMATIZADA. NO LO BUSQUEIS!
            HASTA QUE NO AUTOMATICE MI SUBPROCESO Y EL RESTO DE SUBPROCESOS (Eslabones de la cadena) no tendrá sentido crearlo.

        USAR UN PLAYBOOK ES EJECUTARLO. Y para ejecutarlo necesito:
        - Saber que hace
        - Saber que le tengo que pasar
        - Saber que me va a devolver
        El cómo lo haga internamente me da igual!
---

Lo que estamos creando son programas!
Y que un programa FUNCIONE no es nada especial! Se da por descontado!
Mi trabajo no es un hacer un programa que funcione!
Para ser un programa debe funcionar! Si no, no es un programa, es un archivo de texto con pretensiones!

Un coche, no hay mérito en que ande!
Se da por descontado!
El ingeniero que crea un coche, su trabajo no es hacer que ande! Se da por descontado!
Si no anda no es un coche.. es una escultura de hierro con ruedas!

EL OBJETIVO ES CREAR ALGO QUE SEA MANTENIBLE Y DE POCO DOLOR DE CABEZA EN EL FUTURO! IGUAL QUE CUANDO SE CREA UN COCHE!
Un coche, por definición, es un producto sujeto a MANTENIMIENTO!
Y un producto de software (y un playbook es un producto de software) es por defición también un producto sujeto a CAMBIOS Y MANTENIMIENTO!
Más complejo aún.

Como quien dice, acabamos de llegar al mundo del desarrollo de software. NOS TOCA!
En el mundo del software lo tienen claro! No porque sean listos! PORQUE YA SE LA LLEVARON!

> Os suena la GRAN CRISIS DEL SOFTWARE?

Finales de los 60... llevábamos 2 décadas desarrollando software y de repente se dieron cuenta de que los proyectos no se completaban a tiempo, se excedían en presupuesto y eran de mala calidad.

Ahora, estamos desarrollando software... VAMOS A APRENDER DE LA GENTE QUE LLEVA DECADAS CREANDO SOFTWARE.
Hay 2 opciones:
- Aprendemos por las buenas
- Aprendemos por las malas
  Tengo 500 playbooks en la empresa y qu  e llega el punto en que nadie es capaz de hacer un cambio sin romper algo.
  Que llega una persona nueva al equipo, y el que había se piró! Y no hay forma de entender ni mantener los playbooks existentes.

  ESTO ES LO COMPLEJO! Y LO GRAVE!

En nuestro cas, no vamos a montar APLICACIONES! Eso es mucho más complejo.
Vamos a montar SCRIPTS, que también son programas, pero de otro nivel de complejidad totalmente distinto.
Pero los conceptos/reglas/buenas prácticas del desarrollo de software también aplican a los scripts.
Si no lo aplico, acaaré con mi GRAN CRISIS DEL SOFTWARE PERSONAL/EMPRESRIAL.

---

# Repaso básico de la sintaxis de un play:

```yaml

- name:           Nombre de mi play
  hosts:          localhost # all localhost servidor1 grupo2 !grupo3 grupo1&&grupo2!grupo3 #Valor por defecto (limitante) de los entornos sobre los que potencialmente se ejecutará el play
                            # En general no nos complicamos mucho, porque luego SIEMPRE limitamos a nivel de ejecución.
  gather_facts:   false # Y por defecto vienen en true!
                        # Trae datos del entorno donde ejecuto el play (sistema operativo, hardware, configuraciones de red, procesos que hay corriendo ahora mismo...)
                        # Por qué siempre en FALSE? NUNCA QUIERO TODO Y TARDA MUUUUCHO TIEMPO!!!! Para un curso básico y tutorial de youtube guay.. en empresa no vale!
                        # Cual es la alternativa si necesito datos de las máquinas? Módulo setup
  vars:           # Definir constantes
                  # Las definimos para no tener que esta inundando el play con valores repetidos o difíciles de mantener.
      version_nginx: 1.18.0       # Y ya no tengo que escribir por dejado en las tareas nunca más 1.18.0.. solo uso {{ version_nginx }}
                                  # Si un día quiero cambiar la versión, solo tengo que modificarla aquí y se reflejará en todas las tareas que usen {{ version_nginx }}.
  become:     false # Por defecto false . NO USAMOS TRUE
                   # Si quiero que las tareas del play se ejecuten con el usuario elevado en privilegios (por ejemplo root), pongo true.
                   # En windows el equivalente sería? Ejecutar como administrador.
                   # Decía yo.. que hay muchas formas de elevar privilegios:
                   # - sudo 
                   # - su - (cambiar de usuario)
                   # - runas (en windows para ejecutar como otro usuario)
                   # - polkit (en sistemas Linux con interfaz gráfica para elevar privilegios)
                   #...
                   # Y eso donde se define? y cuándo?
                   # Eso no se define aquí. Al crear un playbook aplicamos un principio de desarrollo de software llamado SoC.
                   # Mi preocupación ahora mismo es CREAR EL PLAYBOOK... No ejecutarlo. Quizás no seré yo ni quién lo ejecute.
                   # Yo se que puedo necesitar permisos elevados. Y lo que hago aqui simplemente es DECLARARLO!
                   # El cómo se elevan permisos se definirá cuando se vaya a ejecutar:
                   # - Es algo que puede cambiar con el tiempo
                   # - Es algo que puede incluso cambiar entre entornos (desarrollo, pruebas, producción)
                   # Es algo que cambia incluso etre tipos de entornos: windows vs linux
                   # Esto luego se define en 2 sitios:
                   # - O bien cuando ejecuto el playbook, y paso al comando de ejecución cómo se debe hacer la elevación de privilegios.
                   # - O a nivel del inventario, indicando para cada máquina o grupo de máquinas cómo se debe elevar privilegios.

                   # La buena práctica es poner este valor siempre en FALSE!
                   # Lastima que no lo quieten ya de aquí.

                   # MUY RARO , MUCHO es que todo lo que quiera hacer en un entorno requiera permisos elevados.
                   # Lo que hacemos es definir become a nivel de cada tarea concreta. Aquellas que requieren permisos elevados lo declaran explícitamente. 
  delegate_to: localhost
    # Dónde ejecuto las tareas del playbook... 
    # Los plays se ejecutan en un entorno con ansible.
    # Las tarea, por defecto, se ejecutan en los entornos remotos.
    # Hay escenarios donde me interesa que las tareas no se ejecuten en los remotos.
    # Solo quiero que se ejecuten en otro sitio diferente.
    # Caso de uso?
    # - Voy a montar un play para dar de alta en un sistema de monitorización mis hosts.
    # - Cuantas veces quiero que se ejecute la tarea: Asegurar que el host queda dado de alta en "datadog"? Una por cada host
    # - Necesito que la tarea se ejecute en el host? Es algo que vaya cambiar en el host? NO
    #   Lo que quiero es darlo de alta en el datadog.. no en el host remoto. Ni necesito llamar a datadog desde el host remoto.
    # Ejecuto el play por cada HOST, Cada ejecución lleva sus propias VARIABLES! pero no ejecuto las tareas sobre los entornos remotos (hosts).. las ejecuto sobre datadog.
    # Raro es que TODAS LAS TAREAS necesite que se ejecuten fuera del host. Lo normal es un híbrido.
    # - Instalo un agente de datadog en el host (ESTO ES DENTRO DEL HOST)
    # - Registro el host en datadog ( ESTO NO ES DENTRO DEL HOST)
    # Y lo normal de nuevo es no usar esta etiqueta A ESTE NIVEL (a nivel del play), sino a nivel de cada tarea.
    # Que cada tarea se haga responsable de DONDE DEBE EJECUTARSE.

# Tareas: Cada bloque contiene una lista SECUENCIAL de tareas

  pre_tasks:
    - name: Tarea1
      # Con su módulo
      notify:   Handler1 # NOMBRE_DEL_HANDLER (name) # Activar un handler/o varios ------> CUTRE !!!!! FEO !!!!! NO LO HACEMOS
    - name: Tarea2
      # Con su módulo
  tasks:
    - name: Tarea3. Soy una tarea que potencialmente CAMBIA EL FICHERO DE CONFIGURACION DE NGINX
      # Si yo estoy creando esta tarea... NO QUIERO PREOCUPARME (soC) AHORA de si necesito o no REINICIAR EL SERVIDOR o las otras 5   consecuencias del cambio de configuración
      #notify: Hacer esto me obliga a PENSAR EN COSAS AQUE AHORA NO QUIERO PENSAR.. COÑO, ESOY CMABIANDO LA CONFIGURACION DEL NGINX.. ES MI PEOCUPACION EN ESTE MOMENTO. Solo DIGO QUE COMO CONSECUENCIA DE MI ACTO, Se ha provocado un cambio en la configuración.
      # Otro problema será QUE DEBE OCURRIR COMO CONSECUENCIA DE ESE CAMBIO EN LA CONFIGURAICON...
      # Luego me meto con ello!
      #- Reiniciar el servicio
      #- Abrir nuevos puertos en el firewall
      # Con su módulo
      notify:  CAMBIO_EN_CONFIGURACION    # EVENTO  # Activar un handler/o varios. -------> GUAY!
    - name: Tarea4. Soy una tarea que potencialmente cambia la configuración del servicio de NGINX
      # Con su módulo
      notify:  CAMBIO_EN_CONFIGURACION    # EVENTO  # Activar un handler/o varios. -------> GUAY!
  post_tasks:
    - name: Tarea5
      # Con su módulo
    - name: Tarea6
      # Con su módulo

    # Cual es la diferencia o diferencias entre estas tres de arriba?
    # - El uso principal / diferencia principal NO ES FUNCIONAL. ES SEMANTICA!
    #   Significado para SERES HUMANOS... los que vendrán el día de mañana a ver por dentro el playbook, porque tengan que editarlo:
    #    - pre_tasks: Tareas necesarias para la ejecución del play
    #    >        Comprobar conectividad con el host remoto.. lo que pasa es que eso me lo regala ansoble.. y no tendre que hacerlo normalmente.
    #    >        Cortar la ejecución del play si estoy en un OS no soportado.
    #    >        Para hacer una prueba uso CURL. ***
    #             Por ende necesito? TENER CURL INSTALADO
    #             Necesito instalar CURL. El objetivo de mi play es instalar CURL? NO
    #             Pero me hace falta (DEPENDENCIA / REQUISITO)
    #    - tasks: Tareas propias del play
    #    >        Asegurar que unos entornos (Ubuntu/RHEL) tienen una determinada versión de nginx instalado
    #    >        Asegurar que el nginx tiene la configuración correcta
    #    >        Asegurar que la ultima versión de la web está desplegada
    #    >        Asegurar que los servicios necesarios están configurados correctamente
    #    - post_tasks: Tareas que pueden necesitar ejecutarse pero como añadido a las tareas principales de mi playbook
    #    >        Verificar que todo queda funcionando correctamente        IMPERATIVO *** PRUEBAS!!!!
    # - A nivel funcional solo una... que ahora después comento

    # Funcionaría todo esto, si en lugar de separar las tareas de esta forma, las meto todas en PRE_TASKS... y no pongo en mi play ninguna task ni ninguna post_task? SI... exactamente IGUAL! NO CAMBIA NADA!

    # La división es CONCEPTUAL / SEGUN LA TAREA Y LO QUE HAGA Y LA NECESIDAD DE LA MISMA (SEMANTICO)

    # Si hay una diferencia a nivel funcional... pero la explico cuando explique los handlers

  # Es una lista secuencial de tareas... cuyas tareas se ejecutan solo si:
  # - Cuando son ACTIVADOS por una tarea que HAYA PROVOCADO CAMBIOS EN EL SISTEMA REMOTO!
  handlers:
    - name: Handler1
      # Con su módulo
    - name: Reiniciar el NGINX
      # Con su módulo
      listen: CAMBIO_EN_CONFIGURACION
    - name: Handler3
      # Con su módulo
      listen: CAMBIO_EN_CONFIGURACION

    # Por qué trabajamos (nos gusta) con eventos y no con nombres?
    # Hay varios motivos:
    # - Facilita el desarrollo! PERMITE APLICAR el principio SoC
    # - Facilita el mantenimiento.
    #   Si cambio el nombre de un handler, no quiero tener que cambiar los 7 notify que apunmtan a él.

```
---

# Variables.. En cualquier lenguaje de programación. Para qué sirven?

Para guardar datos que CAMBIAN en tiempo de ejecución!

CONSTANTE: Para guardar datos que NO CAMBIAN en tiempo de ejecución.. cuándo cambian entonces? EN TIEMPO DE DESARROLLO.

Luego hay otro concepto qwue usamos en programación: 

ARGUMENTOS: Son los datos que se pasan a un programa o una función al momento de invocarlo.

Ansible a todo le llama VARIABLES! No distingue.
Eso simplifica... pero a su vez COMPLICA... porque hay más de 15 sitios en Ansible donde definir "VARIABLES" y no todos deberían usarse de la misma forma.
Dependiendo de si la "variable" de ansible es una variable, constante o argumento, las definimos en distintos lugares y con distintas prioridades.

---

# SoC (Separation of Concerns)

Edsjer Dijkstra fue quien popularizó el concepto de Separation of Concerns (SoC) en el desarrollo de software.

---

# Dónde se ejecutará el playbook?

Un playbook que instale / se asegure que queda instalado nginx en un servidor remoto.

En un entorno que tenga instalado ANSIBLE, que normalmente (al 100%) no va a ser el mismo servidor donde quiero instalar nginx.
- Será un servidor central de ansible o lo más normal hoy en día: UN CONTENEDOR EFIMERO!

Otra cosa es dónde ejecutan las tareas... y cúantas veces se ejecutan los plays que hay en el playbook.

Cuántas veces se ejecutan los plays del playbook?
Tantas como entornos haya en el inventario declarado al ejecutar el playbook.

Si un playbook tiene un play que ejecuta 5 tareas , y lo ejecuto sobre 10 servidores:
- El play se ejecuta 10 veces, una por cada servidor del inventario. Y el play se ejecuta en el entorno donde está instalado ansible.
- Para cada ejecución del play, se ejecutan las tareas que tenga definidas.
  - En nuestro caso cada play hemos dicho que tiene 5 tareas, y cada una de ellas se ejecuta 10 veces, una por cada servidor del inventario.
  - Y SE EJECUTAN DENTRO DEL ENTORNO REMOTO.
  - Por ejemplo, en el caso de linux, cómo me meto habitualmente en una máquina Linux? vía ssh.
  Pregunta... Cúantas conexiones ssh se van a abrir en este esceraio en total?
   - 1 por tarea em cada host... En nuestro caso 50 conexiones ssh en total.


ENTORNO CON ANSIBLE              |      Entornos remotos:       Entorno 1        Entorno 2    ... Entorno 6
---------------------------------|-----------------------------------------------------------------------------------
Ejecuto playbook                 |
 $ ansible-playbook playbook.yml |
 Crea un proceso ansible en      |
  este entorno                   |
                                 |
Ese proceso mira cúantos         |
remotos hay.                     |
Los agrupa en tandas...          |
Por defecto de 5 en 5            |
                                 |
TAREA1                           |
 ---                             |
  Entorno1  -----------------ssh--------------------------------> Módulo tarea1   
               Qué hace por ssh?
               El código del módulo es un programa python
               - Se manda ese código al remoto por red.
               - Se ejecuta ese programa en el entorno remoto.
                 con python * 
               - Ese programa genera respuesta JSON
               - que se manda al entorno de ejecución  
               - Cierra conexión ssh
                 Y así cada uno
  Entorno2
  Entorno3  ---------------ssh--------------------------------------------------------->
            <--------------json---------------------------------------------------------
  Entorno4
  Entorno5
  ---
  Entorno6

TAREA2
 ---
  Entorno1  -----------------ssh--------------------------------> Módulo tarea2
  Entorno2
  Entorno3  ---------------ssh--------------------------------------------------------->
            <--------------json---------------------------------------------------------
  Entorno4
  Entorno5
  ---
  Entorno6

---

* POR ESO ANSIBLE NECESITA QUE LOS ENTORNO REMOTOS TENGAN PYTHON!
---

# Estados de finalización de una tarea

Las tareas se van ejecutando para cada entorno remoto.
Y cada ejecución de cada tarea en cada entorno remoto acaba en un estado:
- OK:              La tarea acabó sin producir errores ni cambios en el sistema remoto
- CHANGED:         La tarea acabó sin producir errores y provocó cambios en el sistema remoto
- FAILED:          La tarea acabó con errores en el sistema remoto
- SKIPPED:         La tarea fue saltada y no se ejecutó en el sistema remoto
- UNREACHABLE:     No se pudo conectar al sistema remoto para ejecutar la tarea

Los módulos son los que POR DEFECTO (y podré cambiarlo y en muchos casos querré hacerlo) dicen el estado de finalización de la tarea según lo que ocurra en el sistema remoto.


---

# Ejecución de handlers:

```yaml
- name: Mi play de ejemplo
  hosts: all
  pre_tasks:
    - name: Tarea1
      # Con su módulo
      notify:   Handler1 # NOMBRE_DEL_HANDLER (name) # Activar un handler/o varios ------> CUTRE !!!!! FEO !!!!! NO LO HACEMOS
    - name: Tarea2
      # Con su módulo
  tasks:
    - name: Tarea3
      # Con su módulo
      notify:  CAMBIO_EN_CONFIGURACION    # EVENTO  # Activar un handler/o varios. -------> GUAY!
    - name: Tarea4
      # Con su módulo
      notify:  CAMBIO_EN_CONFIGURACION    # EVENTO  # Activar un handler/o varios. -------> GUAY!
  post_tasks:
    - name: Tarea5
      # Con su módulo
    - name: Tarea6
      # Con su módulo
      notify: CAMBIO_EN_CONFIGURACION
  handlers:
    - name: Handler1
      # Con su módulo
    - name: Handler2
      # Con su módulo
      listen: CAMBIO_EN_CONFIGURACION
    - name: Handler3
      # Con su módulo
      listen: CAMBIO_EN_CONFIGURACION
```
Al ejecutar, resulta que tanto Tarea1, Tomo tarea3 y tarea 4 provocan cambios.

Cuál sería el orden de ejecución final?
- Tarea1
- Tarea2
- Handler1
- Tarea3
- Tarea4
- Handler2
- Handler3
- Tarea5
- Tarea6
- Handler2
- Handler3

# Cuando y cómo se ejecutan los handlers?

Un handler se ejecuta COMO MUCHO UNA VEZ, aunque sea activado varias veces.
Es activado si una tarea que provoca cambio le notifica (por nombre o evento).
Pero su ejecución NO ES INMEDIATA. Se ejecuta después del bloque PRE, TASKS o POST correspondiente a la tarea que le activó.

De hecho, Un handler se ejecuta COMO MUCHO UNA VEZ, en cada bloque PRE, TASKS o POST donde haya sido activado.