import socket
import time

def test_partial_lines():
    with socket.create_connection(("127.0.0.1", 65432)) as sock:
        sock.sendall(b"Hello, thi")
        time.sleep(1)
        sock.sendall(b"s is a test\n")
        response = sock.recv(1024)
        print("Partial Line Response:", response.decode())

def test_multiple_lines():
    with socket.create_connection(("127.0.0.1", 65432)) as sock:
        sock.sendall(b"line1\nline2\nline3\n")
        sock.shutdown(socket.SHUT_WR)  # let server know we're done
        response = b""
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            response += chunk
        print("Multiple Lines Response:\n" + response.decode())

print("=== Partial Line Test ===")
test_partial_lines()
print("=== Multiple Lines Test ===")
test_multiple_lines()

