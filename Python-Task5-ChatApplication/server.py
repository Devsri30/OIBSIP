"""
Chat Application — Server (Beginner Tier)
--------------------------------------------
A simple two-client relay chat server using sockets + threading.
Any message received from one client is broadcast to the other.

Run this FIRST, then start two instances of client.py.

Usage:
    python server.py
"""

import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5555

clients = []          # list of (connection, address, name)
clients_lock = threading.Lock()


def timestamp() -> str:
    return datetime.now().strftime("%H:%M")


def broadcast(message: str, sender_conn=None):
    """Send a message to every connected client except the sender."""
    with clients_lock:
        for conn, _addr, _name in clients:
            if conn is sender_conn:
                continue
            try:
                conn.sendall(message.encode("utf-8"))
            except OSError:
                pass


def remove_client(conn):
    with clients_lock:
        for entry in clients:
            if entry[0] is conn:
                clients.remove(entry)
                return entry[2]
    return None


def handle_client(conn: socket.socket, addr):
    name = None
    try:
        # First message from a client is treated as their chosen username
        name = conn.recv(1024).decode("utf-8").strip()
        with clients_lock:
            clients.append((conn, addr, name))

        print(f"[{timestamp()}] {name} connected from {addr}")
        broadcast(f"[{timestamp()}] * {name} has joined the chat *", sender_conn=conn)

        while True:
            data = conn.recv(1024)
            if not data:
                break  # client disconnected
            message = data.decode("utf-8")
            print(f"[{timestamp()}] {name}: {message}")
            broadcast(f"[{timestamp()}] {name}: {message}", sender_conn=conn)

    except (ConnectionResetError, ConnectionAbortedError):
        pass
    finally:
        removed_name = remove_client(conn)
        display_name = removed_name or name or "A user"
        print(f"[{timestamp()}] {display_name} disconnected")
        broadcast(f"[{timestamp()}] * {display_name} has left the chat *")
        conn.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("=" * 45)
    print("             CHAT SERVER")
    print("=" * 45)
    print(f"Listening on {HOST}:{PORT} ... (Ctrl+C to stop)\n")

    try:
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
