# Multithreaded Time Server

A simple TCP time server written in Python. It serves many clients at the same time by running one thread per connection. This is a basic exercise from the Network Programming course.

## Features

- **Multithreaded:** serves several clients at once without blocking.
- **TCP:** reliable, ordered communication.
- **Text protocol:** one command to ask for the time, one to end the session.
- **Logging:** real-time log lines for every connection and request.
- **Fast restarts:** uses `SO_REUSEADDR` so the server can be restarted right away.

## Technical details

- Python 3, standard library only: `socket`, `threading`, `datetime`, `logging`, `sys`
- Port: `45000` (TCP)

## Run the server

```bash
python3 server.py
```

You should see a line like this:

```
2025-06-16 21:30:15,123 - Time server berjalan dan mendengarkan di port 45000...
```

## Try it

Keep the server running, open a second terminal, and connect with `netcat` or `telnet`:

```bash
netcat localhost 45000
```

Then type a command and press Enter.

## Protocol

| Command | Meaning | Server response |
|---|---|---|
| `TIME` | Ask for the current time | `JAM hh:mm:ss\r\n` |
| `QUIT` | Close the connection | none (the connection is closed) |
