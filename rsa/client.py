import socket

def rsa_encrypt(plaintext, e, n):
    return pow(plaintext, e, n)

HOST = '127.0.0.1'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"[CLIENT] Terhubung ke {HOST}:{PORT}")

    # Terima public key
    data = s.recv(1024).decode()
    e, n = map(int, data.split(','))
    print(f"[CLIENT] Received public key e={e}, n={n}")

    # Minta input plaintext
    plaintext = int(input("[CLIENT] Masukkan plaintext (angka kecil): "))
    ciphertext = rsa_encrypt(plaintext, e, n)
    print(f"[CLIENT] Ciphertext = {ciphertext}")

    # Kirim ciphertext ke server
    s.sendall(str(ciphertext).encode())
    print("[CLIENT] Ciphertext dikirim ke server.")

    print("[CLIENT] Selesai.")
