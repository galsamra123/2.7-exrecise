"""
Author - Gal Heichal Samra

Program name - client to server connection EX2.7

Description - The program connects this client socket to the server
              (on another computer) and sends commands.
              The client gets answers accordingly.

date   - 23.11.25
"""

import socket
import logging
import os

MAX_PACKET = 1024
IP = '192.168.1.218'
PORT = 3037
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def length_str(msg):
    """
    Return the length of a string padded with zeros to 6 digits.

    :param msg: String to measure.
    :return: Zero-padded length string of 6 characters.
    """
    return str(len(msg)).zfill(6)


def protocol_send(sock, confirmation, data):
    """
    Send a command and its data to the server through the given socket.

    :param sock: The client socket used to send the message.
    :param confirmation: The command name (e.g., 'dir', 'delete', etc.).
    :param data: The payload/data of the command (bytes).
    :return: None
    """
    msg = confirmation.encode() + b',' + data
    final_length = length_str(msg.decode()).encode()
    sock.sendall(final_length + b',' + msg)


def protocol_recive(sock):
    """
    Receive a server response and return the confirmation and data parts.

    :param sock: The client socket used to receive data.
    :return: Tuple (confirmation: str, data: bytes)
    """
    recive = 0
    recived = b""

    # Read first 7 bytes: 6 digits length + comma
    while recive < 7:
        byts = sock.recv(7 - recive)
        recive += len(byts)
        recived += byts

    length_msg = recived.decode()
    logging.info(length_msg)
    length_msg = length_msg[:-1]  # remove comma
    logging.info(length_msg)
    length_msg = int(length_msg)

    recive = 0
    recived = b""

    while recive < length_msg:
        byts = sock.recv(length_msg - recive)
        recive += len(byts)
        recived += byts

    comma = recived.find(b',')
    confirmation = recived[:comma]
    data = recived[comma + 1:]
    confirmation = confirmation.decode()

    return confirmation, data


try:
    my_socket.connect((IP, PORT))

    while True:
        request = input(
            'Enter your request (dir / delete / copy / execute / send screenshot / exit): \n'
        ).strip().lower()

        if request == 'dir':
            path = input('Enter a directory path: \n')
            protocol_send(my_socket, request, path.encode())
            response = protocol_recive(my_socket)
            print(response)

        elif request == 'send screenshot':
            path = input('Enter a file path to save the screenshot (on THIS computer): \n')
            protocol_send(my_socket, request, b'')
            response, bytse = protocol_recive(my_socket)

            if os.path.isdir(path):
                save_path = os.path.join(path, "screen.jpg")
                with open(save_path, 'wb') as f:
                    f.write(bytse)

        elif request == 'delete':
            path = input('Enter a file path to delete: \n')
            protocol_send(my_socket, request, path.encode())
            response = protocol_recive(my_socket)
            print(response)

        elif request == 'copy':
            from_path = input('Enter the file path to copy: \n')
            to_path = input('Enter the directory path to copy to: \n')
            all_paths = f'{from_path},{to_path}'
            protocol_send(my_socket, request, all_paths.encode())
            response = protocol_recive(my_socket)
            print(response)

        elif request == 'execute':
            path = input('Enter an app path to open: \n')
            protocol_send(my_socket, request, path.encode())
            response = protocol_recive(my_socket)
            print(response)

        elif request == 'exit':
            protocol_send(my_socket, request, b'')
            response = protocol_recive(my_socket)
            print(response)
            break

        else:
            protocol_send(my_socket, request, b'')
            response = protocol_recive(my_socket)
            print(response)

except socket.error as err:
    logging.critical('Received socket error: ' + str(err))

finally:
    my_socket.close()
    logging.info('Client socket closed.')
