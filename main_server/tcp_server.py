import socket
import threading
from utils import enviarLog

clientes_conectados = {}

def broadcast(mensaje, remitente, instancia_compartida):
    with instancia_compartida.lock:
        for usuario, socket_destino in clientes_conectados.items():
            if usuario != remitente:
                try:
                    socket_destino.send(f"[{remitente}]: {mensaje}".encode('utf-8'))
                except:
                    pass

def comandoRecibido(comando, username, instancia_compartida):
    if comando.startswith("MSG "):
        mensaje = comando[4:]
        with instancia_compartida.lock:
            instancia_compartida.history.append({
                "user": f"{username}",
                "msg": f"{mensaje}"
            })
        enviarLog("MSG", f"{username}: {mensaje}")
        broadcast(mensaje, username, instancia_compartida)

        return True
    elif comando == "DISCONNECT":
        return False
    else:
        enviarLog("ERROR", f"{username}: Comando Desconocido")
        return False


def hilo_usuario(socket_cliente, instancia_compartida):
    username = None
    try:
        mensaje = socket_cliente.recv(1024)
        if not mensaje:
            return
        
        mensaje = mensaje.decode('utf-8').strip()
        if mensaje.startswith("NICK "):
            username = mensaje[5:].strip()
            with instancia_compartida.lock:
                if username in instancia_compartida.users:
                    socket_cliente.send(f"Ya existe un usuario conectado con ese nick\n".encode('utf-8'))
                    return
                instancia_compartida.users.append(username)
                clientes_conectados[username] = socket_cliente
            socket_cliente.send(f"Usuario Registrado con Nick {username}".encode('utf-8'))
            enviarLog("CONNECT",f'usuario = {username}' )
        else:
            socket_cliente.send("Para registrarte debes enviar NICK <tu_nombre>\n".encode('utf-8'))
            return

        while True:
            entrada = socket_cliente.recv(1024)
            if not entrada:
                break
            comando = entrada.decode('utf-8').strip()
            estado = comandoRecibido(comando, username, instancia_compartida)
            if not estado:
                if comando == "DISCONNECT":
                    socket_cliente.send("Se finalizo la conexion".encode('utf-8'))
                    break
                else:
                    socket_cliente.send("Comando no reconocido".encode('utf-8'))
    except Exception as e:
        print(f"TCP_server: Error inesperado: {e}")
        return

    finally:
        if username:
            with instancia_compartida.lock:
                if username in instancia_compartida.users:
                    instancia_compartida.users.remove(username)
                if username in clientes_conectados:
                    del clientes_conectados[username]

        enviarLog("DISCONNECT", f"{username} se ha desconectado")
        socket_cliente.close()

def tcp_init(instancia_compartida):
    TCP_IP = "0.0.0.0"
    TCP_PORT = 50004
    print(f"TCP_server: Iniciando el tcp en el puerto {TCP_PORT} e ip {TCP_IP}")
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((TCP_IP, TCP_PORT))
    socket_server.listen()
    while True:
        socket_cliente, direccion = socket_server.accept()
        thread = threading.Thread(target=hilo_usuario, args=(socket_cliente, instancia_compartida), daemon=True)
        thread.start()
    


