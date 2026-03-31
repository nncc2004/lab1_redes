import socket
import threading

def hilo_usuario(socket_cliente, direccion, instancia_compartida):
    username = None
    try:
        mensaje = socket_cliente.recv(1024)
        if not mensaje:
            socket_cliente.close()
            return
        mensaje = mensaje.decode('utf-8').strip()
        if mensaje.startswith("NICK "):
            username = mensaje[5:].strip()
            with instancia_compartida.lock:
                instancia_compartida.users.append(username)
            socket_cliente.send(f"TCP_server: Usuario Registrado con Nick {username}".encode('utf-8'))
            
        else:
            socket_cliente.send("TCP_server:  Para registrarte debes enviar NICK <tu_nombre>\n".encode('utf-8'))
            socket_cliente.close()
            return

        while True:
            mensaje = socket_cliente.recv(1024)
            if not mensaje:
                socket_cliente.close()
                return

    except Exception as e:
        print(f"TCP_server: Error inesperado: {e}")
        return

    finally:
        if username:
            with instancia_compartida.lock:
                if username in instancia_compartida.users:
                    instancia_compartida.users.remove(username)
        socket_cliente.close()

def tcp_init(instancia_compartida):
    TCP_IP = "127.0.0.1"
    TCP_PORT = 50002
    print(f"TCP_server: Iniciando el tcp en el puerto {TCP_PORT} e ip {TCP_IP}")
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((TCP_IP, TCP_PORT))
    socket_server.listen()
    while True:
        socket_cliente, direccion = socket_server.accept()
        thread = threading.Thread(target=hilo_usuario, args=(socket_cliente, direccion, instancia_compartida), daemon=True)
        thread.start()
    


