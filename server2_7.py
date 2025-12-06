"""
Author - Gal Heichal Samra

Program name - Server to client connection EX2.7

Description - The server accepts commands from a client and performs:
              dir, delete, copy, execute, screenshot

date   - 28/10/25
"""

import socket
import logging
from funcs2_7 import di_r, delete, copy, execute, send_screenshot, length_str

QUEUE_LEN = 1
IP = '0.0.0.0'
PORT = 3037
SUCCESS = 'success'
EXITED = 'client exited'
FAILURE = 'failed in the way'
NOT_COMMAND = 'not a command'


def protocol_send(sock, confirmation, data):
    """
    Send a response message back to the client.

    :param sock: Client socket to send data to.
    :param confirmation: Command result (success/fail).
    :param data: Payload data to send (bytes).
    :return: None
    """
    msg = confirmation.encode() + b',' + data
    final_length = length_str(msg).encode()
    final_msg = final_length + b',' + msg
    sock.sendall(final_msg)


def protocol_recive(sock):
    """
    Receive a message from the client and return (confirmation, data).

    :param sock: Client socket to read from.
    :return: Tuple of (confirmation: str, data: bytes)
    """
    recive = 0
    recived = b""
    while recive < 7:
        byts = sock.recv(7 - recive)
        if byts == b'':
            raise ConnectionError
        recive += len(byts)
        recived += byts

    length_msg = recived.decode()
    length_msg = length_msg[:-1]
    length_msg = int(length_msg)

    recive = 0
    recived = b""
    while recive < length_msg:
        byts = sock.recv(length_msg - recive)
        if byts == b'':
            raise ConnectionError
        recive += len(byts)
        recived += byts

    comma = recived.find(b',')
    confirmation = recived[:comma]
    data = recived[comma + 1:]
    confirmation = confirmation.decode()

    return confirmation, data


def main():
    """
    Main server loop: accepts clients and handles their commands.
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((IP, PORT))
    my_socket.listen(QUEUE_LEN)

    while True:
        client_socket, client_address = my_socket.accept()
        try:
            logging.info('A connection was made with client socket')

            while True:
                try:
                    client_request, data = protocol_recive(client_socket)
                    request = client_request.strip().lower()

                    if request == 'dir':
                        path = data.decode()
                        confirmation, data = di_r(path)
                        data = data.encode()
                        protocol_send(client_socket, confirmation, data)

                    elif request == 'send screenshot':
                        confirmation, data = send_screenshot()
                        protocol_send(client_socket, confirmation, data)

                    elif request == 'delete':
                        path = data.decode()
                        confirmation, data = delete(path)
                        data = data.encode()
                        protocol_send(client_socket, confirmation, data)

                    elif request == 'copy':
                        path1, path2 = data.decode().split(',')
                        confirmation, data = copy(path1, path2)
                        data = data.encode()
                        protocol_send(client_socket, confirmation, data)

                    elif request == 'execute':
                        path = data.decode()
                        confirmation, data = execute(path)
                        data = data.encode()
                        protocol_send(client_socket, confirmation, data)

                    elif request == 'exit':
                        protocol_send(client_socket, SUCCESS, EXITED.encode())
                        break

                    else:
                        protocol_send(client_socket, FAILURE, NOT_COMMAND.encode())

                except socket.error as err:
                    logging.critical('Socket error on client socket: ' + str(err))
                    break

        except socket.error as err:
            logging.critical('Socket error on server socket: ' + str(err))

        finally:
            client_socket.close()
            logging.info('Client socket closed')


if __name__ == "__main__":
    logging.basicConfig(filename='fserver.log', level=logging.INFO,
                        format='%(asctime)s %(name)s - %(levelname)s - %(message)s')
    logging.info('Server up and running')
    main()
