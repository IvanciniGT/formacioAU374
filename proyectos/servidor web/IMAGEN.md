# Construir y subir la imagen del entorno de ejecución

La imagen lleva todo lo que el playbook necesita para ejecutarse:
ansible-core, las colecciones y el role `instalacion_paquetes`. Se define en
dos ficheros de esta carpeta:

| Fichero                    | Qué dice                                              |
|----------------------------|-------------------------------------------------------|
| `execution-environment.yml` | Imagen base, ansible-core, ansible-runner, paquetes del sistema |
| `requirements.yml`         | Colecciones y roles, con versión fija                 |

Si cambia cualquiera de los dos, la imagen se reconstruye y **se sube con una
etiqueta nueva**.

## Antes de empezar

```bash
pip install ansible-builder      # una vez
open -a Docker                   # Docker Desktop suele estar parado
docker info --format '{{.ServerVersion}}'   # tiene que contestar una versión
```

## 1. Construir

Desde esta carpeta:

```bash
cd "proyectos/servidor web"

VERSION=1.0.1
IMAGEN=registry.ivanosuna.com/curso/ee-servidor-web:$VERSION

ansible-builder build \
  -f execution-environment.yml \
  --context /tmp/ee-servidor-web \
  --container-runtime docker \
  -t $IMAGEN
```

`--context` lleva fuera del repositorio el Dockerfile y los ficheros que
genera ansible-builder. Sin él los deja en una carpeta `context/` de aquí, y
acaban en un commit.

Tarda unos minutos la primera vez. La imagen pesa unos 500 MB.

## 2. Comprobar lo que lleva

Antes de subirla, que lleve lo que se espera:

```bash
docker run --rm ivanosuna.com/curso/ee-servidor-web:v1.2.0 bash -c '
  ansible --version | head -1
  ansible-galaxy collection list 2>/dev/null | grep -E "posix|general"
  ansible-galaxy role list 2>/dev/null | grep instalacion_paquetes'
```

Tiene que salir algo así:

```
ansible [core 2.20.10]
ansible.posix                            2.2.2
community.general                        13.5.0
- instalacion_paquetes, v1.0.1
```

## 3. Subir a Harbor

**Hace falta una cuenta con permiso para subir al proyecto `curso`.** Docker
en este Mac entra en Harbor como `admin`, que puede subir a cualquier proyecto.
Si `docker push` contesta `unauthorized`, es que no hay login o es de otra
cuenta, y se vuelve a entrar:

```bash
kubectl -n harbor get secret harbor-core -o jsonpath='{.data.HARBOR_ADMIN_PASSWORD}' \
  | base64 -d | docker login registry.ivanosuna.com -u admin --password-stdin
```

Basta con hacerlo una vez: queda guardado en el llavero de macOS.

```bash
docker push $IMAGEN
```

**Nada de `DOCKER_CONFIG` temporal ni de `docker logout` después.** En macOS,
Docker guarda el login en el llavero del sistema, que es UNO para todas las
configuraciones: un `docker login` desde una configuración temporal pisa el de
siempre, y el `docker logout` lo borra. Así se perdió el 23-10-2026 el login de
`robot$erp-ci`.

Comprobar que está:

```bash
curl -s "https://registry.ivanosuna.com/api/v2.0/projects/curso/repositories/ee-servidor-web/artifacts?with_tag=true" \
  | python3 -c 'import sys,json;[print([t["name"] for t in a["tags"]]) for a in json.load(sys.stdin)]'
```

El proyecto `curso` es público: **descargar no pide cuenta**. AWX la baja sin
credenciales.

También se ve en https://registry.ivanosuna.com, proyecto `curso`,
repositorio `ee-servidor-web`, con el informe de vulnerabilidades de Trivy.

## 4. Que AWX use la nueva

En AWX, **Execution Environments (Entornos de ejecución) → `alumno29-servidor-web`**, y en *Image* se
cambia la etiqueta a la nueva. La plantilla `alumno29-servidor-web` usa ese
entorno: el siguiente trabajo ya corre con la imagen nueva.

## Las etiquetas no se reutilizan

**Nunca se sube otra imagen con una etiqueta que ya existe.** El entorno de AWX
está en *pull: missing*: si ya tiene la imagen con esa etiqueta, no la vuelve a
descargar, y seguiría ejecutando la vieja sin avisar.

Se sigue el mismo criterio que con el role:

- **PATCH** (1.0.0 → 1.0.1): se reconstruye con lo mismo, o con un arreglo.
- **MINOR** (1.0.x → 1.1.0): una colección o un role nuevos, o una versión
  nueva de uno que ya estaba.
- **MAJOR** (1.x → 2.0.0): cambia ansible-core de serie o la imagen base.

| Versión | Qué lleva                                                     |
|---------|---------------------------------------------------------------|
| 1.0.0   | ansible-core 2.20.10, ansible.posix 2.2.2, community.general 13.5.0, instalacion_paquetes v1.0.0, sobre Fedora 43 |
| 1.1.0   | Lo mismo con instalacion_paquetes v1.0.1 |
| 1.1.1   | Lo mismo que la 1.1.0, reconstruida |
