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
    message_header = client_socket.recv(HEADER_LENGTH)

    message_length = int(message_header.decode('utf-8').strip())
    data = client_socket.recv(message_length)
    return {'header': message_header, 'data': data}


while True:
    read_sockets, _, _ = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print('Accepted new user: ' + user['data'].decode('utf-8'))

        else:
            message = receive_message(notified_socket)
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])


