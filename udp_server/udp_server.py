import socket
from datetime import datetime

# COLORES DE MENSAJES
VERDE = "\033[92m" # mensaje de conexion
CYAN = "\033[96m" # mensaje de desconexion
AZUL = "\033[94m" # mensaje de "mensaje"
ROJO = "\033[91m" # mensaje de error
RESET = "\033[0m" # evento no clasificado

# PUERTO
UDP_IP = "127.0.0.1"
UDP_PORT = 5000

def clasificarEvento(mensaje):
    msgUpper = mensaje.upper()
    if "ERROR" in msgUpper:
        return "ERROR", ROJO
    elif "DISCONNECT" in msgUpper:
        return "DISCONNECT", CYAN
    elif "CONNECT" in msgUpper:
        return "CONNECT", VERDE
    elif "MSG" in msgUpper:
        return "MSG", AZUL
    elif "API HTTP" in msgUpper:
        return "API HTTP", AZUL
    else:
        return "SIN_CLASIFICAR", RESET

def guardar(registro):
    with open("chat.log", "a", encoding="utf-8") as f:
        f.write(registro + "\n")

def mostrar(color, registro):
    print(f"{color}>>> {registro}{RESET}")

def iniciarServidor():
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # para recibir los mesnajes
    SOCKET.bind((UDP_IP, UDP_PORT)) # asignar el puerto
    print(f">>> Servidor de Logs (UDP) escuchando al puerto {UDP_PORT}...{RESET}")


    while True:
        # RECIBIMIENTO DE DATOS
        informacion, direccion = SOCKET.recvfrom(1024)
        mensaje = informacion.decode('utf-8') 
        hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        origen = f"{direccion[0]}:{direccion[1]}"
        
        EVENTO, COLOR = clasificarEvento(mensaje)
        REGISTRO = f"[{hora_actual}] {EVENTO}: [ORIGEN: {origen}] {mensaje}"
        mostrar(COLOR, REGISTRO)
        guardar(REGISTRO)

if __name__ == "__main__":
    iniciarServidor()
        
    

# python -c "import socket; s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.sendto(b'CONNECT usuario=karina', ('127.0.0.1', 5000))"



"""
def enviarLog(evento, descripcion):

    # eventos: CONNECT, DISCONNECT, MSG, ERROR, cualquier otro queda como no clasificado

    UDP_IP = "127.0.0.1"
    UDO_PORT = 5000

    mensaje = f"{evento} {descripcion}"

    try:
        SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        SOCKET.sendto(mensaje.encode('utf-8'), (UDP_IP, UDP_PORT))
    except Exception as exception:
        print(f"No se pudo enviar el log: {exception}")
"""