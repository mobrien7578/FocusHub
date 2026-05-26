import socket

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 5000

PI_IP = "192.168.0.38"
PI_PORT = 5000

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listen_sock.bind((LISTEN_IP, LISTEN_PORT))

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("UDP bridge running...")
print(f"Listening on {LISTEN_IP}:{LISTEN_PORT}")
print(f"Forwarding to Raspberry Pi at {PI_IP}:{PI_PORT}")

while True:
    data, addr = listen_sock.recvfrom(1024)
    print(f"Received from Packet Tracer: {data.decode()} from {addr}")
    send_sock.sendto(data, (PI_IP, PI_PORT))
    print("Forwarded to Raspberry Pi")
