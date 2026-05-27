import socket
import threading

class SensorListener:
    def __init__(self, host="0.0.0.0", port=5000, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.running = False
        self.callback = None

    def start(self):
        self.running = True
        threading.Thread(target=self._listen, daemon=True).start()

    def stop(self):
        self.running = False

    def _listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
            server.bind((self.host, self.port))
            print(f"UDP Listener started on {self.host}:{self.port}")

            while self.running:
                data, address = server.recvfrom(self.buffer_size)
                message = data.decode()
                print(f"Received data: {message} from {address}")

                if self.callback:
                    self.callback(message)

if __name__ == "__main__":
    def handle_data(data):
        print(f"Processing data: {data}")

    listener = SensorListener(port=5000)
    listener.callback = handle_data
    listener.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        listener.stop()
