import socket, json, base64, os, logging

SERVER_ADDR = ('127.0.0.1', 6666)
SOCKET_TIMEOUT = 30

def send_cmd(cmd: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(SOCKET_TIMEOUT)
        try:
            sock.connect(SERVER_ADDR)
            sock.sendall((cmd + "\r\n\r\n").encode())
            buf = ''
            while True:
                try:
                    chunk = sock.recv(4096)
                except socket.timeout:
                    head = cmd.split(maxsplit=2)[:2]
                    logging.error("Timeout saat kirim: %s …[payload omitted]", " ".join(head))
                    return {'status': 'ERROR', 'data': 'Timeout while receiving response'}
                if not chunk:
                    break
                buf += chunk.decode()
                if "\r\n\r\n" in buf:
                    break
        except socket.timeout:
            head = cmd.split(maxsplit=2)[:2]
            logging.error("Timeout saat kirim: %s …[payload omitted]", " ".join(head))
            return {'status': 'ERROR', 'data': 'Timeout during connect/send'}
        except Exception as e:
            logging.error("Error socket: %s", e)
            return {'status': 'ERROR', 'data': str(e)}

    try:
        return json.loads(buf.split("\r\n\r\n")[0])
    except Exception:
        logging.error("Invalid JSON: %s", buf)
        return {'status': 'ERROR', 'data': 'Invalid JSON'}

def list_files():
    return send_cmd("LIST")

def download_file(filename: str, dest_folder: str = "."):
    resp = send_cmd(f"GET {filename}")
    if resp.get('status') == 'OK':
        data = base64.b64decode(resp['data_file'])
        path = os.path.join(dest_folder, resp['data_namafile'])
        with open(path, 'wb') as f:
            f.write(data)
        return True, len(data)
    return False, 0

def upload_file(filepath: str):
    if not os.path.isfile(filepath):
        return False, "not found"
    name = os.path.basename(filepath)
    b64 = base64.b64encode(open(filepath, 'rb').read()).decode()
    resp = send_cmd(f"UPLOAD {name} {b64}")
    return resp.get('status') == 'OK', resp.get('data')
