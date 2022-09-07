import socket
from threading import Thread

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 41775

client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(50)
print('[*] Listening as {}:{}'.format(SERVER_HOST, SERVER_PORT))

def listen_for_client(cs):
    while True:
        try:
            msg = cs.recv(32768).decode()
        except:
            try:
                client_sockets.remove(cs)
                break
            except:
                break
        for client_socket in client_sockets.copy():
            try:
                client_socket.send(msg.encode())
            except:
                try:
                    client_sockets.remove(cs)
                    break
                except:
                    break

while True:
    client_socket, client_address = s.accept()
    print('[+] {} connected.'.format(client_address))
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()

for cs in client_sockets:
    cs.close()
s.close()
