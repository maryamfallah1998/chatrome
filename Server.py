import socket
import select

HEADER_LENGTH = 10

IP = "localhost"
PORT = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}

print('Server is Listening ...')


def receive_message(client_socket):

    data = client_socket.recv(1024)
    return data.decode("utf-8")


while True:
    read_sockets, _, _ = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = client_address

            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print('Accepted new connection from '+ str(client_address))

        else:
            message = receive_message(notified_socket)
            user = clients[notified_socket]

            print(f'Received message from {user}: {message}')

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(message.encode('utf-8'))

    