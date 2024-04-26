import socket

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.1'
port = 1233

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')

while True:
    data, addr = ServerSocket.recvfrom(1024)
    print('Connected to: ' + addr[0] + ':' + str(addr[1]))
    reply = 'Server Says: ' + data.decode('utf-8')
    ServerSocket.sendto(str.encode(reply), addr)
ServerSocket.close()
