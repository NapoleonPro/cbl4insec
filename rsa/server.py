import socket
import random
from math import gcd

# Fungsi bantu
def generate_keypair():
    # pilih dua bilangan prima kecil (biar simulasi cepat)
    primes = [101, 103, 107, 109, 113, 127, 131]
    p = random.choice(primes)
    q = random.choice([x for x in primes if x != p])
    n = p * q
    phi = (p - 1) * (q - 1)

    # pilih e yang relatif prima terhadap phi
    e = 3
    while gcd(e, phi) != 1:
        e += 2

    # cari d (modular inverse)
    d = pow(e, -1, phi)
    return (e, d, n, p, q)

def rsa_decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)

# Setup server socket
HOST = '127.0.0.1'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[SERVER] Listening on {HOST}:{PORT} - tunggu client...")

    conn, addr = s.accept()
    with conn:
        print(f"[SERVER] Client connected:", addr)

        e, d, n, p, q = generate_keypair()
        print(f"[SERVER] p={p}, q={q}, n={n}, e={e}, d={d}")

        # Kirim public key ke client
        conn.sendall(f"{e},{n}".encode())
        print("[SERVER] Public key dikirim ke client.")

        # Terima ciphertext dari client
        data = conn.recv(1024)
        ciphertext = int(data.decode())
        print(f"[SERVER] Ciphertext diterima: {ciphertext}")

        # Dekripsi
        plaintext = rsa_decrypt(ciphertext, d, n)
        print(f"[SERVER] Plaintext hasil dekripsi: {plaintext}")

        print("[SERVER] Selesai.")
