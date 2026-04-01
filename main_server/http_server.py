'''
Notas:
Implementarse utilizando http.server de Python
Sólo de lectura del sistema

Consultas HTTP compatibles:
- Consulta de historial de mensajes
    GET /history Historial de los  ́ultimos N mensajes de la sala

- Consulta de usuarios conectados
    GET /users Lista de todos los usuarios conectados actualmente

- Error 404 para cualquier otra consulta
'''

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import json

class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, instancia_compartida=None, **kwargs):
        self.memoria = instancia_compartida
        self.n = 20
        super().__init__(*args, **kwargs)
    

    def do_GET(self):
        if self.path == '/history':
            with self.memoria.lock:
                datos = self.memoria.history[-1*self.n:]
            self.respuesta_json(datos, 200)
        
        elif self.path == '/users':
            with self.memoria.lock:
                datos = self.memoria.users
            self.respuesta_json(datos, 200)
        
        else:
            self.respuesta_json({"error": "Ruta no encontrada. Recuerda sólo usar /history y /users"}, 404)

    def respuesta_json(self, contenido, codigo):
        respuetsa = json.dumps(contenido).encode('utf-8')
        
        self.send_response(codigo)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(respuetsa)))
        self.end_headers()
        
        self.wfile.write(respuetsa)
    


def poblar_memoria_test(instancia_compartida):
    with instancia_compartida.lock:
        instancia_compartida.users = ["User_A", "User_B", "User_C"]
        
        mensajes_prueba = []
        for i in range(1, 51):
            mensajes_prueba.append({
                "user": f"User_{i % 3}", 
                "msg": f"Mensaje número {i}"
            })
        
        instancia_compartida.history = mensajes_prueba
    
    print("HTTP_server_test: Memoria cargada con 50 mensajes de prueba y 3 usuarios de prueba.")


def http_init(instancia_compartida):
    HTTP_IP = "0.0.0.0"
    HTTP_PORT = 50000
    print(f"HTTP_server: Iniciando el http_server en el puerto {HTTP_PORT} e ip {HTTP_IP}")
    
    poblar_memoria_test(instancia_compartida)
    
    handler_factory = lambda *args, **kwargs: RequestHandler(*args, instancia_compartida=instancia_compartida, **kwargs)

    server = HTTPServer((HTTP_IP, HTTP_PORT), handler_factory)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nHTTP_server: Cerrando servidor http_server")
        server.server_close()