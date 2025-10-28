# server.py
import socket
import random
from math import gcd

def choose_prime_pq():
    
    primes_pq = [

        179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
        233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
        283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
        353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
        419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
        467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
        547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
        607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
        661, 673, 677, 683, 691, 701, 709, 719, 727, 733,
        739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
        811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
        877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
        947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013
    ]
    return random.choice(primes_pq)

def choose_e_from_list(phi):
    
    primes_e = [
        1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069,
        1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151,
        1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223,
        1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291,
        1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373,
        1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451,
        1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511,
        1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583,
        1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657,
        1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733,
        1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811,
        1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889,
        1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987,
        1993, 1997, 1999, 2003, 2011, 2017, 2027, 2029, 2039, 2053,
        2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2129,
        2131, 2137, 2141, 2143, 2153, 2161, 2179, 2203, 2207, 2213,
        2221, 2237, 2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287,
        2293, 2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357
    ]
    valid_e = [e for e in primes_e if 1 < e < phi and gcd(e, phi) == 1]
    if not valid_e:
        e = 3
        while gcd(e, phi) != 1:
            e += 2
        return e
    return random.choice(valid_e)

def generate_keypair():
    
    p = choose_prime_pq()
    q = choose_prime_pq()
    while p == q:
        q = choose_prime_pq()
    
    n = p * q
    phi = (p - 1) * (q - 1)
    e = choose_e_from_list(phi)
    d = pow(e, -1, phi)
    
    return (e, d, n, p, q)

def blocks_to_string(blocks):
    
    combined = ''.join(str(block).zfill(6) for block in blocks)
    
    result = ''
    for i in range(0, len(combined), 3):
        code = int(combined[i:i+3])
        if code == 0:
            continue  # skip padding '000'
        result += chr(code)
    
    return result
def rsa_decrypt_block(ciphertext, d, n):
    """Decrypt single block"""
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
        print(f"[SERVER] RSA Key Generation:")
        print(f"  p = {p}, q = {q}")
        print(f"  n = {n}")
        print(f"  e = {e}, d = {d}")
        print()

        # Kirim public key ke client
        conn.sendall(f"{e},{n}".encode())
        print("[SERVER] Public key dikirim ke client.")
        print()

        # Terima jumlah blok
        num_blocks = int(conn.recv(1024).decode())
        print(f"[SERVER] Akan menerima {num_blocks} blok ciphertext")
        conn.sendall(b"OK")

        # Terima setiap blok ciphertext
        ciphertext_blocks = []
        for i in range(num_blocks):
            data = conn.recv(1024).decode()
            cipher_block = int(data)
            ciphertext_blocks.append(cipher_block)
            conn.sendall(b"OK")
        
        print(f"[SERVER] Ciphertext diterima: {ciphertext_blocks}")
        print()

        # Dekripsi setiap blok
        plaintext_blocks = []
        print("[SERVER] Dekripsi per blok:")
        for i, cipher_block in enumerate(ciphertext_blocks):
            plain_block = rsa_decrypt_block(cipher_block, d, n)
            plaintext_blocks.append(plain_block)
            print(f"  Blok {i+1}: {cipher_block} -> {plain_block}")
        
        print()
        print(f"[SERVER] Plaintext blocks: {plaintext_blocks}")
        
        # Convert blocks ke string
        plaintext_message = blocks_to_string(plaintext_blocks)
        print(f"[SERVER] Plaintext message: '{plaintext_message}'")
        print()
        print("[SERVER] Selesai.")