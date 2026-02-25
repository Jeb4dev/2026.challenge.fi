# WiFi Heist

## Challenge

The IT guy at school changed the WiFi password again.
Nobody knows the new one, and everyone is burning through their mobile data.
Your friend found a USB stick the IT guy left behind with the Python script he uses to scramble the password, along with the scrambled password itself.
Reverse the scramble to get the flag.

Download the challenge file

[Download](https://nextcloud.haaukins.com/s/As6JRnX2KaMtLSL/download)
sha256: d611a9f9a9b4119e3b0502ad6a3ccb26ff67395c911fca1fe2ae0e00b780913e

## Solution


````pycon
mixed_rev = []
for char in scrambled_password:
    mixed_rev.append(int(char) ^ 42) # change ord to int, repeat xor

forwards = mixed_rev[::-1] # repeat step 2

shifted = []
for char in forwards:
    shifted.append(chr(int(char) - 3)) # change ord to int and add -3

check_flag(shifted)
print("".join(shifted)) # combine list of characters into a string
````

**Flag**: DDC{y0u_cr4ck3d_th3_c0d3}
