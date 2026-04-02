from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import json
from utils import enviarLog
from datetime import datetime

class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, instancia_compartida=None, **kwargs):
        self.memoria = instancia_compartida
        self.n = 20
        super().__init__(*args, **kwargs)
    

    def do_GET(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.path == '/history':
            with self.memoria.lock:
                datos = self.memoria.history[-1*self.n:]
            self.respuesta_json(datos, 200)
            enviarLog("API HTTP", f"{timestamp}: Se ha solicitado el historial de mensajes por HTTP.")
        
        elif self.path == '/users':
            with self.memoria.lock:
                datos = self.memoria.users
            self.respuesta_json(datos, 200)
            enviarLog("API HTTP", f"{timestamp}: Se ha solicitado el listado de usuarios conectados por HTTP.")
        else:
            self.respuesta_json({"error 404": "Ruta no encontrada. Recuerda sólo usar /history y /users"}, 404)
            enviarLog("ERROR", f"{timestamp}: Se ha solicitado con un comando incorrecto por HTTP. Se ha respondido con 404.")

    def respuesta_json(self, contenido, codigo):
        respuetsa = json.dumps(contenido).encode('utf-8')
        
        self.send_response(codigo)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(respuetsa)))
        self.end_headers()
        
        self.wfile.write(respuetsa)

    def responder_400(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        enviarLog("ERROR", f"{timestamp}: Se ha solicitado erróneamente una petición HTTP. Se ha respondido con 400.")
        self.respuesta_json({"error 400":"Sólo se puede usar solicitudes tipo GET"}, 400)
    
    def do_POST(self): self.responder_400()
    def do_PUT(self): self.responder_400()
    def do_DELETE(self): self.responder_400()
    def do_HEAD(self): self.responder_400()
    def do_PATCH(self): self.responder_400()


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
    
    #poblar_memoria_test(instancia_compartida)
    
    handler_factory = lambda *args, **kwargs: RequestHandler(*args, instancia_compartida=instancia_compartida, **kwargs)

    server = HTTPServer((HTTP_IP, HTTP_PORT), handler_factory)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nHTTP_server: Cerrando servidor http_server")
        server.server_close()