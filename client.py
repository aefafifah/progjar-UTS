import socket

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.1'
port = 1233

print('Waiting for connection')

while True:
    Input = input('Say Something: ')
    ClientSocket.sendto(str.encode(Input), (host, port))
    Response, addr = ClientSocket.recvfrom(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()
