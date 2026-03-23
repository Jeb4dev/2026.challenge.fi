import re
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def extract_b64_strings(file_content):
    """Finds all PowerShell variable assignments with string values."""
    # Matches: $VariableName = 'base64String...'
    pattern = r"\$([a-zA-Z_]\w*)\s*=\s*'([A-Za-z0-9+/=]+)'"
    return re.findall(pattern, file_content)


def attempt_decrypt(payload_b64, key_b64):
    """Attempts to decrypt the payload with the given key."""
    try:
        data = base64.b64decode(payload_b64)
        key = base64.b64decode(key_b64)

        # AES-256 requires a 32-byte key. IV is 16 bytes.
        if len(key) != 32 or len(data) < 16:
            return None

        iv = data[:16]
        ciphertext = data[16:]

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted.decode('utf-8')
    except Exception:
        # If padding is wrong or characters aren't valid UTF-8, it fails silently
        return None


def process_ps1_file(file_path):
    if not os.path.exists(file_path):
        print(f"[-] File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    variables = extract_b64_strings(content)
    keys = []
    payloads = []

    # Categorize base64 strings by their decoded length
    for name, val in variables:
        try:
            decoded_bytes = base64.b64decode(val)
            if len(decoded_bytes) == 32:
                keys.append((name, val))
            elif len(decoded_bytes) > 32:
                payloads.append((name, val))
        except Exception:
            continue

    print(f"\n" + "=" * 50)
    print(f"Targeting: {file_path}")
    print(f"Found {len(keys)} potential keys and {len(payloads)} potential payloads.")
    print("=" * 50)

    success_count = 0

    # Brute-force the variable combinations
    for p_name, p_val in payloads:
        for k_name, k_val in keys:
            result = attempt_decrypt(p_val, k_val)
            if result:
                success_count += 1
                print(f"[+] Decryption Successful!")
                print(f"    Payload Variable : ${p_name}")
                print(f"    Key Variable     : ${k_name}")
                print(f"    Decrypted Output :\n")
                print("-" * 40)
                print(result)
                print("-" * 40 + "\n")

    if success_count == 0:
        print("[-] No valid key/payload combinations found in this file.")


if __name__ == "__main__":
    # Add your specific file paths here
    files_to_check = [
        "req2_decoded.ps1",
        "req3_decoded.ps1",
        "req4_decoded.ps1"
    ]

    for ps1_file in files_to_check:
        process_ps1_file(ps1_file)