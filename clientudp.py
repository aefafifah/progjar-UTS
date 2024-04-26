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

# Mengirim pesan kosong ke server untuk memulai komunikasi
ClientSocket.sendto(b'', (host, port))

running = True
while running:
    # Menerima warna dari server
    Response, addr = ClientSocket.recvfrom(1024)
    color = Response.decode('utf-8')
    print("Received color from server:", color)
    
    # Meminta jawaban dari pengguna dalam bahasa Indonesia
    answer = input("Apa warna ini? (Jawab dalam bahasa Indonesia): ")
    
    # Mengirim jawaban pengguna ke server
    ClientSocket.sendto(str.encode(answer), (host, port))
    
    # Menerima feedback dari server
    feedback, _ = ClientSocket.recvfrom(1024)
    print(feedback.decode('utf-8'))
    
# Menutup koneksi socket saat loop selesai
ClientSocket.close()
sys.exit(0)  # Mengakhiri program dengan kode keluar 0
