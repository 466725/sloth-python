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


def start_server() -> None:
    """Start a simple TCP server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"\n[SERVER] Listening on {HOST}:{PORT}\n")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"[SERVER] Connection established with {addr}")

                message = f"Thank you for connecting from {addr}"
                conn.sendall(message.encode("utf-8"))

                print(f"[SERVER] Message sent to {addr}\n")


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down gracefully.")
