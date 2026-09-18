"""
✅ How to run (PyCharm workflow)

Run tcp_server.py first

Right‑click → Run
Leave it running

Run tcp_client.py

Right‑click → Run
You’ll see the message printed
"""

import socket

HOST = socket.gethostname()  # Or "127.0.0.1"
PORT = 9337
BUFFER_SIZE = 1024


def run_client() -> None:
    """Connect to the TCP server and receive a message."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        data = client_socket.recv(BUFFER_SIZE)

    print("[CLIENT] Message received:")
    print(data.decode("utf-8"))


if __name__ == "__main__":
    try:
        run_client()
    except ConnectionRefusedError:
        print("[CLIENT] Could not connect to server. Is it running?")
    except Exception as exc:
        print(f"[CLIENT] Unexpected error: {exc}")
