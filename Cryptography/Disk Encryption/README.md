# Disk Encryption

## Challenge

I implemented my own disk encryption service using the standard AES-XTS mode.

It’s still in beta, so I included a debug mode that users can try.
It’s not a security issue, because it only encrypts using ECB, and no one else knows the key.

Only administrator users can read the key anyway.

Can it be hacked?

nc diskenc.cfire 1337

[Download](https://nextcloud.haaukins.com/s/8HjrLdHMLHGY8A9/download)
sha256: 56202e94379438fa982c71239e5f0e56bc60c8ed6cbb972e76a7cb534023c128

NOTE: Create a user and find the VPN and Browser LABs on Campfire Labs:
https://qualification.campfiresecurity.dk/challenges?challenge=disk-encryption

## Solution

### Challenge Overview: The XOR Known Plaintext/Key Reuse Attack

The core of this challenge revolves around a cryptographic operation called XOR (Exclusive OR, represented by the ⊕ symbol). XOR is a fundamental building block of encryption, but it has a very specific mathematical property: it is perfectly reversible.

The "Why" boils down to these three rules of XOR math:

    Encryption: Plaintext⊕Key=Ciphertext

    Decryption: Ciphertext⊕Key=Plaintext

    Key Recovery (The Vulnerability): Ciphertext⊕Plaintext=Key

Because of Rule #3, if an attacker has an encrypted message (Ciphertext) and can guess even a small part of the original unencrypted message (Plaintext), they can instantly extract the Key.

### Step-by-Step Writeup
1. The Vulnerability: Reused Keys & Predictable Data

In cryptography, if you encrypt data using XOR (like a stream cipher or a One-Time Pad), you must never reuse the key. If the key is reused across multiple files or messages, the system becomes vulnerable to a Known Plaintext Attack (KPA).

In this challenge, we encountered hexadecimal strings being manipulated via XOR. We also recognized a predictable piece of data: the hex string 6461656d6f6e3a783a303a303a646165, which translates to standard Linux /etc/passwd contents: daemon:x:0:0:dae.
2. The Exploit: "Crib Dragging" or Key Recovery

Because we knew a piece of the original plaintext (daemon:x:0:0:dae), we could exploit the reversible nature of XOR.

By taking the known plaintext and XORing it against an unknown string (either a ciphertext or another key), we force the math to work in reverse.

    If f9e988b0b59a0541d57abe2cbf88340a was an encrypted file, XORing it with the daemon text revealed the hidden encryption key.

    If f9e988b0b59a0541d57abe2cbf88340a was the key itself, XORing it against the daemon text allowed us to manually forge an encrypted ciphertext.

3. Executing the Final Payload

Once we verified the key (or the relationship between the strings), we applied it to the next piece of the puzzle.

We took the next hexadecimal target:
5e974a9a0cb78ba0d264927a9193840d

And XORed it with our known variable:
f9e988b0b59a0541d57abe2cbf88340a

Because Ciphertext⊕Key=Plaintext, this operation cleanly stripped the XOR encryption layer away, giving us the resulting output: a77ec22ab92d8ee1071e2c562e1bb007, unlocking the next stage of the challenge.

Flag: `DDC{d1sk_3ncrypt10n_1s_w31rd}`

````shell
                                                                                                  
┌──(kali㉿kali)-[~]
└─$ nc 10.42.11.62 1337
File 'passwd' encrypted in memory.

For debugging purposes, I can encrypt two blocks under ECB.
00000000000000000000000000000000 02000000000000000000000000000000
59ef1f82d2959c119b42db7701b36052 f9e988b0b59a0541d57abe2cbf88340a 

For debugging purposes, I can also restore an encrypted block in memory, just give me number and contents (but do not change usernames).
a
Traceback (most recent call last):
  File "server.py", line 75, in <module>
    number, contents = line.split()
ValueError: not enough values to unpack (expected 2, got 1)
                                                         
┌──(kali㉿kali)-[~]
└─$ nc 10.42.11.62 1337
File 'passwd' encrypted in memory.

For debugging purposes, I can encrypt two blocks under ECB.
9d88eddddaf43f39ef4a841c85ec556f 00000000000000000000000000000000
5e974a9a0cb78ba0d264927a9193840d f9dc2f0101f96f531ba373216e31b9a5 

For debugging purposes, I can also restore an encrypted block in memory, just give me number and contents (but do not change usernames).
2 a77ec22ab92d8ee1071e2c562e1bb007

Non-root administrator user 'daemon' is given access to secret: DDC{d1sk_3ncrypt10n_1s_w31rd}
````
