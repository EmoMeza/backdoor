import hashlib, binascii
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def create_key(word):
    salt = "your_salt"  # Replace with your own salt
    dk = hashlib.pbkdf2_hmac('sha256', word.encode(), salt.encode(), 100000)
    return binascii.hexlify(dk).decode()

def encrypt_file(key, filename):
    data = None
    with open(filename, 'rb') as file:
        data = file.read()

    cipher = AES.new(key, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))

    with open(filename + ".enc", 'wb') as file_enc:
        file_enc.write(ct_bytes)

    os.remove(filename)  # Delete the original file after encryption

def encrypt_files_in_dir(key, dir_path):
    for dirpath, _, files in os.walk(dir_path):
        for filename in files:
            filepath = os.path.join(dirpath, filename)
            encrypt_file(key, filepath)

def decrypt_file(key, filename):
    data = None
    with open(filename, 'rb') as file:
        data = file.read()

    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(data), AES.block_size)

    with open(filename.replace(".enc", ""), 'wb') as file_dec:
        file_dec.write(pt)

def decrypt_files_in_dir(key, dir_path):
    for dirpath, _, files in os.walk(dir_path):
        for filename in files:
            if filename.endswith(".enc"):
                filepath = os.path.join(dirpath, filename)
                decrypt_file(key, filepath)
                os.remove(filepath)

word = "example"
key = create_key(word).encode()[:16]  # Convert the key to bytes and take the first 16 bytes
print(key)

dir_path = "./test"
# encrypt_files_in_dir(key, dir_path)
# decrypt_files_in_dir(key, dir_path)