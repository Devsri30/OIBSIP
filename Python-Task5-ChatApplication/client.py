"""
Chat Application — Client (Beginner Tier)
--------------------------------------------
Connects to server.py and lets a user send/receive real-time messages.
Run server.py first, then run this script in two separate terminals
to chat between two "users" on localhost.

Usage:
    python client.py
"""

import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 5555


def listen_for_messages(sock: socket.socket):
    """Background thread: continuously print any message from the server."""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[Disconnected from server]")
                break
            print("\n" + data.decode("utf-8"))
            print("You: ", end="", flush=True)
        except OSError:
            break


def main():
    print("=" * 45)
    print("             CHAT CLIENT")
    print("=" * 45)

    name = input("Choose a username: ").strip() or "Anonymous"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("⚠ Could not connect to server. Is server.py running?")
        sys.exit(1)

    sock.sendall(name.encode("utf-8"))
    print(f"Connected as '{name}'. Type a message and press Enter. Type /quit to exit.\n")

    listener = threading.Thread(target=listen_for_messages, args=(sock,), daemon=True)
    listener.start()

    try:
        while True:
            message = input("You: ")
            if message.strip().lower() == "/quit":
                break
            if message:
                sock.sendall(message.encode("utf-8"))
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        sock.close()
        print("Disconnected.")


if __name__ == "__main__":
    main()
