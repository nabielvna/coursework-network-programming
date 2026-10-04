import sys
import socket
import json
import logging
import ssl
import os

server_address = ('localhost', 8889)

def make_socket(destination_address='localhost', port=12000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        # logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        return sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")
        return None


def make_secure_socket(destination_address='localhost', port=10000):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        # logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        secure_socket = context.wrap_socket(sock, server_hostname=destination_address)
        # logging.warning(secure_socket.getpeercert())
        return secure_socket
    except Exception as ee:
        logging.warning(f"error {str(ee)}")
        return None



def send_command(command_str, is_secure=False):
    alamat_server = server_address[0]
    port_server = server_address[1]

    if is_secure == True:
        sock = make_secure_socket(alamat_server, port_server)
    else:
        sock = make_socket(alamat_server, port_server)
    
    if not sock:
        logging.error("Could not connect to the server.")
        return False

    try:
        # logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received = "" 
        while True:
            data = sock.recv(2048)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = data_received
        # logging.warning("data received from server:")
        return hasil
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False
    finally:
        sock.close()


if __name__ == '__main__':
    while True:
        print("\nPilih tindakan:")
        print("1. List file di server")
        print("2. Upload file ke server")
        print("3. Delete file di server")
        print("4. Exit")
        
        choice = input("Masukkan pilihan (1-4): ")
        
        if choice == '1':
            # --- PENGUJIAN: GET (Melihat Daftar File) ---
            print("\n--- Meminta daftar file dari server ---")
            cmd_get = """GET / HTTP/1.0\r\nHost: localhost:8885\r\n\r\n"""
            hasil = send_command(cmd_get, is_secure=False)
            if hasil:
                print(hasil)

        elif choice == '2':
            # --- PENGUJIAN: POST (Mengunggah File dari Komputer) ---
            local_filepath = input("Masukkan path file lokal yang ingin diunggah: ")

            if not os.path.exists(local_filepath):
                print(f"Error: File '{local_filepath}' tidak ditemukan di komputer Anda.")
                continue

            with open(local_filepath, 'r') as f:
                content = f.read()

            server_filename = os.path.basename(local_filepath)
            
            print(f"\n--- Mengunggah file '{local_filepath}' sebagai '{server_filename}' ke server ---")
            
            content_length = len(content)
            
            cmd_post = (
                f"POST /{server_filename} HTTP/1.0\r\n"
                f"Host: localhost:8885\r\n"
                f"Content-Length: {content_length}\r\n"
                f"\r\n"
                f"{content}"
            )
            hasil = send_command(cmd_post, is_secure=False)
            if hasil:
                print(hasil)

        elif choice == '3':
            # --- PENGUJIAN: DELETE (Menghapus File) ---
            filename = input("Masukkan nama file di server yang akan dihapus: ")
            print(f"\n--- Menghapus file '{filename}' dari server ---")
            
            cmd_delete = f"""DELETE /{filename} HTTP/1.0\r\nHost: localhost:8885\r\n\r\n"""
            hasil = send_command(cmd_delete, is_secure=False)
            if hasil:
                print(hasil)

        elif choice == '4':
            print("Terima kasih, program keluar.")
            break
        
        else:
            print("Pilihan tidak valid, silakan coba lagi.")