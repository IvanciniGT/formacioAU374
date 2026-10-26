Es proyecto definirá un playbook que cuando acabe de ejecutarse:
- Me asegure que tengo un servidor web (nginx) instalado 
- Que ese nginx tenga la configuración que me interesa
- Que quede arrancado y configurado para arrancar automáticamente al iniciar el sistema.
- Y que me quede desplegada una web en el servidor (web que tendremos de un repo de Git).
- Debe funcionar tanto en RHEL como en Ubuntu.


Estimación inicial. Cuántas tareas vamos a necesitar?
- 10
- 12
- 15
- 30

A ver si tenemos suerte y acabamos con menos de 50.
LA IDEMPOTENCIA.... SALE CARA!
De paso, vamos a montar un playbook un poquito complicado... más que complicado REALISTA!
No vamos a montar un playbook de curso de youtube. Vamos a montar un playbook que sea apto para un entorno de producción en una empresa! Y HAY MUCHA DIFERENCIA!

Cuando empiezo a trabajar en un playbook, LOS MODULOS AL FINAL!
No son lo relevante, no pienso en ellos.
PIENSO EN TAREAS, TRABAJO, FLUJO!

---

Qué nginx instalo?
- La ultima estable? De repo oficial según distro? O del repo de nginx (que suele ir más adelantado en versiones?)
- La última estable realmente?

Quién decide la versión que hay que instalar de un programa?
LA VERSION LA MARCA LA FUNCIONALIDAD QUE NECESITO DE ESE PROGRAMA!
Esto en general lo sabe DESARROLLO, que es quien USA el software y conoce qué funcionalidades necesita.
A veces viene impuesto por POLITICAS DE LA EMPRESA (licencias...), y son lentejas.

Yo soy desarrollador y voy a usar una BBDD.. y necesito crear ciertos tipos de INDICES y usar ciertos tipos de consultas SQL.
En algunas versiones de mi motor de BBDD esa funcionalidad NO ESTARA DISPONIBLE y en otras si.

# Cómo funciona lo de la versiones de software?

Wordpress -> MySQL 5.7 pero no un MySQL 8.0 (no soportado)

Ls versiones en software habitualmente usan el ESQUEMA SEMANTICO: MAJOR.MINOR.PATCH (semver)

v A.B.C
                Cuándo suben esos numeritos?
- A major       Breaking changes: Cambios que rompen compatibilidad con versiones anteriores
                Básicamente quitar algo del programa (con o sin reemplazo) 
- B minor       Nueva funcionalidad
                Funcionalidad marcada como obsoleta (deprecated) 
                (Opcionalmente pueden venir arreglos de bugs... pero si solo se arreglan bugs, se subiría C patch)
- C patch       Cuando se arregla un bug! (o varios)

La funcionalidad de un sistema viene dada por la pareja:              MAJOR.MINOR
El patch refleja la cantidad de correcciones de bugs aplicadas.


WEBLOGIC 12c
Puedo pasar a WEBLOGIC 15c por las bravas? NO
Estoy cambiando MAJOR. Eso significa que estoy introduciendo cambios que rompen compatibilidad con versiones anteriores.
El primero de ellos:
WEBLOGIC 12 -> JAVA 1.8
WEBLOGIC 15 -> JAVA 17

Los programas que funcionaban en WEBLOGIC 12 NO VAN A FUNCIONAR DIRECTAMENTE EN WEBLOGIC 15, lo primero que necesito es recompilar y reescribir algunas cosas del código de esas apps que tengo desplegadas en el WEBLOGIC 12.

Yo no voy a montar un playbook que instale X o Y versión de un programa... La versión me la trae al peiro!
Yo voy a montar un playbook que instale nginx. CUAL ? NO ES MI PUÑETERA RESPONSABILDIAD.
QUE ME DIGAN CUAL! Te monto la que quieras

De qué repo instalo? NO ES MI RESPONSABILIDAD. QUE ME DIGAN CUAL! Te monto la que quieras.
Qué clave tiene ese repo? NO ES MI RESPONSABILIDAD. QUE ME DIGAN CUAL! Te monto la que quieras.

Aunque sea yo el que decida también eso... ES OTRO CONCEPTO.
En un rato, me pongo el gorro de quien decide la versión y el repo de nginx.
Pero ahora tengo el gorro del ti@ que está montando el playbook... y con este gorro, me la trae al peiro la version, el repo... las claves...!

El playbook no se casa con una versión del nginx.

Cómo nos dicen qué versión instalar?
DATO: Eso será un YAML que me van a pasar... de alguna forma.
Ese YAML habrá muchos sitios donde escribirlo.YA hablaremos de ello y veremos cuál es el que más nos interesa.
Por ahora, lo amos a poner en vars del playbook.

PREGUNTA: Qué estructura YAML (ESQUEMA) vamos a definir ahí? Eso es mio... es parte de mi playbook.. Y YO CREADOR DEL PLAYBOOK DECIDO LA FORMA EN LA QUE ME LLEGAN LOS DATOS (ESO SI ES MI REPSONSABILIDAD)

Necesitamos definir una estructura YAML para quenos den la info del nginx, repo, clave...

```yaml
nginx_version:      "a.b.c"
nginx_repo:         "http://example.com/nginx.repo"
nginx_repo_key:     "http://example.com/nginx.repo.key"
git_version:      "a.b.c"
git_repo:         "http://example.com/nginx.repo"
git_repo_key:     "http://example.com/nginx.repo.key"

nginx:
    version:      "a.b.c"
    repo:         "http://example.com/nginx.repo"
    repo_key:     "http://example.com/nginx.repo.key"
git:
    version:      "a.b.c"
    repo:         "http://example.com/nginx.repo"
    repo_key:     "http://example.com/nginx.repo.key"



nginx:
    version:
        name:          "a.b.c"           # Default que puede sobreescribirse a nivel de cada distro (o no)
        matching:      ">="              # = (= default)
    redhat:                              # Esta etiqueta es opcional (si se tira de repos oficiales y quiero la ultima version)
        version:      
            name:      "a.b.c"
            matching:  ">="
        repo:
            url:       "http://example.com/nginx.repo"
            key:       "http://example.com/nginx.repo.key"
    ubuntu:
        version:      
            name:      "a.b.c"      
            matching:  ">="              # La version también es opcional (si uso la de arriba)
        repo:                            # Repo es opcional si uso el oficial de la distro
            url:       "http://example.com/nginx.repo"
            key:       "http://example.com/nginx.repo.key"

git:
    version:      "a.b.c"
    ubuntu:
        version:      "a.b.d"
```


# Cuando se va a ejecutar este playbook?

- Cuando queramos desplegar un nginx y una web
- Cuando queramos actualizar la versión del nginx
- Cuando queramos actualizar la configuración del nginx (me cambian el puerto o el fqdn de la web)
- Cuando queremos actualizar la web
- Para arreglar el sistema si algún graciosillo ha entrado y ha borrado o cambiado algo que no debía
- Para pegarle un reinicio a mi nginx si se ha quedado colgado
- Para comprobar el correcto funcionamiento de mi nginx

QUE HACE EL PLAYBOOK? 
El playbook no hace un despliegue!
El playbook se asegura que todo está correcto.

Y esta es la magia de la IDEMPOTENCIA!

Respuesta más contundente y realista:  Cuando se va a ejecutar este playbook? NPI
Yo creo un plabook... Quien sabe donde acabará la cosa!

Quizás se va a enganchar a un sistema de monitorización, que cuando detecte que el nginx no contesta lo primero que hará será SOLICITAR LA REEJECUCION DEL PLAYBOOK (autocurado del entorno)... Si ya no cuela, que me avisen... pero y si cuela!

Una cosa es el objetivo inicial con el que hago el playbook... Quién sabe para que se usará esto en el futuro.
Y esa suposición de que el playbook lo hago para mi: NO PUEDO HACERLA NUNCA!
PORQUE SIEMPRE ES FALSA!
Quizás es apra mi hoy... dentro de semanas será para el pendejo que venga a calentar mi silla, que yo me haré pirado a otro lado!

ANSIBLE NO ES SOLO UNA NUEVA SINTAXIS PARA CREAR LOS SCRIPTS DE SIEMPRE.
PARA CREAR LOS SCRIPTS DE SIEMPRE SIGO CON LAS MISMAS HERRAMIENTAS DE SIEMPRE! NO QUIERO ANSIBLE
Cuando me vengo a ANSIBLE no es solo por la herramienta, es por la filosofía de la idempotencia y la automatización confiable que ofrece.

Y ESTA LA CLAVE!

Y este escenario nuevo....
Cuando yo reejecute mi playbook QUIERO SABER SI HA TOCADO ALGO O NO!
Quizás lo ejecuto de forma preventiva todos los dias a las 3am... por si hay una versión nueva de nginx o de la web (CONTINUOS DEPLOYMENT)
Y cuando se ejecute NECESITO SABER SI HA PROVOCADO CAMBIOS.... Porque si ha provocado cambios... NECESITO ESTAR OJO AVIZOR!

Oye.. ni que sea le voy a echar un ojito media hora (en la pantalla de monitorización.. que no haya problemas... yo que se. Lo mínimo para saber quesigue todo guay!)
Quiero que me avise ANSIBLE si se ha hecho un apt update en la máquina? NO... esto no me interesa controlarlo.
Me interesa saber si se ha instalado una nueva verisón del nginx, de la web, de la configuración o de cualquier otro componente crítico que gestione el playbook.

---

# Vamos a poner a funcionar un nginx... actuando como servidor web

Me dan una web , la despliego (copio los archivos de la web en una carpeta del host) y?
qué necesito hacer para que la web se sirva correctamente?

- Configurar el servidor web (nginx) para que sirva la web correctamente
    Hay unos datos a dar al nginx:
    - Ruta de la carpeta donde está la web
    - El puerto en el que debe servirla
    - El nombre del servidor (server_name) que debe responder por la web (fqdn)

    En el caso del nginx es crear un fichero de configuración.
    En ubuntu:
        /etc/nginx/sites-available/miweb
        Y creamos un enlace simbólico en /etc/nginx/sites-enabled:
    En redhat:
        /etc/nginx/conf.d/miweb.conf

    El archivo en los dos casos es igual:
    ```nginx
        server {
            listen 80;
            server_name app1.miempresa.com;
            root /var/www/miweb;

            location / {
                try_files $uri $uri/ =404;
            }
            // NGINX admite otros 500 parametros de configuración:
            // Tamaño máximo de upload
            client_max_body_size 10M;
            // Tiempo máximo de ejecución de una solicitud
            client_body_timeout 10s;
            // Tiempo máximo de espera para recibir el cuerpo de la solicitud
            client_body_timeout 10s;
            client_header_timeout 10s;

            // Configuración de logs
            access_log /var/log/nginx/miweb.access.log;
            error_log /var/log/nginx/miweb.error.log;
        }
    ```
La parte básica :
```nginx
    server {
        listen 80;
        server_name app1.miempresa.com;
        root /var/www/miweb;

        location / {
            try_files $uri $uri/ =404;
        }
    }
```
La puedo montar yo con que me den : fqdn, ruta de la web y puerto.
El resto me lo invento yo?  NO... eso me lo tienen que dar

- Abrir puertos en firewall


---

Cuando esté instalado....
Cómo accede un usuario a nuestra web?
http://app1.miempresa.com:80 
http://app2.miempresa.com:80


---

Vamos a meter pruebas para asegurar que el trabajo ha quedado bien.
Pruebas?
- curl http://app1.miempresa.com:80/salud
  Y contesta un 200 y aparece el texto: "El sitio está funcionando ok"
  Lo tenemos? SI.. Necesitamos alguna prueba adicional? DECENAS!

  Porque el problema no es que si la prueba anterior ha dado ok.
  El problema es si da KO... si da KO qué ha fallado? LO SABEMOS? NO

Y el tema es cuando prefiero averiguarlo:
- Ahora que tranquilamente estoy montando el playbook
- O cuando el sistema se despliegue un día X en producción y falle y haya que arreglarlo? Con toda la presión?

Un dia fallará . FIJO: Ley de Murphy
El tema es que 100% HABRA QUE AVERIGUARLO!

Pruebas que vamos a hacer a día de HOY:
- Si el proceso está corriendo
- Si el host está accesible desde fuera (por ejemplo, desde mi máquina local)
- Si el puerto está escuchando (desde donde?) en local
- Si consigo llegar al puerto desde fuera (FIREWALL)
- Si el dns está bien configurado

# TAGS

Qué tipos de tareas hace nuestro playbook? Es decir, tareas de naturalezas distintas:
- prueba
- instalacion
- configuracion
- despliegue
- always (Ese tag es especial... es un nombre reservado de ansible)
  Aunque me pidan ejecutar solo ciertas tarea (tags), las que tengan el tag always se ejecutarán siempre.


---

# Instalaciones

Necesitamos instalar:
- dependencias:
  - git
  - curl
  - rsync
- nginx

Cada cosa que quiera instalar (paquete) va a requerir del mismo trabajo:
- Dar de alta claves
- Dar de alta repos... o no... depende de si los han configurado previamente en los datos que nos pasan
- Actualizar repos
- Hacer la instalación

Y además, estamos lidiando con Redhat y Ubuntu... 
Esas tareas se hacen igual en un redhat y un ubuntu? NO


Nos interesará tener:
- Un conjunto de tareas que sepan instalar un paquete en Redhat  (repos, claves, install...)
- Un conjunto de tareas que sepan instalar un paquete en Ubuntu  (repos, claves, install...)
- Una tarea a la que le pueda pedir instalar un paquete y ya dependiendo de la distro invoque las tareas correspondientes (Redhat o Ubuntu)
- Y esa tarea la puedo llamar normal para el nginx o en bucle para las dependencias 

Lo que en programación tradicional sería CREARME FUNCIONES!
    installPaqueteEnUbuntu
    installPaqueteEnRedhat

    installPaquete
        -> installPaqueteEnUbuntu o installPaqueteEnRedhat dependiendo de la distro

    puedo llamar a la funcion para nginx
    puedo llamar a la funcion en bucle para las dependencias

En Ansible no existe el concepto de función
Pero lo podemos hacer bien con el include_tasks de Ansible.
    Incluyo un fichero de tareas que contega la lógica para instalar un paquete en la distro correspondiente (Redhat o Ubuntu)
    A su vez ese incluye el fichero de tareas de ubuntu o redhat según corresponda

De alguna forma, esos ficheros que voy a crear son "FUNCIONES"


# Despliegue de la web:

- Descargar el repositorio de git en local. La última versión (No consideramos un cambio en la máquina que se haga).
  - MODULO git
  Esa descarga la haremos en una carpeta temporal
      /tmp/web
- Nos aseguramos que existe la carpeta real de despliegue de la app (la da ahora mismo el usuario que ejecuta el playbook)
      /var/www/myapp
      MODULO file
- Miramos si hay diferencias entre lo descargado y lo que ya está desplegado en la carpeta real de la app.
  NOTA: en tmp/web habrá una carpeta llamada .git que es de git y que no queremos copiar a la carpeta real de despliegue.
  Pero en cualquier caso, NO QUEREMOS HACER LA COPIA AUN.. solo ver si hay diferencias:
    rsync (MODO --dry-run)
      MODULO synchronize
- Caso que haya diferencias, backup de lo que hay actualmente en     
  la carpeta real de despliegue (/var/www/myapp).
  Podemos llevarlos a ~/home/<usuario>~/backups/ o alguna carpeta similar para tener un historial de backups.
  Los backpus comprimidos y el archivo en su nombre con un timestamp.
    MODULO archive
- Una vez hecho el backup, podemos proceder a copiar los archivos desde /tmp/web a /var/www/myapp.
    MODULO synchronize

# Nos faltan más cosas:

- Configurar el arranque de servicio automático
- Reiniciar el servicio web si hay cambios en la configuración o en los archivos desplegados.
   MODULE : service
   Se asegura de que el servicio web esté en ejecución y habilitado para el arranque automático.

# Opcional!
- Si estamos en redhat y hay firewalld activo, asegurarnos de abrir el puerto correspondiente para el servicio web.
- Si estamnos en ubuntu y hay ufw activo, asegurarnos de abrir el puerto correspondiente para el servicio web.