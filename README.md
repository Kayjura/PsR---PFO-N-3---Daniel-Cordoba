# PFO 3 - Rediseño como Sistema Distribuido (Cliente-Servidor)

## Información académica

Instituto de Formación Técnica Superior N° 29

Tecnicatura Superior en Desarrollo de Software

Daniel Cordoba - 3°A - Año 2026

---

# Descripción

Este proyecto corresponde al rediseño de la solución desarrollada en la PFO 2 hacia una arquitectura distribuida basada en sockets TCP utilizando Python.

La aplicación implementa un modelo Cliente - Servidor - Workers donde:

* Los clientes envían solicitudes.
* El servidor central recibe y distribuye tareas.
* Los workers procesan las solicitudes.
* La información se almacena en una base de datos SQLite compartida.

El objetivo es desacoplar la recepción de solicitudes de su procesamiento, permitiendo una arquitectura más escalable y concurrente.

---

# Arquitectura Implementada

## Diagrama del Sistema

```text
                           CLIENTE
                              │
                              │
                              ▼

              ┌──────────────────────────┐
              │     SERVIDOR TCP         │
              │       Puerto 5000        │
              │                          │
              │      Round Robin         │
              └────────────┬─────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼

   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
   │  WORKER 1   │ │  WORKER 2   │ │  WORKER 3   │
   │ Puerto 5001 │ │ Puerto 5002 │ │ Puerto 5003 │
   │ Pool x 5    │ │ Pool x 5    │ │ Pool x 5    │
   └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
          │               │               │
          └───────────────┼───────────────┘
                          │
                          ▼

                ┌──────────────────┐
                │    SQLite DB     │
                │   usuarios.db    │
                └──────────────────┘
```

---

# Arquitectura Objetivo Solicitada por la Consigna

La consigna solicita una arquitectura distribuida completa que incluya balanceador de carga, cola de mensajes y almacenamiento distribuido.

```text
Clientes
    │
    ▼
Balanceador de Carga
(Nginx / HAProxy)
    │
    ▼
Servidor Central
    │
    ▼
RabbitMQ
    │
 ┌──┼──┐
 ▼  ▼  ▼
W1 W2 WN
    │
    ▼
PostgreSQL / S3
```

La implementación desarrollada representa una versión simplificada y funcional de dicho modelo, manteniendo el concepto de distribución de tareas entre múltiples workers.

---

# Tecnologías Utilizadas

* Python 3
* Sockets TCP
* JSON
* SQLite
* Threading
* ThreadPoolExecutor
* Werkzeug Security

---

# Componentes

## Cliente

Archivo:

```text
cliente.py
```

Responsabilidades:

* Registro de usuarios.
* Inicio de sesión.
* Solicitud de tareas.
* Recepción de respuestas.

---

## Servidor

Archivo:

```text
servidor.py
```

Responsabilidades:

* Escuchar conexiones entrantes.
* Atender múltiples clientes.
* Distribuir solicitudes mediante Round Robin.
* Reenviar respuestas.

---

## Workers

Archivo:

```text
workers.py
```

Responsabilidades:

* Procesamiento de solicitudes.
* Registro de usuarios.
* Validación de credenciales.
* Consulta de información.
* Acceso a base de datos.

Cada worker se ejecuta en un puerto independiente:

| Worker   | Puerto |
| -------- | ------ |
| Worker 1 | 5001   |
| Worker 2 | 5002   |
| Worker 3 | 5003   |

---

# Balanceo de Carga

El servidor implementa un algoritmo Round Robin.

Cada solicitud se distribuye secuencialmente entre los workers disponibles:

```text
Solicitud 1 → Worker 5001
Solicitud 2 → Worker 5002
Solicitud 3 → Worker 5003
Solicitud 4 → Worker 5001
...
```

Esto permite repartir la carga de trabajo entre múltiples procesos.

---

# Concurrencia

## Servidor

Cada cliente es atendido mediante un hilo independiente:

```python
threading.Thread(...)
```

## Workers

Cada worker utiliza:

```python
ThreadPoolExecutor(max_workers=5)
```

permitiendo procesar varias solicitudes simultáneamente.

---

# Base de Datos

Se utiliza SQLite como almacenamiento persistente.

Tabla principal:

```sql
usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE,
    password TEXT
)
```

Las contraseñas se almacenan utilizando hash seguro mediante Werkzeug.

---

# Funcionalidades

## Registro

Permite registrar nuevos usuarios.

---

## Login

Valida usuario y contraseña.

---

## Consulta de Estadísticas

Permite consultar:

* Worker que procesó la solicitud.
* Cantidad de usuarios registrados.

Ejemplo:

```json
{
    "status": 200,
    "worker": 5002,
    "usuarios_registrados": 15
}
```

---

# Ejecución

## 1. Iniciar Worker 1

```bash
python workers.py 5001
```

## 2. Iniciar Worker 2

```bash
python workers.py 5002
```

## 3. Iniciar Worker 3

```bash
python workers.py 5003
```

## 4. Iniciar Servidor

```bash
python servidor.py
```

## 5. Iniciar Cliente

```bash
python cliente.py
```

---

# Flujo de Funcionamiento

1. El cliente envía una solicitud.
2. El servidor recibe la conexión.
3. El servidor selecciona un worker mediante Round Robin.
4. El worker procesa la tarea.
5. El worker consulta la base de datos si es necesario.
6. El resultado vuelve al servidor.
7. El servidor responde al cliente.

---

# Evidencia de Distribución

Las respuestas muestran qué worker procesó cada solicitud:

```json
{
    "worker": 5001
}
```

```json
{
    "worker": 5002
}
```

```json
{
    "worker": 5003
}
```

Demostrando que las tareas son distribuidas entre múltiples workers.

---

# Conclusión

La solución implementa una arquitectura distribuida Cliente-Servidor-Workers basada en sockets TCP.

El servidor central distribuye tareas entre múltiples workers utilizando Round Robin, cada worker procesa solicitudes concurrentemente mediante un pool de hilos y la información se almacena en una base de datos compartida.

Este rediseño permite desacoplar responsabilidades, mejorar la escalabilidad y aproximarse al modelo distribuido solicitado en la consigna.

---

# Capturas

## Terminal Cliente
<img width="940" height="235" alt="image" src="https://github.com/user-attachments/assets/768d100a-f6d3-42fb-b58f-f421b009a9c1" />

## Terminal Servidor
<img width="940" height="154" alt="image" src="https://github.com/user-attachments/assets/870d6ae7-5dba-4e36-be00-5eda2fc58384" />

## Terminal Worker 1
<img width="940" height="161" alt="image" src="https://github.com/user-attachments/assets/a24bab84-5643-4655-a70a-acbcf7272d8d" />

## Terminal Worker 2

## Terminal Worker 3