# -*- coding: utf-8 -*-

"""
gdown.utils
~~~~~~~~~~~~~~~~~~~

This module provides utility functions that are used within gdown.

"""

import struct
import base64
from Crypto.Cipher import AES


def aes_cbc_encrypt(data, key):
    aes_cipher = AES.new(key, AES.MODE_CBC, '\0' * 16)
    return aes_cipher.encrypt(data)


def aes_cbc_encrypt_a32(data, key):
    return str_to_a32(aes_cbc_encrypt(a32_to_str(data), a32_to_str(key)))


def stringhash(str, aeskey):
    s32 = str_to_a32(str)
    h32 = [0, 0, 0, 0]
    for i in range(len(s32)):
        h32[i % 4] ^= s32[i]
    for r in range(0x4000):
        h32 = aes_cbc_encrypt_a32(h32, aeskey)
    return a32_to_base64((h32[0], h32[2]))


def prepare_key(arr):
    pkey = [0x93C467E3, 0x7DB0C7A4, 0xD1BE3F81, 0x0152CB56]
    for r in range(0x10000):
        for j in range(0, len(arr), 4):
            key = [0, 0, 0, 0]
            for i in range(4):
                if i + j < len(arr):
                    key[i] = arr[i + j]
            pkey = aes_cbc_encrypt_a32(pkey, key)
    return pkey


def a32_to_str(a):
    return struct.pack('>%dI' % len(a), *a)


def str_to_a32(b):
    if len(b) % 4:  # pad to multiple of 4
        b += '\0' * (4 - len(b) % 4)
    return struct.unpack('>%dI' % (len(b) / 4), b)


def base64_url_encode(data):
    data = base64.b64encode(data)
    for search, replace in (('+', '-'), ('/', '_'), ('=', '')):
        data = data.replace(search, replace)
    return data


def a32_to_base64(a):
    return base64_url_encode(a32_to_str(a))
