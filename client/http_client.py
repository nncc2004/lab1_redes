import requests
import json

def cliente_interactivo():
    print("--- Cliente de Consulta HTTP (Mos Eisley) ---")

    url_base = input("Ingrese la URL del servidor: ").strip()
    

    if url_base.endswith('/'):
        url_base = url_base[:-1]
    if not url_base.startswith('http'):
        url_base = 'http://' + url_base

    # Header para evitar el problema con ngrok
    headers = {"ngrok-skip-browser-warning": "1111"}

    print(f"\nConectado a: {url_base}")
    print("Comandos: history, users, exit")

    while True:
        comando = input("\n[Consulta] > ").strip().lower()

        if comando == 'exit':
            break
        
        url = f"{url_base}/{comando}"
        
        try:
            response = requests.get(url, headers=headers)
            
            print(f"Estado: {response.status_code}")
            
            try:
                data = response.json()
                print("Datos recibidos:")
                print(json.dumps(data, indent=4, ensure_ascii=False))
            except json.JSONDecodeError:
                print("Error: La respuesta no es JSON.")
                print(f"Contenido: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")

if __name__ == "__main__":
    cliente_interactivo()