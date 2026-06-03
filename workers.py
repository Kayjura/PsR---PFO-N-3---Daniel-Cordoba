import socket
import json
import sqlite3
import sys

from concurrent.futures import ThreadPoolExecutor

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

HOST = "127.0.0.1"

if len(sys.argv) != 2:
    print("Uso: python workers.py <puerto>")
    sys.exit(1)

PORT = int(sys.argv[1])

DB = "usuarios.db"


def init_db():
    """
    Crea la base de datos y la tabla usuarios
    si todavía no existen.
    """

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def registrar_usuario(usuario, password):

    conn = None

    try:

        conn = sqlite3.connect(DB)

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO usuarios(usuario,password)
            VALUES(?,?)
            """,
            (
                usuario,
                generate_password_hash(password)
            )
        )

        conn.commit()

        return {
            "status": 201,
            "mensaje": "Usuario registrado correctamente",
            "worker": PORT
        }

    except sqlite3.IntegrityError:

        return {
            "status": 400,
            "error": "El usuario ya existe",
            "worker": PORT
        }

    except Exception as e:

        return {
            "status": 500,
            "error": str(e),
            "worker": PORT
        }

    finally:

        if conn:
            conn.close()


def login_usuario(usuario, password):

    conn = None

    try:

        conn = sqlite3.connect(DB)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT password
            FROM usuarios
            WHERE usuario = ?
            """,
            (usuario,)
        )

        resultado = cursor.fetchone()

        if resultado and check_password_hash(
            resultado[0],
            password
        ):

            return {
                "status": 200,
                "mensaje": "Login exitoso",
                "worker": PORT
            }

        return {
            "status": 401,
            "error": "Credenciales inválidas",
            "worker": PORT
        }

    except Exception as e:

        return {
            "status": 500,
            "error": str(e),
            "worker": PORT
        }

    finally:

        if conn:
            conn.close()


def obtener_estadisticas():

    conn = None

    try:

        conn = sqlite3.connect(DB)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM usuarios
            """
        )

        total = cursor.fetchone()[0]

        return {
            "status": 200,
            "worker": PORT,
            "usuarios_registrados": total,
            "mensaje": "Consulta realizada correctamente"
        }

    except Exception as e:

        return {
            "status": 500,
            "error": str(e),
            "worker": PORT
        }

    finally:

        if conn:
            conn.close()


def procesar_solicitud(conn, addr):

    try:

        data = conn.recv(4096)

        if not data:

            conn.close()
            return

        request = json.loads(
            data.decode()
        )

        action = request.get("action")

        if action == "registro":

            response = registrar_usuario(
                request.get("usuario"),
                request.get("contraseña")
            )

        elif action == "login":

            response = login_usuario(
                request.get("usuario"),
                request.get("contraseña")
            )

        elif action == "tareas":

            response = obtener_estadisticas()

        else:

            response = {
                "status": 400,
                "error": "Acción inválida",
                "worker": PORT
            }

        conn.sendall(
            json.dumps(response).encode()
        )

    except json.JSONDecodeError:

        response = {
            "status": 400,
            "error": "JSON inválido",
            "worker": PORT
        }

        conn.sendall(
            json.dumps(response).encode()
        )

    except Exception as e:

        response = {
            "status": 500,
            "error": str(e),
            "worker": PORT
        }

        conn.sendall(
            json.dumps(response).encode()
        )

    finally:

        conn.close()


def start_worker():

    init_db()

    worker = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    worker.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    worker.bind(
        (HOST, PORT)
    )

    worker.listen()

    print(
        f"[WORKER {PORT}] Escuchando conexiones..."
    )

    with ThreadPoolExecutor(
        max_workers=5
    ) as executor:

        while True:

            conn, addr = worker.accept()

            print(
                f"[WORKER {PORT}] "
                f"Solicitud recibida desde {addr}"
            )

            executor.submit(
                procesar_solicitud,
                conn,
                addr
            )


if __name__ == "__main__":

    print(
        f"Iniciando Worker en puerto {PORT}"
    )

    start_worker()