#!/usr/bin/env python3
import base64
import codecs

s = "xSbRFPNuKpLeguYhiCAFcddbchSQMY"

results = []
results.append(f"=== Secret_password analysis ===")
results.append(f"Input: {s}")
results.append(f"Length: {len(s)}")

# Try base64
try:
    padded = s + '=' * (-len(s) % 4)
    decoded = base64.b64decode(padded)
    results.append(f"\nBase64 decoded bytes: {decoded.hex()}")
    try:
        results.append(f"Base64 decoded UTF-8: {decoded.decode('utf-8')}")
    except:
        results.append(f"Base64 decoded latin-1: {decoded.decode('latin-1')}")
except Exception as e:
    results.append(f"Base64 failed: {e}")

# Try ROT13
rot13 = codecs.encode(s, 'rot_13')
results.append(f"\nROT13: {rot13}")

# Try reverse
results.append(f"Reversed: {s[::-1]}")

# Caesar shifts
results.append("\nCaesar shifts (all):")
for shift in range(1, 26):
    result = ""
    for c in s:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result += chr((ord(c) - base + shift) % 26 + base)
        else:
            result += c
    flag_mark = " *** DDC FOUND ***" if 'DDC' in result else ""
    results.append(f"  Shift {shift}: {result}{flag_mark}")

# Atbash
atbash = ""
for c in s:
    if c.isupper():
        atbash += chr(ord('Z') - (ord(c) - ord('A')))
    elif c.islower():
        atbash += chr(ord('z') - (ord(c) - ord('a')))
    else:
        atbash += c
results.append(f"\nAtbash: {atbash}")

# Base58
base58_alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
is_base58 = all(c in base58_alphabet for c in s)
results.append(f"\nIs valid Base58: {is_base58}")
if is_base58:
    num = 0
    for c in s:
        num = num * 58 + base58_alphabet.index(c)
    result_bytes = num.to_bytes((num.bit_length() + 7) // 8, 'big')
    results.append(f"Base58 decoded hex: {result_bytes.hex()}")
    try:
        results.append(f"Base58 decoded text: {result_bytes.decode('utf-8')}")
    except:
        results.append(f"Base58 decoded latin-1: {result_bytes.decode('latin-1')}")

# XOR with single bytes - looking for printable DDC
results.append("\nXOR results containing DDC:")
sbytes = s.encode()
ddc_found = []
for key in range(1, 256):
    xored = bytes([b ^ key for b in sbytes])
    try:
        decoded_str = xored.decode('ascii')
        if all(32 <= b < 127 for b in xored):
            if 'DDC' in decoded_str:
                ddc_found.append(f"  XOR 0x{key:02x}: {decoded_str}")
    except:
        pass
if ddc_found:
    results.extend(ddc_found)
else:
    results.append("  No XOR keys produce DDC")

# All printable XOR results (first 10)
results.append("\nFirst 10 all-printable XOR results:")
count = 0
for key in range(1, 256):
    xored = bytes([b ^ key for b in sbytes])
    try:
        decoded_str = xored.decode('ascii')
        if all(32 <= b < 127 for b in xored):
            if count < 10:
                results.append(f"  XOR 0x{key:02x}: {decoded_str}")
            count += 1
    except:
        pass
results.append(f"Total printable XOR results: {count}")

# Maybe it's the MSHTA var gfd that matters - gfd="1" so Profile1
# The challenge title is "Persistance is Key" - the KEY is in the registry
# The flag might be constructed from multiple registry values

# Check if base64 decode of secret_password gives flag-like output
results.append("\n\n=== Trying base64 variations ===")
# standard
try:
    d = base64.b64decode(s + "==")
    results.append(f"b64 standard: {d}")
except Exception as e:
    results.append(f"b64 standard err: {e}")

# what if the password is actually a cipher of the flag using the mshta key
# The mshta key reads Profile+gfd where gfd=1, so Profile1
# Profile1 = new ActiveXObject("WScript.Shell").Run(...)
# Secret_password = xSbRFPNuKpLeguYhiCAFcddbchSQMY

# Let's try Vigenere with various likely keys
results.append("\n=== Vigenere decoding ===")
def vigenere_decode(ciphertext, key):
    result = ""
    key_idx = 0
    for c in ciphertext:
        if c.isalpha():
            shift = ord(key[key_idx % len(key)].lower()) - ord('a')
            base = ord('A') if c.isupper() else ord('a')
            result += chr((ord(c) - base - shift) % 26 + base)
            key_idx += 1
        else:
            result += c
    return result

test_keys = ['persistence', 'persistanceiskey', 'iskey', 'key', 'ddc', 'flag',
             'registry', 'bags', 'desktop', 'profile', 'discord', 'update',
             'mshta', 'wscript', 'shell', 'secret', 'password', 'challenge']
for k in test_keys:
    r = vigenere_decode(s, k)
    flag_mark = " *** DDC ***" if 'DDC' in r else ""
    results.append(f"  key='{k}': {r}{flag_mark}")

with open('/home/kali/PycharmProjects/ghindra/flag_results.txt', 'w') as f:
    f.write('\n'.join(str(r) for r in results))

print("Done - results written to flag_results.txt")

