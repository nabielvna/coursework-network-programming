"""Create the 10, 50, and 100 MB test files used by stress_test.py.

The files are not stored in the repository because they are large and fully
reproducible. Run this once before running the stress test.
"""
import os

SIZES = {
    'test_10MB.bin': 10 * 1024 * 1024,
    'test_50MB.bin': 50 * 1024 * 1024,
    'test_100MB.bin': 100 * 1024 * 1024,
}

# The client uploads from the current folder; the server serves ./files.
for folder in ('.', 'files'):
    os.makedirs(folder, exist_ok=True)
    for name, size in SIZES.items():
        path = os.path.join(folder, name)
        if os.path.exists(path) and os.path.getsize(path) == size:
            continue
        with open(path, 'wb') as fp:
            fp.write(os.urandom(size))
        print(f'created {path} ({size // (1024 * 1024)} MB)')
