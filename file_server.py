from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading
import logging

from file_protocol import FileProtocol

fp = FileProtocol()

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address

    def run(self):
        buffer = ""
        while True:
            chunk = self.connection.recv(4096)
            if not chunk:
                break
            buffer += chunk.decode()
            if "\r\n\r\n" in buffer:
                request_str = buffer.split("\r\n\r\n")[0]
                logging.warning(f"string diproses: {request_str}")
                hasil = fp.proses_string(request_str)
                self.connection.sendall((hasil + "\r\n\r\n").encode())
                buffer = ""
        self.connection.close()

class Server(threading.Thread):
    def __init__(self, ipaddress='0.0.0.0', port=6666):
        super().__init__()
        self.ipinfo = (ipaddress, port)
        self.my_socket = socket(AF_INET, SOCK_STREAM)
        self.my_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.the_clients = []

    def run(self):
        logging.warning(f"server berjalan di ip address {self.ipinfo}")
        self.my_socket.bind(self.ipinfo)
        self.my_socket.listen(5)
        while True:
            conn, addr = self.my_socket.accept()
            logging.warning(f"connection from {addr}")
            client = ProcessTheClient(conn, addr)
            client.start()
            self.the_clients.append(client)

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    svr = Server()
    svr.start()
