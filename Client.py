import socket
import select
import errno


IP = "localhost"
PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))



while True:
    message = input('YOU > ')

    if message:
        message = message.encode('utf-8')
        client_socket.send(message)

    
        while True:

            message = client_socket.recv(1024).decode('utf-8')
            print(' > ' + message)
           

    