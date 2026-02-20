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
