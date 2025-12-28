import socket
import threading

clients = []

def handle_client(c):
    while True:
        try:
            data = c.recv(1024)
            if not data:
                break
            for client in clients:
                if client != c:
                    client.send(data)
        except:
            break
    if c in clients:
        clients.remove(c)
    c.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 7002))
server.listen(5)
print("Server is running...")

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()