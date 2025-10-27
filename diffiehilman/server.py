# server.py
import socket
import random

def choose_prime():
    primes = [101,103,107,109,113,127,131,137,139,149]
    return random.choice(primes)

HOST = '127.0.0.1'   # localhost
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[SERVER] Listening on {HOST}:{PORT} - tunggu client...")
    conn, addr = s.accept()
    with conn:
        print(f"[SERVER] Client connected: {addr}")
        p = choose_prime()
        g = random.randint(2, p-1)
        print(f"[SERVER] p = {p}, g = {g}")
        conn.send(f"{p},{g}".encode())

        a = random.randint(2, p-2)
        print(f"[SERVER] Private key (a) = {a}")
        A = pow(g, a, p)
        print(f"[SERVER] Public key (A) = {A}")

        data = conn.recv(4096).decode()
        B = int(data)
        print(f"[SERVER] Received client public (B) = {B}")

        conn.send(str(A).encode())
        shared = pow(B, a, p)
        print(f"[SERVER] Shared key = {shared}")

        print("[SERVER] Selesai. Tekan Ctrl+C jika mau stop server.")
