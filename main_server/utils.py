'''
Funciones de utilidad
'''
import socket

def enviarLog(evento, descripcion):
    '''
    Falta probarla bien 
    '''
    # eventos: CONNECT, DISCONNECT, MSG, ERROR, cualquier otro queda como no clasificado
    # falta consulta HTTP

    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000

    mensaje = f"{evento} {descripcion}"

    try:
        SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        SOCKET.sendto(mensaje.encode('utf-8'), (UDP_IP, UDP_PORT))
    except Exception as exception:
        print(f"No se pudo enviar el log: {exception}")



if __name__ == '__main__':
    print("Ejecutando desde utils.py")
    #Kari! Aquí prueba tu función
