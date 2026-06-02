import socket
import json
import sqlite3

from concurrent.futures import ThreadPoolExecutor

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

HOST = "127.0.0.1"
PORT = 5001

DB = "usuarios.db"


def init_db():

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


def procesar_tarea(conn, addr):

    try:

        data = conn.recv(4096)

        request = json.loads(data.decode())

        action = request.get("action")

        response = {
            "status": 400,
            "Error": "Acción inválida"
        }

        if action == "registro":

            usuario = request.get("usuario")
            password = request.get("contraseña")

            if not usuario or not password:

                response = {
                    "status": 400,
                    "Error": "Faltan datos"
                }

            else:

                try:

                    conn_db = sqlite3.connect(DB)

                    cursor = conn_db.cursor()

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

                    conn_db.commit()
                    conn_db.close()

                    response = {
                        "status": 201,
                        "Mensaje": "Usuario registrado"
                    }

                except sqlite3.IntegrityError:

                    response = {
                        "status": 400,
                        "Error": "Usuario existente"
                    }

        elif action == "login":

            usuario = request.get("usuario")
            password = request.get("contraseña")

            conn_db = sqlite3.connect(DB)

            cursor = conn_db.cursor()

            cursor.execute(
                """
                SELECT password
                FROM usuarios
                WHERE usuario=?
                """,
                (usuario,)
            )

            resultado = cursor.fetchone()

            conn_db.close()

            if resultado and check_password_hash(
                    resultado[0],
                    password):

                response = {
                    "status": 200,
                    "Mensaje": "Login exitoso"
                }

            else:

                response = {
                    "status": 401,
                    "Error": "Credenciales inválidas"
                }

        elif action == "tareas":

            response = {
                "status": 200,
                "Mensaje": "Acceso correcto. Tarea procesada por Worker."
            }

        conn.sendall(
            json.dumps(response).encode()
        )

    except Exception as e:

        print("[WORKER ERROR]", e)

    finally:

        conn.close()


def start_workers():

    init_db()

    worker = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    worker.bind((HOST, PORT))

    worker.listen()

    print(f"[WORKERS] Escuchando en {HOST}:{PORT}")

    with ThreadPoolExecutor(max_workers=5) as executor:

        while True:

            conn, addr = worker.accept()

            executor.submit(
                procesar_tarea,
                conn,
                addr
            )


if __name__ == "__main__":
    start_workers()