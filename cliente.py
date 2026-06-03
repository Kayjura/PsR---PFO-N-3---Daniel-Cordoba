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

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as cliente:

            cliente.connect(
                (HOST, PORT)
            )

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
            "error": "Servidor no disponible"
        }

    except Exception as e:

        return {
            "status": 500,
            "error": str(e)
        }


def registrar():

    print("\n=== REGISTRO ===")

    usuario = input(
        "Usuario: "
    ).strip()

    password = input(
        "Contraseña: "
    ).strip()

    respuesta = enviar_peticion(
        "registro",
        {
            "usuario": usuario,
            "contraseña": password
        }
    )

    print("\nRespuesta:")

    print(
        json.dumps(
            respuesta,
            indent=4,
            ensure_ascii=False
        )
    )


def login():

    print("\n=== LOGIN ===")

    usuario = input(
        "Usuario: "
    ).strip()

    password = input(
        "Contraseña: "
    ).strip()

    respuesta = enviar_peticion(
        "login",
        {
            "usuario": usuario,
            "contraseña": password
        }
    )

    print("\nRespuesta:")

    print(
        json.dumps(
            respuesta,
            indent=4,
            ensure_ascii=False
        )
    )

    if respuesta.get("status") == 200:

        print(
            "\nLogin exitoso."
        )

        menu_tareas()

    else:

        print(
            "\nNo fue posible iniciar sesión."
        )


def consultar_estadisticas():

    respuesta = enviar_peticion(
        "tareas"
    )

    print(
        "\n=== INFORMACIÓN DEL SISTEMA ==="
    )

    print(
        json.dumps(
            respuesta,
            indent=4,
            ensure_ascii=False
        )
    )


def menu_tareas():

    while True:

        print(
            "\n=== MENÚ DE TAREAS ==="
        )

        print(
            "1. Consultar estadísticas"
        )

        print(
            "2. Volver"
        )

        opcion = input(
            "Seleccione una opción: "
        )

        if opcion == "1":

            consultar_estadisticas()

        elif opcion == "2":

            break

        else:

            print(
                "\nOpción inválida."
            )


def mostrar_menu():

    while True:

        print(
            "\n=============================="
        )

        print(
            " SISTEMA DISTRIBUIDO PFO 3 "
        )

        print(
            "=============================="
        )

        print(
            "1. Registrarse"
        )

        print(
            "2. Login"
        )

        print(
            "3. Salir"
        )

        opcion = input(
            "Seleccione una opción: "
        )

        if opcion == "1":

            registrar()

        elif opcion == "2":

            login()

        elif opcion == "3":

            print(
                "\nHasta luego."
            )

            break

        else:

            print(
                "\nOpción inválida."
            )


if __name__ == "__main__":

    mostrar_menu()