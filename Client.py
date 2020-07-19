import socket
import select

HEADER_LENGTH = 10

IP = "localhost"
PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

client_socket.setblocking(False)


while True:
    message = input('YOU > ')

    message = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message)

    try:
        while True:
            address_header = client_socket.recv(HEADER_LENGTH)
            address_length = int(address_header.decode('utf-8').strip())

            address = client_socket.recv(address_length).decode('utf-8')
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(address + ' > ' + message)
            
    
    except IOError as e:
        continue
