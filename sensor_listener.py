import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((UDP_IP, UDP_PORT))

print("FocusHub UDP listener running...")

while True:
    data, addr = server.recvfrom(1024)
    print(f"Received: {data.decode()} from {addr}")
