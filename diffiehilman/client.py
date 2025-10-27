# client.py
import socket
import random

SERVER = '127.0.0.1'   # localhost
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER, PORT))
    print(f"[CLIENT] Terhubung ke {SERVER}:{PORT}")

    data = s.recv(4096).decode()
    p, g = map(int, data.split(","))
    print(f"[CLIENT] Received p = {p}, g = {g}")

    b = random.randint(2, p-2)
    print(f"[CLIENT] Private key (b) = {b}")
    B = pow(g, b, p)
    print(f"[CLIENT] Public key (B) = {B}")

    s.send(str(B).encode())
    A = int(s.recv(4096).decode())
    print(f"[CLIENT] Received server public (A) = {A}")

    shared = pow(A, b, p)
    print(f"[CLIENT] Shared key = {shared}")

    print("[CLIENT] Selesai.")

