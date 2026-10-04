# Network Programming Coursework

Coursework for a Network Programming class (Institut Teknologi Sepuluh Nopember, 2025). Every project is plain Python socket programming with the standard library only.

| Folder | What it is | How to run |
|---|---|---|
| [`time-server/`](time-server) | Multithreaded TCP time server with a two-command text protocol | `python3 server.py` |
| [`file-server/`](file-server) | File server and CLI client over a custom text protocol (`LIST`, `GET`, `UPLOAD`, `DELETE`, Base64, JSON replies) | `python file_server.py`, then `python file_client_cli.py` |
| [`file-server-stress-test/`](file-server-stress-test) | The file server with thread-pool and process-pool versions, plus an automated stress test and results | `python make_test_files.py`, then `python stress_test.py` |
| [`http-server/`](http-server) | HTTP server (`GET`, `POST`, `DELETE`) in thread-pool and process-pool versions, with a CLI client | `python server_thread_pool_http.py`, then `python client/client.py` |

## How the projects build on each other

1. **Time server:** sockets and threads.
2. **File server:** designing an application-layer protocol and splitting the code into network, protocol, and file layers.
3. **Stress test:** comparing a thread pool with a process pool under load.
4. **HTTP server:** implementing a standard protocol and comparing the same two concurrency models again.

## Getting a single project

Every project is also published as its own branch (`time-server`, `file-server`, `file-server-stress-test`, `http-server`) that contains only that project, and tagged `<project>-v1.0.0`:

```bash
git clone -b http-server --single-branch https://github.com/nabielvna/coursework-network-programming.git
```

Alternatively, fetch one folder from `main` with sparse checkout:

```bash
git clone --filter=blob:none --sparse https://github.com/nabielvna/coursework-network-programming.git
cd coursework-network-programming
git sparse-checkout set http-server
```

## License

[MIT](LICENSE)
