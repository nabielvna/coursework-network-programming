import os
import base64
from glob import glob

class FileInterface:
    def __init__(self):
        # Use os.path.join for Windows compatibility
        self.files_dir = os.path.join(os.getcwd(), 'files')
        os.makedirs(self.files_dir, exist_ok=True)
        os.chdir(self.files_dir)

    def list(self, params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK', data=filelist)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, params=[]):
        try:
            if not params:
                return dict(status='ERROR', data='No filename provided')
            filename = params[0]
            # Sanitize filename for Windows
            filename = os.path.basename(filename)
            if not os.path.exists(filename):
                return dict(status='ERROR', data='File not found')
            with open(filename, 'rb') as fp:
                isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def upload(self, params=[]):
        try:
            if len(params) < 2:
                return dict(status='ERROR', data='Missing filename or data')
            filename = params[0]
            data_b64 = params[1]
            # Sanitize filename for Windows
            filename = os.path.basename(filename)
            file_data = base64.b64decode(data_b64)
            with open(filename, 'wb') as fp:
                fp.write(file_data)
            return dict(status='OK', data=f'File {filename} berhasil diupload')
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def delete(self, params=[]):
        try:
            if not params:
                return dict(status='ERROR', data='No filename provided')
            filename = params[0]
            # Sanitize filename for Windows
            filename = os.path.basename(filename)
            if os.path.exists(filename):
                os.remove(filename)
                return dict(status='OK', data=f'File {filename} berhasil dihapus')
            else:
                return dict(status='ERROR', data='File tidak ditemukan')
        except Exception as e:
            return dict(status='ERROR', data=str(e))

if __name__=='__main__':
    f = FileInterface()
    print(f.list())