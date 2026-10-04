import json
import logging
import shlex

from file_interface import FileInterface

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def proses_string(self, string_datamasuk=''):
        cmd = string_datamasuk.split(maxsplit=1)[0].upper()
        logging.warning(f"string diproses: {cmd}")
        # Pisahkan token tanpa merubah case untuk Base64
        tokens = shlex.split(string_datamasuk)
        try:
            c_request = tokens[0].lower()  
            logging.warning(f"memproses request: {c_request}")
            params = tokens[1:]
            result = getattr(self.file, c_request)(params)
            return json.dumps(result)
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return json.dumps(dict(status='ERROR', data='request tidak dikenali'))

if __name__=='__main__':
    fp = FileProtocol()
    print(fp.proses_string("LIST"))