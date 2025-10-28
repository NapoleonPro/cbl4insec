# server.py
import socket
import random

def choose_prime():
    """Memilih bilangan prima dari daftar yang tersedia"""
    primes = [
        2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417, 2423,
        2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531,
        2539, 2543, 2549, 2551, 2557, 2579, 2591, 2593, 2609, 2617,
        2621, 2633, 2647, 2657, 2659, 2663, 2671, 2677, 2683, 2687,
        2689, 2693, 2699, 2707, 2711, 2713, 2719, 2729, 2731, 2741,
        2749, 2753, 2767, 2777, 2789, 2791, 2797, 2801, 2803, 2819,
        2833, 2837, 2843, 2851, 2857, 2861, 2879, 2887, 2897, 2903,
        2909, 2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999,
        3001, 3011, 3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079,
        3083, 3089, 3109, 3119, 3121, 3137, 3163, 3167, 3169, 3181,
        3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251, 3253, 3257,
        3259, 3271, 3299, 3301, 3307, 3313, 3319, 3323, 3329, 3331,
        3343, 3347, 3359, 3361, 3371, 3373, 3389, 3391, 3407, 3413,
        3433, 3449, 3457, 3461, 3463, 3467, 3469, 3491, 3499, 3511,
        3517, 3527, 3529, 3533, 3539, 3541, 3547, 3557, 3559, 3571,
        3581, 3583, 3593, 3607, 3613, 3617, 3623, 3631, 3637, 3643,
        3659, 3671, 3673, 3677, 3691, 3697, 3701, 3709, 3719, 3727,
        3733, 3739, 3761, 3767, 3769, 3779, 3793, 3797, 3803, 3821,
        3823, 3833, 3847, 3851, 3853, 3863, 3877, 3881, 3889, 3907,
        3911, 3917, 3919, 3923, 3929, 3931, 3943, 3947, 3967, 3989
    ]
    return random.choice(primes)

HOST = '0.0.0.0'
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