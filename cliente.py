import socket
import json

HOST = "127.0.0.1"
PORT = 5000


def enviar_peticion(action, data=None):

    if data is None:
        data = {}

    payload = {
        "action": action,
        **data
    }

    with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM) as cliente:

        try:

            cliente.connect((HOST, PORT))

            cliente.sendall(
                json.dumps(payload).encode()
            )

            respuesta = cliente.recv(4096)

            return json.loads(
                respuesta.decode()
            )

        except ConnectionRefusedError:

            return {
                "status": 500,
                "Error": "Servidor no disponible"
            }


def registrar():

    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    print(
        enviar_peticion(
            "registro",
            {
                "usuario": usuario,
                "contraseña": password
            }
        )
    )


def login():

    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    respuesta = enviar_peticion(
        "login",
        {
            "usuario": usuario,
            "contraseña": password
        }
    )

    print(respuesta)

    if respuesta["status"] == 200:

        print(
            enviar_peticion("tareas")
        )


def menu():

    while True:

        print("\n=== SISTEMA DISTRIBUIDO ===")
        print("1. Registrarse")
        print("2. Login")
        print("3. Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            registrar()

        elif opcion == "2":
            login()

        elif opcion == "3":
            break


if __name__ == "__main__":
    menu()