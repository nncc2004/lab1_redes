import socket
import json

def http_client_request(host, puerto, endpoint):
    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.settimeout(10)
    try:
        print(f"Conectando a {host} en puerto {puerto}...")
        http_socket.connect((host, puerto))
        
        request = (
            f"GET {endpoint} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
            f"ngrok-skip-browser-warning: 11111\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )
        http_socket.sendall(request.encode('utf-8'))
        
        respuesta = b""
        while True:
            datos = http_socket.recv(4096)
            if not datos:
                break
            respuesta += datos
            
        if not respuesta:
            print("El servidor cerró la conexión sin enviar datos.")
        else:
            print(f"\nHTTP_client: Respuesta de {endpoint}:")
            respuesta = respuesta.decode('utf-8').split('\r\n\r\n', 1)
            header = respuesta[0]
            cuerpo = respuesta[1]

            try:
                json_format = json.loads(cuerpo)
                json_format =json.dumps(json_format, indent=4, ensure_ascii=False)
                print(json_format)

            except:
                print(cuerpo)
            print("-"*50)


    except Exception as e:
        print(f"Error en la consulta: {e}")
    finally:
        http_socket.close()


if __name__ == "__main__":
    host = input("Host (localhost o ngrok): ").strip()
    host = host.replace("https://", "").replace("http://", "").split('/')[0]
    puerto = int(input("Puerto: "))


    while True:
        opcion = input("\nComando (history/users/exit): ").strip().lower()
        if opcion == 'exit': break
        http_client_request(host, puerto, f"/{opcion}")


'''
NOTAR QUE SÓLO FUNCIONA SI AL INICIAR NGROK SE HACE COMO
ngrok http 50000 --scheme http

Y ACÁ SE COLOCA EL PUERTO 80
'''