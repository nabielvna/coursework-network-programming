import sys
import os
import os.path
import uuid
from glob import glob
from datetime import datetime

class HttpServer:
    def __init__(self):
        self.sessions = {}
        self.types = {}
        self.types['.pdf'] = 'application/pdf'
        self.types['.jpg'] = 'image/jpeg'
        self.types['.txt'] = 'text/plain'
        self.types['.html'] = 'text/html'
        
        # Mendefinisikan direktori data server
        self.server_directory = 'server_data'
        # Membuat direktori jika belum ada
        if not os.path.exists(self.server_directory):
            os.makedirs(self.server_directory)

    def response(self, kode=404, message='Not Found', messagebody=bytes(), headers={}):
        tanggal = datetime.now().strftime('%c')
        resp = []
        resp.append(f"HTTP/1.0 {kode} {message}\r\n")
        resp.append(f"Date: {tanggal}\r\n")
        resp.append("Connection: close\r\n")
        resp.append("Server: myserver/1.0\r\n")
        resp.append(f"Content-Length: {len(messagebody)}\r\n")
        for kk in headers:
            resp.append(f"{kk}:{headers[kk]}\r\n")
        resp.append("\r\n")

        response_headers = ''
        for i in resp:
            response_headers = f"{response_headers}{i}"

        if not isinstance(messagebody, bytes):
            messagebody = messagebody.encode()

        response = response_headers.encode() + messagebody
        return response

    def proses(self, data):
        requests = data.split("\r\n")
        baris = requests[0]
        
        all_headers = [n for n in requests[1:] if n != '']
        
        body_start_index = data.find("\r\n\r\n") + 4
        request_body = data[body_start_index:]

        j = baris.split(" ")
        try:
            method = j[0].upper().strip()
            object_address = j[1].strip()

            if method == 'GET':
                return self.http_get(object_address, all_headers)
            if method == 'POST':
                return self.http_post(object_address, all_headers, request_body)
            if method == 'DELETE':
                return self.http_delete(object_address, all_headers)
            else:
                return self.response(400, 'Bad Request', '', {})
        except IndexError:
            return self.response(400, 'Bad Request', '', {})

    def get_full_path(self, object_address):
        relative_path = object_address.lstrip('/')
        return os.path.join(self.server_directory, relative_path)

    def http_get(self, object_address, headers):
        full_path = self.get_full_path(object_address)
        
        if os.path.isdir(full_path):
            try:
                list_items = "<html><head><title>Directory Listing</title></head><body>"
                list_items += f"<h1>Directory listing for {object_address}</h1><ul>"
                for item in sorted(os.listdir(full_path)):
                    url_path = os.path.join(object_address, item).replace("\\", "/")
                    list_items += f'<li><a href="{url_path}">{item}</a></li>'
                list_items += "</ul></body></html>"
                return self.response(200, 'OK', list_items, {'Content-Type': 'text/html'})
            except OSError:
                return self.response(500, "Internal Server Error", "Could not read directory", {})

        if os.path.isfile(full_path):
            try:
                with open(full_path, 'rb') as fp:
                    isi = fp.read()
                fext = os.path.splitext(full_path)[1]
                content_type = self.types.get(fext, 'application/octet-stream')
                headers_resp = {'Content-type': content_type}
                return self.response(200, 'OK', isi, headers_resp)
            except FileNotFoundError:
                 return self.response(404, 'Not Found', f'File {object_address} not found', {})
        
        return self.response(404, 'Not Found', f'Resource {object_address} not found', {})

    def http_post(self, object_address, headers, body):
        full_path = self.get_full_path(object_address)
        
        try:
            with open(full_path, 'wb') as f:
                f.write(body.encode('utf-8'))
            return self.response(201, 'Created', f"File {object_address} uploaded successfully.", {})
        except Exception as e:
            return self.response(500, 'Internal Server Error', f"Could not upload file: {e}", {})

    def http_delete(self, object_address, headers):
        full_path = self.get_full_path(object_address)
        
        if os.path.exists(full_path) and os.path.isfile(full_path):
            try:
                os.remove(full_path)
                return self.response(200, 'OK', f"File {object_address} deleted successfully.", {})
            except Exception as e:
                return self.response(500, 'Internal Server Error', f"Error deleting file: {e}", {})
        else:
            return self.response(404, 'Not Found', 'File not found.', {})

if __name__ == "__main__":
    httpserver = HttpServer()