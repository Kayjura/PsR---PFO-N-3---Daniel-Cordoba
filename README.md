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

Arquitectura distribuida completa con balanceador de carga, cola de mensajes y almacenamiento distribuido.

```text

╭──────────────────────────────────────────────────────────╮
│      PFO 3 - REDISEÑO COMO SISTEMA DISTRIBUIDO           │
╰──────────────────────────────────────────────────────────╯

                      👤 CLIENTE
                           │
                           │ TCP
                           ▼
╭──────────────────────────────────────────────────────────╮
│                  SERVIDOR CENTRAL                        │
│                      Puerto 5000                         │
│                                                          │
│  • Recibe solicitudes de clientes                        │
│  • Gestiona conexiones concurrentes                      │
│  • Distribuye tareas mediante Round Robin                │
╰─────────────────────────┬────────────────────────────────╯
                          │
                          ▼

              BALANCEO DE CARGA (ROUND ROBIN)

            ┌──────────────┬──────────────┬
            │              │              │              
            ▼              ▼              ▼
╭────────────────╮╭────────────────╮╭────────────────╮
│    WORKER 1    ││    WORKER 2    ││    WORKER 3    │
│                ││                ││                │
│ Puerto 5001    ││ Puerto 5002    ││ Puerto 5003    │
│                ││                ││                │
│ Pool 5 Threads ││ Pool 5 Threads ││ Pool 5 Threads │
╰───────┬────────╯╰───────┬────────╯╰───────┬────────╯
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                          ▼
╭──────────────────────────────────────────────────────────╮
│                    BASE DE DATOS                         │
│                       SQLite                             │
│                                                          │
│  • Usuarios                                              │
│  • Contraseñas cifradas (hash)                           │
│  • Estadísticas                                          │
╰──────────────────────────────────────────────────────────╯


```

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
<img width="940" height="351" alt="image" src="https://github.com/user-attachments/assets/77d5c1f2-2503-42b9-8450-6c094c304d4d" />

## Terminal Servidor
<img width="940" height="234" alt="image" src="https://github.com/user-attachments/assets/67163f04-70d4-4441-8e9c-4ff53ba2b6b0" />

## Terminal Worker 1
<img width="940" height="234" alt="image" src="https://github.com/user-attachments/assets/fc9b24da-3f36-4ab3-a757-256bc9aac2fa" />

## Terminal Worker 2
<img width="940" height="207" alt="image" src="https://github.com/user-attachments/assets/19168164-844e-49e3-8d45-1f64738e9b3f" />

## Terminal Worker 3
<img width="940" height="199" alt="image" src="https://github.com/user-attachments/assets/593cdc8b-4788-493d-87a5-6ae672565b76" />
