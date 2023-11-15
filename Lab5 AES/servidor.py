import socket
import random
from Crypto.Cipher import AES
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
    
    # Mensaje a cifrar
    with open(archivo_entrada, 'r') as file:
        mensaje_original = file.read()
    print("Las claves son las mismas")

    


    # Generar una clave aleatoria para AES
    key_aes = get_random_bytes(16)
    client.send(key_aes)
    # Crear un objeto AES para cifrar
    cipher = AES.new(key_aes, AES.MODE_EAX)
    
    # Cifrar el mensaje
    ciphertext, tag = cipher.encrypt_and_digest(mensaje_original.encode())

    # Enviar el mensaje cifrado y el tag al cliente
    client.send(cipher.nonce + tag + ciphertext)
    print("El texto cifrado es : ",ciphertext)
else:
    print("Las claves no coinciden.")
    
           
client.close()
server.close()
