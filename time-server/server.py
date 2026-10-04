import socket
import threading
import datetime
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', stream=sys.stdout)

class ClientHandler(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        try:
            while True:
                data = self.connection.recv(1024).decode('utf-8').strip()
                
                if not data:
                    logging.info(f"Koneksi dengan {self.address} ditutup oleh klien.")
                    break

                logging.info(f"Menerima request '{data}' dari {self.address}")

                if data == "TIME":
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    response = f"JAM {current_time}\r\n"
                    
                    self.connection.sendall(response.encode('utf-8'))
                    logging.info(f"Mengirim waktu '{current_time}' ke {self.address}")
                
                elif data == "QUIT":
                    logging.info(f"Klien {self.address} meminta untuk keluar.")
                    break
                
                else:
                    response = "ERROR: Perintah tidak dikenal.\r\n"
                    self.connection.sendall(response.encode('utf-8'))

        except Exception as e:
            logging.error(f"Terjadi error pada koneksi dengan {self.address}: {e}")
            
        finally:
            self.connection.close()
            logging.info(f"Koneksi dengan {self.address} telah ditutup.")

class TimeServer(threading.Thread):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind((self.host, self.port))
        self.my_socket.listen(5)
        logging.info(f"Time server berjalan dan mendengarkan di port {self.port}...")

        while True:
            connection, client_address = self.my_socket.accept()
            logging.info(f"Menerima koneksi baru dari {client_address}")
            
            client_thread = ClientHandler(connection, client_address)
            client_thread.start()
            self.the_clients.append(client_thread)
	
def main():
    server = TimeServer('0.0.0.0', 45000)
    server.start()

if __name__ == "__main__":
    main()