import socket
import random
from Crypto.Cipher import AES
# Parámetros compartidos
p = 997   # Número primo
g = 400  # Generador

# Ruta del archivo de entrada 
archivo_salida = 'mensajerecibido.txt'

# Configurar el cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))


A = int(client.recv(1024).decode())


print("Clave pública  (P):", p)

print("Clave pública (G)):", g)

# Solicitar al usuario que ingrese su clave privada
b = int(input("Ingresa tu clave privada: "))

# Calcular clave pública del cliente
B = (g ** b) % p

# Enviar la clave pública al servidor
client.send(str(B).encode())

# Calcular la clave compartida
shared_key = (A ** b) % p

# Enviar la clave pública al servidor
client.send(str(shared_key).encode())

print("Clave compartida:", shared_key)

#=====================================================================
#=====================================================================


key_aes = client.recv(1024)

# Recibir el mensaje cifrado y el tag del cliente
data = client.recv(1024)
nonce = data[:16]
tag = data[16:32]
ciphertext = data[32:]

# Crear un objeto AES para descifrar
cipher = AES.new(key_aes, AES.MODE_EAX, nonce=nonce)

# Descifrar el mensaje
mensaje_descifrado = cipher.decrypt_and_verify(ciphertext, tag)

# Imprimir el mensaje descifrado
print("Mensaje descifrado:", mensaje_descifrado.decode())

with open(archivo_salida, 'wb') as f:
    f.write(mensaje_descifrado)
print("Mensaje guardado correctamente")
# Cerrar la conexión
client.close()
