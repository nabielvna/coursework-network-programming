# File Server Stress Test

An extension of [`file-server`](https://github.com/nabielvna/coursework-network-programming/tree/main/file-server) that compares two concurrency models under load: a **thread pool** and a **process pool**. A script runs every scenario automatically and records the results in a CSV file.

The protocol is the same as in `file-server` (`LIST`, `GET`, `UPLOAD`, `DELETE`, Base64 content, JSON replies ended by `\r\n\r\n`).

## Files

| File | Role |
|---|---|
| `server_mt_pool.py` | Server that uses a `ThreadPoolExecutor` |
| `server_mp_pool.py` | Server that uses a `ProcessPoolExecutor` |
| `client_lib.py` | Client functions `download_file` and `upload_file` |
| `file_protocol.py`, `file_interface.py` | Protocol parsing and file operations |
| `stress_test.py` | Runs all scenarios and writes `results_auto.csv` |
| `make_test_files.py` | Creates the 10, 50, and 100 MB test files |
| `testing_result/` | Screenshots of test runs |
| `result_backup/` | Results of earlier runs |

Both servers listen on port `6666` and take the number of workers with `-w` or `--workers` (default `5`).

## Run it

1. Create the test files (they are not stored in the repository):

   ```bash
   python make_test_files.py
   ```

2. Run all scenarios:

   ```bash
   python stress_test.py
   ```

   The script starts and stops the right server for each scenario, so you do not start a server yourself. It can be stopped and started again; it continues after the last scenario recorded in `results_auto.csv`.

You can also start a single server by hand:

```bash
python server_mt_pool.py --workers 5
```

## Scenarios

Each scenario is one combination of:

| Parameter | Values |
|---|---|
| Server model | `mt` (threads), `mp` (processes) |
| Operation | download, upload |
| File size | 10 MB, 50 MB, 100 MB |
| Number of clients | 1, 5, 50 |
| Number of server workers | 1, 5, 50 |

That is 108 combinations. When there are more than 10 clients and more clients than server workers, at most 10 clients run at the same time. Otherwise the number of simultaneous clients is the smaller of the client count and the worker count.

## Results

`results_auto.csv` has one row per scenario with these columns: `No`, `ServerModel`, `Operation`, `Volume`, `ClientPool`, `ServerPool`, `TimePerClient(s)`, `Throughput(bytes/s)`, `ClientOK`, `ClientFail`, `ServerOK`, `ServerFail`.

The results in this repository are incomplete: only 15 of the 108 scenarios were recorded. Scenarios up to number 15 were run before the servers accepted the worker count as an argument, so their server pool column does not reflect a real setting (see `result_backup/1_fixed_server_worker/readme.md`).
