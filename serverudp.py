import socket
import json
import random
import threading
import time
import sys

# Function to set client response timer
def client_response_timer(addr):
    time.sleep(5)  # Client has 5 seconds to respond
    if not response_received.is_set():
        print("Response time exceeded. No response received.")
        feedback = 0
        feedback_lock.acquire()
        try:
            feedbacks[addr] = feedback
        finally:
            feedback_lock.release()
        ServerSocket.sendto(b'Waktu habis!', addr)  # Send "Waktu habis" message to client

# Function to stop color sender thread and close server socket
def stop_server():
    global running
    running = False  # Set running flag to False to stop the while loop in the main server code
    color_sender_thread.join()  # Wait for color sender thread to finish
    ServerSocket.close()  # Close the server socket
    sys.exit(0)  # Exit the program with exit code 0

# Membuat pemetaan antara warna dalam bahasa Inggris dan bahasa Indonesia
color_mapping = {
    'red': 'merah',
    'yellow': 'kuning',
    'blue': 'biru',
    'orange': 'orange',
    'purple': 'ungu',
    'pink': 'pink',
    'brown': 'coklat',
    'black': 'hitam',
    'white': 'putih',
    'grey': 'abu-abu'
}

# Function to send color to all clients
def send_color_to_clients(color):
    for client_addr in clients:
        ClientSocket.sendto(str.encode(color), client_addr)

# Server
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.1'
port = 1233

colors = list(color_mapping.keys())

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')

feedbacks = {}  # Dictionary to store feedback from clients
feedback_lock = threading.Lock()  # Lock to access feedbacks dictionary
response_received = threading.Event()  # Event to mark if response from client is received

clients = set()  # Set to store addresses of connected clients

# Define ClientSocket
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Start a thread to continuously send colors to all clients
def color_sender(running):  # Receive running flag as argument
    while running:
        random_color = random.choice(colors)
        send_color_to_clients(random_color)
        time.sleep(10)  # Send color every 10 seconds

color_sender_thread = threading.Thread(target=color_sender, args=(True,))  # Pass True to indicate running
color_sender_thread.start()

running = True  # Define running flag here
while running:
    data, addr = ServerSocket.recvfrom(1024)
    print('Connected to: ' + addr[0] + ':' + str(addr[1]))
    clients.add(addr)  # Add client address to the set of connected clients
    
    # Start timer for client response time
    timer_thread = threading.Thread(target=client_response_timer, args=(addr,))
    timer_thread.start()
    
    # Send a random color to the client
    random_color = random.choice(colors)
    ServerSocket.sendto(str.encode(random_color), addr)
    
    # Receive response from the client
    response_received.clear()  # Mark that response is not received yet
    Response, _ = ServerSocket.recvfrom(1024)
    response_received.set()  # Mark that response is received
    
    # Check client's answer
    client_answer = Response.decode('utf-8').lower().strip()  # Convert to lowercase and remove whitespace
    correct_answer = color_mapping[random_color]  # Get Indonesian translation of the correct color
    feedback = 100 if client_answer == correct_answer else 0
    
    # Provide feedback to the client
    feedback_lock.acquire()
    try:
        feedbacks[addr] = feedback
    finally:
        feedback_lock.release()
    
    # Correct the answer and give feedback
    if feedback == 100:
        print("Client at {} answered correctly with '{}'.".format(addr, client_answer))
        ServerSocket.sendto(b'Jawaban Anda benar! nilai anda 100', addr)
    else:
        print("Client at {} answered incorrectly with '{}' (correct answer: '{}').".format(addr, client_answer, correct_answer))
        ServerSocket.sendto(b'Jawaban Anda salah! nilai anda 0', addr)


stop_server()
