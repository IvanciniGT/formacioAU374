# DO374 — Developing Advanced Automation with Red Hat Ansible Automation Platform

## Datos del curso

| Dato       | Valor                                         |
|------------|-----------------------------------------------|
| Fechas     | Del lunes 26 al viernes 30 de octubre de 2026 |
| Horario    | De 9:00 a 14:00                               |
| Plataforma | Red Hat Ansible Automation Platform 2.6       |

Red Hat lo ofrece ahora con el código **AU374**. DO374 es el nombre con el que
se conoció hasta las versiones anteriores de la plataforma.

## A quién va dirigido

A quien escribe automatización: desarrolladores, ingenieros DevOps,
administradores de sistemas Linux y otros profesionales de IT que ya han usado
Red Hat Ansible Automation Platform en entornos Linux.

## Requisitos previos

- Haber hecho el curso **Red Hat Enterprise Linux Automation with Ansible
  (AU294 / RH294)**.
- O tener la certificación **RHCE** en Red Hat Enterprise Linux 9 o posterior,
  o experiencia equivalente con Ansible.

## Objetivos

Al terminar el curso, el alumno será capaz de:

- Desarrollar *playbooks* con `ansible-navigator`.
- Aplicar las prácticas recomendadas para que la automatización sea eficaz.
- Trabajar con datos usando filtros y *plugins*.
- Hacer actualizaciones escalonadas, sin parar el servicio.
- Construir entornos de ejecución con todo lo que necesita el código de
  automatización.

## Contenidos

### 1. Develop Playbooks with Ansible Automation Platform 2

Escribir *playbooks* siguiendo las prácticas recomendadas.

### 2. Manage Ansible Content Collections and Automation Execution Environments

Ejecutar *playbooks* que usan colecciones que no vienen en ansible-core, ya
sea desde un entorno de ejecución existente o descargándolas del automation hub.

### 3. Run Playbooks with Automation Controller

Qué es el *automation controller* y cómo ejecutar en él los *playbooks*
desarrollados con `ansible-navigator`.

### 4. Work with Ansible Configuration Settings

Revisar y ajustar la configuración de Ansible y de `ansible-navigator` para
desarrollar más cómodo y resolver problemas.

### 5. Manage Inventories

Funciones avanzadas de los inventarios de Ansible.

### 6. Manage Task Execution

Controlar y optimizar cómo se ejecutan las tareas de los *playbooks*.

### 7. Transform Data with Filters and Plug-ins

Rellenar, transformar y gestionar los datos de las variables con filtros y
*plugins*.

### 8. Coordinate Rolling Updates

Hacer actualizaciones escalonadas que reduzcan la parada del servicio y
mantengan los *playbooks* sencillos y mantenibles.

### 9. Create Ansible Content Collections and Automation Execution Environments

Escribir colecciones propias, publicarlas, meterlas en un entorno de ejecución
a medida y usarlas en *playbooks* ejecutados desde el *automation controller*.

## El laboratorio

Cada alumno tiene su propio entorno de prácticas:

- Dos máquinas gestionadas, una **Rocky Linux** (compatible con RHEL) y una
  **Ubuntu**, para escribir *playbooks* que funcionen en distribuciones de
  familias distintas.
- **AWX** para ejecutar los *playbooks*. Es el proyecto de código abierto del
  que sale el *automation controller* de Red Hat Ansible Automation Platform.
- **Harbor** para guardar las imágenes de los entornos de ejecución.

Cómo se entra y cómo está montado se explica en el [README](../README.md) del
repositorio.
