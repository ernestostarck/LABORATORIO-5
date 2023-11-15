import socket
import random
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import base64
# Parámetros compartidos
p = 997  # Número primo
g = 400   # Generador

# Clave privada del servidor
a = random.randint(1, 399) # valor inferior al generador

# Calcular clave pública del servidor
A = (g ** a) % p

# Ruta del archivo de entrada 
archivo_entrada = 'mensajeentrada.txt'



# Configurar el servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 12345))
server.listen(1)
print("Esperando una conexión...")

# Aceptar la conexión
client, addr = server.accept()
print("Conexión establecida desde", addr)

# Enviar la clave pública del servidor al cliente
client.send(str(A).encode())

# Recibir la clave pública del cliente
B = int(client.recv(1024).decode())

# Calcular la clave compartida
shared_key = (B ** a) % p
print("Clave compartida:", shared_key)


# Recibir la clave pública del cliente
Z = int(client.recv(1024).decode())

#=====================================================================
#=====================================================================

if Z == shared_key:
    
    print("Las claves son las mismas")
    clave = b'password'
    # Genera un IV aleatorio
    iv = get_random_bytes(8)

    # Cifra el mensaje
    with open(archivo_entrada, 'rb') as f:
        mensaje = f.read()
    mensaje = mensaje + b' ' * (8 - len(mensaje) % 8)
    cipher = DES.new(clave, DES.MODE_CBC, iv)
    mensaje_encriptado = cipher.encrypt(mensaje)

    # Codifica el mensaje en Base64
    mensaje_encriptado_base64 = base64.b64encode(mensaje_encriptado)

    print("el mensaje encriptado es : ",mensaje_encriptado_base64)
    
    # Envía el IV al cliente
    client.send(iv)

    # Espera una confirmación del cliente
    client.recv(1024)

    # Envía el mensaje cifrado en Base64 al cliente
    client.send(mensaje_encriptado_base64)
    
    #=============================================================================

       
client.close()
server.close()
