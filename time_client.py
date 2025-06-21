import socket
def main():
    server_address = ('localhost', 45000)
    # Buat socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Jangan pakai sock.bind() di sisi client!
    sock.connect(server_address)
    try:
        # Kirim request TIME
        sock.sendall(b"TIME\r\n")
        data = sock.recv(1024)
        print(f"Received: {data.decode()}")
        # Kirim request QUIT
        sock.sendall(b"QUIT\r\n")
    finally:
        sock.close()
if __name__ == "__main__":
    main()
