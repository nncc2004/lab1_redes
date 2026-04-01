import socket
import threading

def escuchar_servidor(socket_cliente):
    while True:
        try:
            mensaje = socket_cliente.recv(1024)
            if not mensaje:
                print("Se perdio la conexion con el servidor")
                break
            print(f"{mensaje.decode('utf-8').strip()}\n")
            if mensaje.decode('utf-8').strip().startswith("Se finalizo "):
                break
        except Exception as e:
            print(f"Error de conexion: {e}")
            break

def iniciar_cliente():
    IP = "0.tcp.sa.ngrok.io"
    PUERTO = 17435
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((IP, PUERTO))
    except ConnectionRefusedError as e:
        print(f"No se pudo conectar al servidor: {e}")
        return
    print("Ingrese el comando NICK para conectarse a la sala de chat")
    comando = input()
    cliente.send(comando.strip().encode('utf-8'))
    respuesta = cliente.recv(1024).decode('utf-8').strip()
    if not respuesta.startswith("Usuario Registrado con "):
        print(respuesta)
        cliente.close()
        return
    
    hilo_escucha = threading.Thread(target=escuchar_servidor, args=(cliente,), daemon=True)
    hilo_escucha.start()
    print(">>> Conectado correctamente a la sala de chat, escribe el comando y apreta enter")
    while True:
        try:
            entrada = input()
            cliente.send(entrada.encode('utf-8'))
        except KeyboardInterrupt as e:
            cliente.send("DISCONNECT".encode('utf-8'))
            break
    print("\nDesconectando..")
    cliente.close

if __name__ == "__main__":
    iniciar_cliente()