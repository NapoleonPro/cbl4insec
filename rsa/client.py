
# client.py
import socket

def string_to_blocks(text, block_size=6):
    """
    Convert string to blocks of 6-digit numbers
    Sesuai dengan laporan: 
    - Convert setiap karakter ke ASCII (3 digit dengan leading zero)
    - Gabungkan dan pecah jadi blok 6 digit
    """
    # Convert setiap karakter ke ASCII 3 digit
    ascii_codes = [str(ord(char)).zfill(3) for char in text]
    
    # Gabungkan semua ASCII codes
    combined = ''.join(ascii_codes)
    
    # Pecah jadi blok 6 digit
    blocks = []
    for i in range(0, len(combined), block_size):
        block = combined[i:i+block_size]
        # Pad dengan 0 jika kurang dari 6 digit
        block = block.ljust(block_size, '0')
        blocks.append(int(block))
    
    return blocks

def rsa_encrypt_block(plaintext, e, n):
    """Encrypt single block"""
    return pow(plaintext, e, n)

HOST = '127.0.0.1'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"[CLIENT] Terhubung ke {HOST}:{PORT}")
    print()

    # Terima public key
    data = s.recv(1024).decode()
    e, n = map(int, data.split(','))
    print(f"[CLIENT] Public key diterima:")
    print(f"  e = {e}")
    print(f"  n = {n}")
    print()

    # Minta input plaintext
    plaintext = input("[CLIENT] Masukkan pesan: ")
    
    # Convert string ke blok-blok
    plaintext_blocks = string_to_blocks(plaintext)
    print(f"[CLIENT] Plaintext blocks: {plaintext_blocks}")
    print()

    # Enkripsi setiap blok
    ciphertext_blocks = []
    print("[CLIENT] Enkripsi per blok:")
    for i, plain_block in enumerate(plaintext_blocks):
        if plain_block >= n:
            print(f"  WARNING: Blok {i+1} ({plain_block}) >= n ({n})")
            print(f"  Gunakan p dan q yang lebih besar!")
        cipher_block = rsa_encrypt_block(plain_block, e, n)
        ciphertext_blocks.append(cipher_block)
        print(f"  Blok {i+1}: {plain_block} -> {cipher_block}")
    
    print()
    print(f"[CLIENT] Ciphertext: {ciphertext_blocks}")
    print()

    # Kirim jumlah blok
    s.sendall(str(len(ciphertext_blocks)).encode())
    s.recv(1024)  # Wait for OK

    # Kirim setiap blok ciphertext
    for cipher_block in ciphertext_blocks:
        s.sendall(str(cipher_block).encode())
        s.recv(1024)  # Wait for OK
    
    print("[CLIENT] Ciphertext dikirim ke server.")
    print("[CLIENT] Selesai.")
