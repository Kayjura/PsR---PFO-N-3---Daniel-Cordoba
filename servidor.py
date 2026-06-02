import socket
import json
import threading

HOST_CENTRAL = "127.0.0.1"
PORT_CENTRAL = 5000

HOST_WORKER = "127.0.0.1"
PORT_WORKER = 5001


def derivar_a_worker(data_bytes):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as worker:
            worker.connect((HOST_WORKER, PORT_WORKER))
            worker.sendall(data_bytes)

            respuesta = worker.recv(4096)

            return respuesta

    except ConnectionRefusedError:

        error = {
            "status": 500,
            "Error": "Workers no disponibles"
        }

        return json.dumps(error).encode()


def manejar_cliente(conn, addr):

    print(f"[SERVIDOR] Cliente conectado: {addr}")

    try:

        data = conn.recv(4096)

        if data:

            respuesta = derivar_a_worker(data)

            conn.sendall(respuesta)

    except Exception as e:

        print("[ERROR]", e)

    finally:

        conn.close()


def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST_CENTRAL, PORT_CENTRAL))

    server.listen()

    print(f"[SERVIDOR] Escuchando en {HOST_CENTRAL}:{PORT_CENTRAL}")

    while True:

        conn, addr = server.accept()

        threading.Thread(
            target=manejar_cliente,
            args=(conn, addr)
        ).start()


if __name__ == "__main__":
    start_server()