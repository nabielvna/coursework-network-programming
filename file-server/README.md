# File Server

A TCP file server and command-line client built on a text protocol designed from scratch. One thread serves each client. Files are sent as Base64 and every reply is JSON.

## Files

| File | Role |
|---|---|
| `file_server.py` | TCP server (one thread per client), listens on port `6666` |
| `file_protocol.py` | Parses a request string and dispatches it |
| `file_interface.py` | The actual file operations (list, get, upload, delete) |
| `file_client_cli.py` | Interactive command-line client |
| `files/` | The folder the server serves |

## Run it

```bash
python file_server.py
```

In another terminal:

```bash
python file_client_cli.py
```

The client connects to `0.0.0.0:6666` by default. Change `SERVER_ADDRESS` in `file_client_cli.py` to use another address.

## Protocol

A request is one string, `REQUEST PARAMETER1 PARAMETER2 ...`, ended by `\r\n\r\n`. Every response is JSON followed by `\r\n\r\n`. An unknown request returns `status: ERROR` with `data: request tidak dikenali`.

| Request | Parameters | Success response | Failure response |
|---|---|---|---|
| `LIST` | none | `status: OK`, `data`: list of file names | `status: ERROR`, `data`: message |
| `GET` | file name | `status: OK`, `data_namafile`, `data_file` (content in Base64) | `status: ERROR`, `data`: message |
| `UPLOAD` | file name, content in Base64 | `status: OK`, `data`: confirmation | `status: ERROR`, `data`: message |
| `DELETE` | file name | `status: OK`, `data`: confirmation | `status: ERROR`, `data`: message |

For `UPLOAD`, the client reads the local file, encodes its content as a Base64 string, and sends `UPLOAD <name> <base64>`. For `GET`, the server reads the file, encodes it in Base64, and the client decodes it and saves it.

## What this exercise covers

- Designing an application-layer protocol.
- Separating the network layer, the protocol layer, and the file layer.
- Sending binary data over a text protocol with Base64.

The extended version with thread-pool and process-pool servers and a stress test is in [`file-server-stress-test`](https://github.com/nabielvna/coursework-network-programming/tree/main/file-server-stress-test).
