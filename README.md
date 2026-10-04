# HTTP Server with Two Concurrency Models

A simple HTTP server written in Python without any web framework. It handles `GET`, `POST`, and `DELETE`, and comes in two versions that handle many clients at once in different ways: a **thread pool** and a **process pool**. An interactive command-line client is included for testing.

## How it is organised

1. **Core HTTP module (`http.py`):** the `HttpServer` class parses requests, processes them, and builds responses. It does not depend on the concurrency model.
2. **Two concurrent servers:** each one opens a TCP listener and hands every client to `HttpServer`.
   - `server_process_pool_http.py` uses a `ProcessPoolExecutor` (20 processes), port `8889`. Processes can use several CPU cores and avoid Python's Global Interpreter Lock.
   - `server_thread_pool_http.py` uses a `ThreadPoolExecutor` (20 threads), port `8885`. Threads suit I/O-bound work and use less memory.
3. **Client (`client/client.py`):** a terminal application that builds raw HTTP requests.

## What the server supports

| Method | Behaviour |
|---|---|
| `GET` | Returns a file, or an HTML listing when the path is a directory |
| `POST` | Uploads a file into `server_data/` |
| `DELETE` | Deletes a file from `server_data/` |

All files are stored in and served from `server_data/`, which is created automatically. `response()` in `http.py` builds the full HTTP response with status code, headers, and body.

## Run it

1. Start one of the servers from this folder:

   ```bash
   python server_process_pool_http.py    # port 8889
   # or
   python server_thread_pool_http.py     # port 8885
   ```

2. In another terminal, start the client:

   ```bash
   python client/client.py
   ```

   The client connects to `localhost:8889` by default. To use the thread-pool server, change the port in `client/client.py` to `8885`.

3. Pick an action from the menu:

   ```text
   1. List files on the server
   2. Upload a file to the server
   3. Delete a file on the server
   4. Exit
   ```

## Load testing

`server_data/perftest.sh` has example commands for [Apache Benchmark](https://httpd.apache.org/docs/current/programs/ab.html), for example:

```bash
ab -n 100 -c 50 http://localhost:8887/testing.txt
```

Change the port to match the server you started (`8885` or `8889`).

## Known quirks

- The client opens its socket to port `8889`, but the `Host` header in its hand-built requests says `localhost:8885`. The connection still works.
- `client/client.py` has helper code for TLS and `certs/` holds a certificate and the command to generate a key (`certs/generate.txt`), but the servers do not use TLS. They speak plain HTTP.
