# instalador_paquete_concreto

Role de Ansible que **asegura que un paquete queda instalado** en un host
Debian/Ubuntu o RHEL/Rocky. Si se le da un repositorio y su clave, los da de
alta primero. Si se le da una versión, instala esa versión o una que cumpla la
condición pedida.

Para quien lo llama son siempre los mismos cuatro pasos, en cualquier
distribución:

1. Dar de alta el repositorio y su clave, si se los han dado.
2. Actualizar la caché de paquetes.
3. Instalar el paquete en la versión pedida.

Lo que cambia por debajo (dnf o apt, `.repo` o `.sources`, `nginx-1.20` o
`nginx=1.20`) es cosa del role.

```yaml
- name: Asegurar que git está instalado, en la 2.30 o superior
  ansible.builtin.include_role:
    name: instalador_paquete_concreto
  vars:
    paquete:          git
    version:          "2.30"
    operador_version: ">="
```

---

## Requisitos

| Qué                    | Por qué                                                         |
|------------------------|-----------------------------------------------------------------|
| ansible-core 2.15 o más | Lo mínimo con lo que se ha escrito. Probado con la 2.20         |
| `become` en el host    | Instalar paquetes y tocar repositorios pide ser superusuario   |
| Python en el host      | Como cualquier módulo de Ansible                                |

**No necesita ninguna colección**: todo es `ansible.builtin`.

En Debian/Ubuntu **tampoco necesita `python3-apt` ni `python3-debian` de
antemano** para dar de alta un repositorio. El role escribe el fichero
`.sources` y descarga la clave él mismo, en vez de usar `apt_repository` o
`deb822_repository`, que los piden. Una imagen mínima de Ubuntu no los trae.

### Distribuciones

| Familia | Probado en       | Gestor | Repositorio                          |
|---------|------------------|--------|--------------------------------------|
| RedHat  | Rocky Linux 9    | dnf    | `/etc/yum.repos.d/<paquete>.repo`    |
| Debian  | Ubuntu 24.04     | apt    | `/etc/apt/sources.list.d/<paquete>.sources` |

En cualquier otra familia el role **falla al principio**, con un mensaje que
dice cuál es. No intenta adivinar.

---

## Argumentos

| Argumento          | Obligatorio | Por defecto | Qué es                                         |
|--------------------|:-----------:|-------------|------------------------------------------------|
| `paquete`          | **sí**      |             | Nombre del paquete: `nginx`, `git`...          |
| `version`          | no          | `""`        | Versión. Vacía: la última disponible           |
| `operador_version` | no          | `"="`       | `=`, `>=`, `<=`, `>` o `<`                     |
| `repositorio`      | no          | `""`        | URL del repositorio. Vacía: los oficiales      |
| `clave`            | no          | `""`        | URL de la clave GPG del repositorio            |
| `suite`            | no          | `""`        | Solo Debian/Ubuntu. Vacía: la de la versión del host |
| `componentes`      | no          | `[main]`    | Solo Debian/Ubuntu: componentes del repositorio |

Los argumentos **se validan antes de la primera tarea**
(`meta/argument_specs.yml`). Un operador mal escrito, como `=>`, o un paquete
vacío fallan ahí, con un mensaje claro. Si no, el fallo saldría a mitad de un
`dnf`, con un error del gestor de paquetes.

### Lo que no se da, se pasa vacío, no con `omit`

Es el error más fácil de cometer con este role, y no avisa:

```yaml
# MAL
vars:
  version: "{{ mi_version | default(omit) }}"

# BIEN
vars:
  version: "{{ mi_version | default('') }}"
```

`omit` solo funciona en los parámetros de un módulo. En los `vars:` de un
`include_role` no quita la variable: le pone un texto como
`__omit_place_holder__5f3a...`. El role lo recibe como si fuera una versión e
intenta instalar `nginx-__omit_place_holder__5f3a...`.

### La versión, en cada gestor

| Lo que pides                          | dnf (RedHat)    | apt (Debian)    |
|---------------------------------------|-----------------|-----------------|
| `version: ""`                         | `nginx`         | `nginx`         |
| `version: "1.20.1"`, `operador_version: "="` | `nginx-1.20.1`  | `nginx=1.20.1`  |
| `version: "1.20"`, `operador_version: ">="`  | `nginx >= 1.20` | `nginx>=1.20`   |

Con `=` la comparación es **exacta**, y la versión de un paquete Debian lleva
la revisión del empaquetador: `1.24.0-2ubuntu7`, no `1.24.0`. Para «cualquier
1.24» se usa un comodín: `version: "1.24*"`. En dnf vale lo mismo:
`version: "1.20*"`.

### Con versión, siempre la más nueva que la cumpla

Cuando se da una versión, el paquete se instala con `state: latest`: **la más
nueva disponible que cumpla la condición**, y en cada ejecución. Si mañana sale
una que también la cumple, la siguiente ejecución la instala.

`present` no sirve, porque no actualiza lo que ya está instalado. Con dnf, una
nginx 1.20 instalada se da por buena aunque se pida `>= 1.26`, sin ningún
error.

dnf y apt no saben nada de versionado semántico: solo comparan números. Así que
`>=` no se para en ninguna MAJOR:

| `version` | `operador_version` | Instala, y va subiendo a        |
|-----------|--------------------|---------------------------------|
| `2.4.1`   | `=`                | la 2.4.1, y de ahí no se mueve  |
| `2.4*`    | `=`                | la última 2.4.x: solo parches   |
| `2.*`     | `=`                | la última 2.x: minors y parches |
| `2.4`     | `>=`               | la última que haya, **3.0 incluida** |

Para seguir una rama sin saltar de MAJOR, `=` con comodín. Comprobado con dnf
en Rocky 9 y con apt en Ubuntu 24.04.

**Sin versión no se actualiza nada.** Si no se pide ninguna, el paquete se
instala con `present`, y lanzar el playbook no cambia la versión que haya.

### El repositorio, en cada gestor

La misma URL no significa lo mismo en los dos:

- **RedHat**: es la `baseurl`, la carpeta donde están los paquetes. Admite las
  variables de dnf: `https://nginx.org/packages/centos/$releasever/$basearch/`.
  **No es** la URL de un fichero `.repo`.
- **Debian/Ubuntu**: es la URI del repositorio:
  `https://nginx.org/packages/ubuntu`. La *suite* la pone el role con el
  nombre en clave de la versión del host (`noble`, `jammy`...), así que el
  mismo argumento vale para todas. Si el repositorio usa una fija, como
  `stable`, se le pasa en `suite`. Los componentes salen de `componentes`.

En RedHat el repositorio se da de alta con `module_hotfixes: true`. En RHEL 8
y 9 muchos paquetes, nginx entre ellos, existen también como módulos de
AppStream, y dnf esconde los de otros repositorios que se llamen igual. Sin
esa opción, el repositorio queda configurado y dnf sigue instalando la versión
del módulo. No da ningún error.

En Debian/Ubuntu, una clave dada se descarga en `/etc/apt/keyrings/` y el
repositorio se firma con ella (`Signed-By`). apt distingue el formato **por la
extensión**: `<paquete>.gpg` si la URL de la clave acaba en `.gpg`, que es una
clave binaria, y `<paquete>.asc` en cualquier otro caso, que es texto. Una
clave binaria guardada como `.asc`, apt la ignora y el repositorio falla con `NO_PUBKEY`, como si no tuviera clave.

---

## Ejemplos

### Lo más simple: el de la distribución, el último

```yaml
- name: Asegurar que tree está instalado
  ansible.builtin.include_role:
    name: instalacion_paquetes
  vars:
    paquete: tree
```

### Desde un repositorio propio, con clave

El mismo paquete en las dos familias, cada una con su repositorio. Lo normal es
que estos datos vengan del inventario, por grupo:

```yaml
# group_vars/redhat.yaml
nginx_repo: "https://nginx.org/packages/centos/$releasever/$basearch/"

# group_vars/debian.yaml
nginx_repo: "https://nginx.org/packages/ubuntu"
nginx_componentes: [nginx]
```

```yaml
- name: Asegurar que nginx está instalado desde nginx.org
  ansible.builtin.include_role:
    name: instalacion_paquetes
  vars:
    paquete:          nginx
    version:          "1.26"
    operador_version: ">="
    repositorio:      "{{ nginx_repo }}"
    clave:            https://nginx.org/keys/nginx_signing.key
    componentes:      "{{ nginx_componentes | default(['main']) }}"
```

### Varios paquetes, en bucle

`include_role` admite `loop`; `roles:` e `import_role`, no. Es la razón para
llamarlo así:

```yaml
- name: Asegurar que las dependencias están instaladas
  ansible.builtin.include_role:
    name: instalacion_paquetes
  vars:
    paquete:          "{{ dependencia.key }}"
    version:          "{{ dependencia.value.version | default('') }}"
    operador_version: "{{ dependencia.value.operador | default('=') }}"
  loop: "{{ dependencias | dict2items }}"
  loop_control:
    loop_var: dependencia
  # Ojo: loop_var con un nombre propio. Con el `item` de siempre, un bucle
  # dentro del role chocaría con el de fuera.
```

```yaml
dependencias:
  git:   { version: "2.30", operador: ">=" }
  tree:  {}
  rsync: {}
```

---

## Etiquetas

Todas las tareas del role llevan `always`: **si se le incluye, hace el trabajo
entero**. Qué etiqueta activa la instalación lo decide quien lo llama, en su
`include_role`:

```yaml
- name: Asegurar que nginx está instalado
  ansible.builtin.include_role:
    name: instalacion_paquetes
    apply:
      tags: [instalacion]
  vars:
    paquete: nginx
  tags: [instalacion]
```

Las dos `tags` hacen falta, y por motivos distintos. La de fuera es la del
propio `include_role`: sin ella, un `--tags instalacion` se lo salta. La de
`apply` se la pone a las tareas de dentro.

## Facts

El role **no necesita `gather_facts`**. Si quien lo llama no ha recogido la
familia del sistema operativo, la pide él, y nada más (`gather_subset:
distribution`). Un `gather_facts` completo tarda, y aquí no hace falta.

## Idempotencia

Una segunda ejecución sin cambios termina **sin ningún `changed`**. Con una
excepción buscada: si se ha pedido una versión y desde la última ejecución ha
salido otra que la cumple, se instala y sale `changed`. Ese `changed` es justo
el que interesa ver.

El `apt update` lleva `changed_when: false`. Actualizar la caché sí cambia la
máquina, pero no es un cambio que interese controlar. Si contara, cada
ejecución diría que ha tocado algo, y un cambio de verdad pasaría desapercibido
entre los falsos.

Para no hacer un `apt update` por paquete, la caché vale una hora. La excepción
es cuando el role acaba de dar de alta un repositorio: entonces actualiza sí o
sí, porque la caché vieja no lo conoce.

---

## Cómo se usa desde un playbook

El role no se copia dentro del playbook. Se declara como dependencia en el
`requirements.yml` del playbook, **con la versión fijada a una etiqueta**:

```yaml
roles:
  - name:    instalacion_paquetes
    src:     git+https://github.com/IvanciniGT/ansible-role-instalacion_paquetes.git
    version: "v1.0.0"
```

El `name` tiene que ser `instalacion_paquetes`. Es el nombre con el que lo
buscan los `include_role`, y sin él ansible-galaxy lo guardaría con el nombre
del repositorio.

Una etiqueta y no `main`, porque una rama se mueve: el mismo
`requirements.yml` instalaría otra cosa cada semana.

Ese `requirements.yml` se instala **dentro de la imagen del entorno de
ejecución**, con `ansible-builder`, no en el portátil ni en AWX. Así el
playbook corre con el mismo role en todos los sitios.

Para desarrollar en local sin construir la imagen:

```bash
ansible-galaxy role install -r requirements.yml -p roles/
```

## Versiones

Se sigue [versionado semántico](https://semver.org/lang/es/):

- **MAJOR**: cambia la interfaz. Se quita o se renombra un argumento, o cambia
  lo que significa.
- **MINOR**: algo nuevo que no rompe a nadie, como un argumento opcional o una
  distribución más.
- **PATCH**: un arreglo.

Cada versión publicada es una etiqueta `vX.Y.Z`. **Una etiqueta publicada no se
mueve nunca**: hay imágenes construidas con ella.

## Licencia

MIT

## Autor

Iván Osuna Ayuste — formación en Ansible, Kubernetes, Java y Angular.
