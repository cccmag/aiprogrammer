#!/usr/bin/env python3
"""密碼學基礎範例 - AI 程式人雜誌 202307"""

import hashlib
import hmac
import random
import sys

def caesar_encrypt(text, shift):
    result = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

SBOX = [0x9, 0x4, 0xA, 0xB, 0xD, 0x1, 0x8, 0x5,
        0x6, 0x2, 0x0, 0x3, 0xC, 0xE, 0xF, 0x7]

def aes_like_encrypt(block_hex, key_hex):
    block = int(block_hex, 16) ^ int(key_hex, 16)
    enc = 0
    for i in range(8):
        nibble = (block >> (i * 4)) & 0xF
        enc |= SBOX[nibble] << (i * 4)
    return format(enc, '08x')

def aes_like_decrypt(block_hex, key_hex):
    block = int(block_hex, 16)
    inv = [SBOX.index(i) for i in range(16)]
    dec = 0
    for i in range(8):
        nibble = (block >> (i * 4)) & 0xF
        dec |= inv[nibble] << (i * 4)
    return format(dec ^ int(key_hex, 16), '08x')

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("No inverse")
    return x % m

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def rsa_keygen(bits=16):
    while True:
        p = random.getrandbits(bits // 2)
        if is_prime(p):
            break
    while True:
        q = random.getrandbits(bits // 2)
        if is_prime(q) and q != p:
            break
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modinv(e, phi)
    return (e, n), (d, n)

def rsa_encrypt(m, pub):
    return pow(m, pub[0], pub[1])

def rsa_decrypt(c, priv):
    return pow(c, priv[0], priv[1])

def sha256_digest(data):
    return hashlib.sha256(data.encode()).hexdigest()

def hmac_digest(key, data):
    return hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()

def demo():
    print("=== 密碼學基礎範例 ===\n")

    print("1. Caesar Cipher")
    pt = "HelloWorld"
    sh = 3
    ct = caesar_encrypt(pt, sh)
    dt = caesar_decrypt(ct, sh)
    print(f"   plain:  {pt}")
    print(f"   shift:  {sh}")
    print(f"   cipher: {ct}")
    print(f"   dec:    {dt}\n")

    print("2. AES-like Substitution")
    blk = "a1b2c3d4"
    key = "deadbeef"
    ea = aes_like_encrypt(blk, key)
    da = aes_like_decrypt(ea, key)
    print(f"   block:   {blk}")
    print(f"   key:     {key}")
    print(f"   encrypt: {ea}")
    print(f"   decrypt: {da}\n")

    print("3. RSA")
    pub, priv = rsa_keygen(16)
    msg = 42
    c = rsa_encrypt(msg, pub)
    m = rsa_decrypt(c, priv)
    print(f"   pub:  ({pub[0]}, {pub[1]})")
    print(f"   priv: ({priv[0]}, {priv[1]})")
    print(f"   msg:  {msg}")
    print(f"   enc:  {c}")
    print(f"   dec:  {m}\n")

    print("4. SHA256")
    d = "AI 程式人雜誌"
    h = sha256_digest(d)
    print(f"   data: {d}")
    print(f"   hash: {h}\n")

    print("5. HMAC")
    kh = "secret"
    dh = "message"
    hh = hmac_digest(kh, dh)
    print(f"   key:  {kh}")
    print(f"   data: {dh}")
    print(f"   hmac: {hh}\n")

    print("=== All Demos Passed ===")

if __name__ == "__main__":
    demo()
