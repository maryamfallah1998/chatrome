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
            user = client_address

            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print('Accepted new connection from '+ str(client_address))

        else:
            message = receive_message(notified_socket)
            user = clients[notified_socket]

            message_print = message["data"].decode('utf-8')
            print(f'Received message from {user}: {message_print}')

            user_tosend = str(user).encode('utf-8')
            user_header = f"{len(user_tosend):<{HEADER_LENGTH}}".encode('utf-8')

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user_header + user_tosend + message['header'] + message['data'])


    
