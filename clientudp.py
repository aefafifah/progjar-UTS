import socket
import sys

# Membuat pemetaan antara warna dalam bahasa Indonesia dan bahasa Inggris
color_mapping = {
    'merah': 'red',
    'kuning': 'yellow',
    'biru': 'blue',
    'orange': 'orange',
    'ungu': 'purple',
    'pink': 'pink',
    'coklat': 'brown',
    'hitam': 'black',
    'putih': 'white',
    'abu-abu': 'grey'
}

# Client
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.1'
port = 1233

# Pesan Kosong
ClientSocket.sendto(b'', (host, port))

running = True
while running:
    # Menerima warna dari server
    Response, addr = ClientSocket.recvfrom(1024)
    color = Response.decode('utf-8')
    print("Received color from server:", color)
    
    # Tebak-tebakan sisi klien dimulai
    answer = input("Apa warna ini? (Jawab dalam bahasa Indonesia): ")
    
    # Mengirim jawaban pengguna ke server
    ClientSocket.sendto(str.encode(answer), (host, port))
    
    # Menerima feedback dari server
    feedback, _ = ClientSocket.recvfrom(1024)
    print(feedback.decode('utf-8'))
    

ClientSocket.close()
sys.exit(0)  
