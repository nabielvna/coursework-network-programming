import argparse
import logging
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from concurrent.futures import ThreadPoolExecutor
from file_protocol import FileProtocol

HOST = '0.0.0.0'
PORT = 6666

def main():
    parser = argparse.ArgumentParser(description='File server with thread pool')
    parser.add_argument('-w', '--workers', type=int, default=5,
                        help='Jumlah worker pool')
    args = parser.parse_args()
    max_workers = args.workers

    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(message)s')
    srv = socket(AF_INET, SOCK_STREAM)
    srv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen()
    logging.warning(f"Server (MT-Pool) listening on {(HOST, PORT)} with {max_workers} workers")

    fp = FileProtocol()

    def handle_client(conn, addr):
        logging.warning(f"MT worker handling {addr}")
        buffer = ""
        try:
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()
                if "\r\n\r\n" in buffer:
                    req = buffer.split("\r\n\r\n")[0]
                    parts = req.split(maxsplit=2)
                    cmd = parts[0].upper()
                    if cmd == "UPLOAD" and len(parts) >= 2:
                        filename = parts[1]
                        logging.warning(f"processing: UPLOAD {filename} (payload omitted)")
                    else:
                        logging.warning(f"processing: {cmd}")
                    resp = fp.proses_string(req)
                    conn.sendall((resp + "\r\n\r\n").encode())
                    buffer = ""
        finally:
            conn.close()

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        while True:
            conn, addr = srv.accept()
            pool.submit(handle_client, conn, addr)

if __name__ == '__main__':
    main()