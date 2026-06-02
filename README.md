# PFO 3 - Rediseño como Sistema Distribuido (Cliente-Servidor)

## Información académica

Instituto de Formación Técnica Superior N° 29

Tecnicatura Superior en Desarrollo de Software

Daniel Cordoba - 3°A - Año 2026
```
---

# Descripción

Rediseño del PFO N°2 hacia una arquitectura distribuida basada en sockets TCP.
La solución separa la aplicación en tres componentes:

* Cliente
* Servidor Central
* Workers
```
---

# Arquitectura del Sistema Original

```text
                 CLIENTES
                      │
                      ▼
       ┌─────────────────────────┐
       │     SERVIDOR TCP        │
       │       Puerto 5000       │
       └───────────┬─────────────┘
                   │
                   ▼
       ┌─────────────────────────┐
       │        WORKERS          │
       │       Puerto 5001       │
       │ ThreadPoolExecutor(5)   │
       └───────────┬─────────────┘
                   │
                   ▼
            ┌────────────┐
            │ SQLite DB  │
            └────────────┘
```

# Arquitectura Distribuida

```text
Clientes Web/Móvil
         │
         ▼
┌─────────────────┐
│ Balanceador     │
│ Nginx/HAProxy   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Servidor TCP    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ RabbitMQ        │
└────────┬────────┘
         │
 ┌───────┼─────────┐
 ▼       ▼         ▼
Worker1 Worker2 WorkerN
    \      |      /
     \     |     /
      ▼    ▼    ▼
 PostgreSQL / S3
```
---
# Tecnologías

* Python 3
* Sockets TCP
* SQLite
* JSON
* Threading
* ThreadPoolExecutor
* Werkzeug Security
```
---

# Funcionalidades

## Registro

Permite crear usuarios nuevos.
Las contraseñas son almacenadas utilizando hash seguro.

## Login

Valida credenciales almacenadas en la base de datos.

## Tareas

Permite acceder a una funcionalidad protegida luego de iniciar sesión.
```
---

# Concurrencia

## Servidor

Cada cliente es atendido mediante un hilo independiente.

## Workers

Los workers utilizan:

```python
ThreadPoolExecutor(max_workers=5)
```

para procesar múltiples solicitudes simultáneamente.
```
---

# Base de Datos

Tabla:

```sql
usuarios(
 id INTEGER PRIMARY KEY,
 usuario TEXT UNIQUE,
 password TEXT
)
```

---

# Ejecución

## 1. Iniciar Workers

```bash
python workers.py
```

## 2. Iniciar Servidor

```bash
python servidor.py
```

## 3. Iniciar Cliente

```bash
python cliente.py
```

---

# Flujo del Sistema

1. El cliente envía una solicitud.
2. El servidor la recibe.
3. El servidor deriva la tarea a un worker.
4. El worker procesa la solicitud.
5. El worker consulta la base de datos si es necesario.
6. El resultado vuelve al servidor.
7. El servidor responde al cliente.
```
---

# Capturas

## Terminal Cliente
<img width="940" height="235" alt="image" src="https://github.com/user-attachments/assets/768d100a-f6d3-42fb-b58f-f421b009a9c1" />

## Terminal Servidor
<img width="940" height="154" alt="image" src="https://github.com/user-attachments/assets/870d6ae7-5dba-4e36-be00-5eda2fc58384" />

## Terminal Workers
<img width="940" height="161" alt="image" src="https://github.com/user-attachments/assets/a24bab84-5643-4655-a70a-acbcf7272d8d" />

```
---
# Conclusión

El proyecto implementa exitosamente una arquitectura distribuida Cliente-Servidor-Worker mediante sockets TCP, incorporando concurrencia y separación de responsabilidades respecto de la solución monolítica desarrollada previamente.
