import socket
import threading
import argparse  # command-line argument "-v" (verbose)

HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 1024

def handle_connection(client_socket, client_address, verbose):
    if verbose:
        print(f"Handling connection from {client_address}")
    buffer = ""

    with client_socket:
        while True:
            try:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    if verbose:
                        print(f"Connection closed from {client_address}")
                    break

                buffer += data.decode()

                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.rstrip('\r')
                    if verbose:
                        print(f"[{client_address}] Received: {line}")
                    client_socket.sendall((line + '\n').encode())

            except ConnectionResetError:
                if verbose:
                    print(f"Connection reset by {client_address}")
                break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            if args.v:
                print(f"Accepted connection from {client_address}")
            client_thread = threading.Thread(
                target=handle_connection,
                args=(client_socket, client_address, args.v),
                daemon=True
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
