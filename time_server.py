import socket
import threading
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address

    def run(self):
        logging.info(f"Client connected from {self.address}")
        try:
            while True:
                data = self.connection.recv(32)
                if not data:
                    break

                message = data.decode('utf-8').strip()
                logging.info(f"Received {repr(message)} from {self.address}")

                if message.upper() == "TIME":
                    now = datetime.now()
                    waktu = now.strftime("%H:%M:%S")
                    response = f"JAM {waktu}\r\n"
                    self.connection.sendall(response.encode('utf-8'))
                elif message.upper() == "QUIT":
                    logging.info(f"Client {self.address} requested QUIT, closing connection.")
                    break
                else:
                    self.connection.sendall(b"ERROR\r\n")
        except Exception as e:
            logging.error(f"Error handling client {self.address}: {e}")
        finally:
            self.connection.close()
            logging.info(f"Connection to {self.address} closed.")

class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5)
        logging.info("Server listening on port 45000")

        while True:
            connection, client_address = self.my_socket.accept()
            logging.info(f"Connection from {client_address}")
            clt = ProcessTheClient(connection, client_address)
            clt.start()
            self.the_clients.append(clt)

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()
