import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 50002))
client.send("NICK c4m1lo".encode('utf-8'))
respuesta = client.recv(1024)
print(f"Servidor dice: {respuesta.decode('utf-8')}")
client.close()