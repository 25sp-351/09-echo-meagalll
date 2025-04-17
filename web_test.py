import socket
import threading
import argparse

HOST = '127.0.0.1'
PORT = 2345

def handle_connection(client_socket, client_address, verbose=False):
    if verbose:
        print(f"[+] Connection from {client_address}")

    with client_socket:
        request = client_socket.recv(1024).decode()

        if verbose:
            print(f"[{client_address}] Request:\n{request.strip()}")

        # Extract requested path from the request
        lines = request.splitlines()
        path = "/"
        if lines:
            parts = lines[0].split()
            if len(parts) >= 2:
                path = parts[1]

        # Build HTTP response
        response_body = f"<h1>Hello {path}</h1>"
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(response_body.encode())}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{response_body}"
        )

        client_socket.sendall(response.encode())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", action="store_true", help="Enable verbose output")
    parser.add_argument("-p", type=int, default=2345, help="Port to listen on")
    args = parser.parse_args()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, args.p))
    server_socket.listen()
    print(f"[🌐] HTTP server listening on http://{HOST}:{args.p}")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(
            target=handle_connection,
            args=(client_socket, client_address, args.v),
            daemon=True
        )
        thread.start()

if __name__ == "__main__":
    main()

