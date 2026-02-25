import string

alphabet = 'abcdefghijklmnopqrstuvwxyzæøå{}_'

# Rotate each character by the index of the key character
def xor(a, b):
    # Ignore spaces
    if a in string.whitespace:
        return a
    return alphabet[(alphabet.index(a) ^ alphabet.index(b))]

def caesar_encrypt(key, text):
    ciphertext = ""
    for i in range(len(text)):
        ciphertext += xor(text[i], key)
    return ciphertext

def main():
    text = "pporkmhce}taii_}tomi}m{s"

    for key in alphabet:
        ciphertext = caesar_encrypt(key, text)
        print(ciphertext.encode("utf-8"))


if __name__ == '__main__':
    main()
