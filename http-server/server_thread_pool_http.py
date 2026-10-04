from socket import *
import socket
import time
import sys
import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from http import HttpServer

httpserver = HttpServer()

def ProcessTheClient(connection, address):
    try:
        headers = b""
        while True:
            data = connection.recv(1)
            if not data:
                break
            headers += data
            if headers.endswith(b"\r\n\r\n"):
                break

        header_str = headers.decode('utf-8')
        lines = header_str.split('\r\n')
        content_length = 0
        for line in lines:
            if line.startswith("Content-Length:"):
                try:
                    content_length = int(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    content_length = 0
                break

        body = b""
        if content_length > 0:
            body = connection.recv(content_length)

        full_request_bytes = headers + body
        full_request_str = full_request_bytes.decode('utf-8')
        
        hasil = httpserver.proses(full_request_str)
        
        connection.sendall(hasil)
    
    except Exception as e:
        logging.warning(f"Error processing client: {e}")
    finally:
        connection.close()
        return

def Server():
    the_clients = []
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    my_socket.bind(('0.0.0.0', 8885))
    my_socket.listen(1)

    with ThreadPoolExecutor(20) as executor:
        while True:
            connection, client_address = my_socket.accept()
            p = executor.submit(ProcessTheClient, connection, client_address)
            the_clients.append(p)
            jumlah = ['x' for i in the_clients if i.running()==True]

def main():
    Server()

if __name__ == "__main__":
    main()