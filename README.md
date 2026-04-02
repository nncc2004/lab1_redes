Karina Aliaga, 202373556-6
Camilo Valdebenito 202373538-8
Nicolás Chehde 202373508-6

MAINSERVER:
    Para ejecutar el mainserver, es decir, aquel que es server tcp, http y cliente udp, se debe ejecutar el código 'mainserver/main.py' desde una consola. 
    Eso iniciará un hilo para cada servidor para que se ejecute desde la misma consola. Ahí mismo se expondrán las IP y puertos de cada uno. 
    No debe hacer nada más desde esta terminal. 

UDP_SERVER:
    Para ejecutar el udp_server debe ejecutar el código 'udp_server/udp_server.py' desde una consola. Se mostrará un mensaje de inicio del mismo.


CLIENTE TCP:
    Para iniciar el cliente tcp, debe ejecutar el código 'client/tcp_client.py', y le pedirá primero la IP para conectarse. Aquí debe conectar la URL dada por el ngrok para el server tcp, en formato '0.tcp.sa.ngrok.io'. Luego pedirá el puerto, también dado por ngrok.

CLIENTE HTTP:
    Para iniciar el cliente de la API HTTP, debe ejecutar el código 'client/http_server.py'. Esto le solicitará la conexión con el host, que corresponde al segundo link dado por el NGROK, y luego el puerto. En caso de haberse conectado por localhost, el puerto es el 50000, si es por ngrok es el 80.


PROTOCOLO DE COMANDOS PARA SISTEMA CLIENTE TCP:
- NICK [nickname]: Inicia la sesión bajo el nombre puesto en el espacio 'nickname'.
- MSG [mensaje]: Envía un mensaje al servidor para que se distribuya. 
- DISCONNECT: Desconecta al usuario del server, y de la memoria compartida. 

PROTOCOLO DE COMANDOS PARA CLIENTE API HTTP:
- /users: Devuelve la lista de usuarios activamente conectados al servidor
- /history: Devuelve el histrial de los últimos 20 mensajes enviados en el servidor. 
- /exit: Cierra la conexión. 

PROTOCOLO PARA INICIAR EL NGROK:
    ngrok start --config ./ngrok.yml --all