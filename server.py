import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('localhost', 9999))
sock.listen(5)

while True:
    client, addr = sock.accept()
    print("getting data...")
    data = client.recv(1024)
    udata = data.decode('utf-8')
    with open('data.log', 'a') as f:
        f.write(udata)
    client.close()
