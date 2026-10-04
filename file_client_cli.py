import socket
import json
import base64
import os
import logging

# Konfigurasi server: sesuaikan alamat dan port jika perlu
default_server = ('0.0.0.0', 6666)
SERVER_ADDRESS = default_server


def send_command(command_str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(SERVER_ADDRESS)
        full_command = f"{command_str}\r\n\r\n"
        sock.sendall(full_command.encode())
        buffer = ''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            buffer += chunk.decode()
            if "\r\n\r\n" in buffer:
                break
    try:
        payload = buffer.split("\r\n\r\n")[0]
        return json.loads(payload)
    except json.JSONDecodeError:
        logging.error("Gagal decoding JSON dari server: %s", buffer)
        return {'status': 'ERROR', 'data': 'Invalid JSON response'}


def remote_list():
    resp = send_command("LIST")
    if resp.get('status') == 'OK':
        print("Daftar file di server:")
        for fname in resp.get('data', []):
            print(f"- {fname}")
    else:
        print("Gagal daftar file:", resp.get('data'))


def remote_get():
    filename = input("Nama file yang akan di-download: ")
    resp = send_command(f"GET {filename}")
    if resp.get('status') == 'OK':
        try:
            data_b64 = resp['data_file']
            file_bytes = base64.b64decode(data_b64)
            with open(resp['data_namafile'], 'wb') as fp:
                fp.write(file_bytes)
            print(f"File '{filename}' berhasil di-download.")
        except Exception as e:
            print("Gagal menulis file:", e)
    else:
        print("Gagal download:", resp.get('data'))


def remote_upload():
    filepath = input("Path file untuk di-upload: ")
    if not os.path.isfile(filepath):
        print("File tidak ditemukan.")
        return
    nama_file = os.path.basename(filepath)
    try:
        with open(filepath, 'rb') as fp:
            b64 = base64.b64encode(fp.read()).decode()
    except Exception as e:
        print("Gagal membaca file:", e)
        return
    resp = send_command(f"UPLOAD {nama_file} {b64}")
    if resp.get('status') == 'OK':
        print(resp.get('data'))
    else:
        print("Gagal upload:", resp.get('data'))


def remote_delete():
    filename = input("Nama file yang akan dihapus: ")
    resp = send_command(f"DELETE {filename}")
    if resp.get('status') == 'OK':
        print(resp.get('data'))
    else:
        print("Gagal hapus:", resp.get('data'))


def main():
    logging.basicConfig(level=logging.WARNING)
    while True:
        print("\n=== MENU FILE SERVER ===")
        print("1. List files")
        print("2. Download file")
        print("3. Upload file")
        print("4. Delete file")
        print("5. Exit")
        choice = input("Pilih menu (1-5): ")

        if choice == '1':
            remote_list()
        elif choice == '2':
            remote_get()
        elif choice == '3':
            remote_upload()
        elif choice == '4':
            remote_delete()
        elif choice == '5':
            print("Keluar dari client.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")


if __name__ == '__main__':
    main()
