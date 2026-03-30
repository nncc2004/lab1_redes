import socket
from datetime import datetime

#COLORES DE MENSAJES
VERDE = "\033[92m" # mensaje de conexion
CYAN = "\033[96m" # mensaje de desconexion
AZUL = "\033[94m" # mensaje de "mensaje"
ROJO = "\033[91m" # mensaje de error
RESET = "\033[0m" # evento no clasificado

UDP_IP = "127.0.0.1"
UDP_PORT = 5000

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # para recibir los mesnajes
SOCKET.bind((UDP_IP, UDP_PORT)) # asignar el puerto

print(f">>> Servidor de Logs (UDP) escuchando al puerto {UDP_PORT}...{RESET}")

while True:

    # RECIBIMIENTO DE DATOS
    informacion, direccion = SOCKET.recvfrom(1024)
    mensaje = informacion.decode('utf-8') 
    hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 

    # CLASIFICACION DE EVENTOS
    if "ERROR" in mensaje.upper():
        EVENTO = "ERROR"
        COLOR = ROJO
        ARCHIVO = "errores.log"
    
    elif "DISCONNECT" in mensaje.upper():
        EVENTO = "DISCONNECT"
        COLOR = CYAN
        ARCHIVO = "chat.log"

    elif "CONNECT" in mensaje.upper():
        EVENTO = "CONNECT"
        COLOR = VERDE
        ARCHIVO = "chat.log"
        
    elif "MSG" in mensaje.upper():
        EVENTO = "MSG"
        COLOR = AZUL
        ARCHIVO = "chat.log"
        
    else:
        EVENTO = "SIN_CLASIFICAR"
        COLOR = RESET
        ARCHIVO = "chat.log"
        
    REGISTRO = f"[{hora_actual}] {EVENTO}: [ORIGEN: {direccion[0]}:{direccion[1]}] {mensaje}"
    print(f"{COLOR}>>> [{hora_actual}] {EVENTO}: [ORIGEN: {direccion[0]}:{direccion[1]}] {mensaje}{RESET}")

    with open(ARCHIVO, "a", encoding="utf-8") as f:
        f.write(REGISTRO + "\n")
    

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