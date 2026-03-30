import threading
from tcp_server import tcp_init
from http_server import http_init


#Gente, esta es la clase para el tema del trheading. Igual que en SO. Lo dejé con el candado igual. 
class ClaseCompartida:
    def __init__(self):
        self.users = []       
        self.history = []     
        self.lock = threading.Lock() #El candado 


def main():
    instancia_compartida = ClaseCompartida()

    #Hilos:
    thread_tcp = threading.Thread(target=tcp_init, args=(instancia_compartida,), daemon=True)
    thread_http = threading.Thread(target=http_init, args=(instancia_compartida,), daemon=True)

    print("main.py: Se han creado los hilos. Iniciando servidores.")

    thread_tcp.start()
    thread_http.start()

    try:
        thread_tcp.join()
        thread_http.join()
    except KeyboardInterrupt:
        print("\nmain.py: Se han cerrado los servidores.")


if __name__ == '__main__':
    print("main.py: Iniciando programa...")
    main()