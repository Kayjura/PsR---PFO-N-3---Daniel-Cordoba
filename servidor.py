import socket
import json
import threading

HOST_CENTRAL = "127.0.0.1"
PORT_CENTRAL = 5000

WORKERS = [
    ("127.0.0.1", 5001),
    ("127.0.0.1", 5002),
    ("127.0.0.1", 5003)
]

worker_actual = 0

lock = threading.Lock()


def obtener_worker():

    global worker_actual

    with lock:

        worker = WORKERS[worker_actual]

        worker_actual = (
            worker_actual + 1
        ) % len(WORKERS)

    return worker


def derivar_a_worker(data_bytes):

    host, puerto = obtener_worker()

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as worker:

            worker.connect(
                (host, puerto)
            )

            worker.sendall(data_bytes)

            respuesta = worker.recv(4096)

            return respuesta

    except Exception as e:

        error = {
            "status": 500,
            "error": (
                f"No fue posible "
                f"contactar al worker "
                f"{puerto}: {str(e)}"
            )
        }

        return json.dumps(error).encode()


def manejar_cliente(conn, addr):

    print(
        f"[SERVIDOR] Cliente conectado: "
        f"{addr}"
    )

    try:

        data = conn.recv(4096)

        if not data:

            conn.close()
            return

        respuesta = derivar_a_worker(data)

        conn.sendall(respuesta)

    except Exception as e:

        error = {
            "status": 500,
            "error": str(e)
        }

        conn.sendall(
            json.dumps(error).encode()
        )

    finally:

        conn.close()

        print(
            f"[SERVIDOR] Cliente "
            f"{addr} desconectado"
        )


def start_server():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        (HOST_CENTRAL, PORT_CENTRAL)
    )

    server.listen()

    print(
        f"[SERVIDOR] Escuchando "
        f"en {HOST_CENTRAL}:{PORT_CENTRAL}"
    )

    print(
        "[SERVIDOR] Round Robin activo"
    )

    print(
        f"[SERVIDOR] Workers: "
        f"{WORKERS}"
    )

    while True:

        conn, addr = server.accept()

        threading.Thread(
            target=manejar_cliente,
            args=(conn, addr),
            daemon=True
        ).start()


if __name__ == "__main__":
    start_server()