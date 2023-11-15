import socket
from Crypto.Cipher import DES
import base64
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

# Enviar la clave pública a l servidor
client.send(str(shared_key).encode())

print("Clave compartida:", shared_key)

#=====================================================================
#=====================================================================

# Recibe el IV
iv = client.recv(8)

# Envía una confirmación al servidor
client.send(b'OK')

# Recibe el mensaje cifrado en Base64
mensaje_encriptado_base64 = client.recv(1024)

# Decodifica el mensaje en Base64
mensaje_encriptado = base64.b64decode(mensaje_encriptado_base64)

# Descifra el mensaje
clave = b'password'
cipher = DES.new(clave, DES.MODE_CBC, iv)
mensaje_desencriptado = cipher.decrypt(mensaje_encriptado)

# Elimina el padding
mensaje_desencriptado = mensaje_desencriptado.rstrip(b' ')

# Imprime el mensaje desencriptado
print("Mensaje encriptado:", mensaje_encriptado_base64)
print("Mensaje desencriptado:", mensaje_desencriptado.decode('utf-8', errors='replace'))

with open(archivo_salida, 'wb') as f:
    f.write(mensaje_desencriptado)
    
print("Mensaje guardado")


# Cerrar la conexión
client.close()

