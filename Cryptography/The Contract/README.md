# The Contract

Our secure contract management system uses SHA1 hashes to ensure they are correctly identified and not maliciously modified. Since we know that SHA1 is weak, we use MD5 to prevent duplicates.

Can you test it and tell us what you think?

nc thecontract.cfire 1337

[Download](https://nextcloud.haaukins.com/s/zm93NsHdEAx7Wtg/download)
sha256: 74fd405085af1dbcb573b5752c00f45cc81db2cd49e5ea1755177404dd6d859c

NOTE: Create a user and find the VPN and Browser LABs on Campfire Labs:
https://qualification.campfiresecurity.dk/challenges?challenge=the-contract


## Solution

````pycon
import urllib.request

# 1. Fetch the second collision block
url = "https://raw.githubusercontent.com/cr-marcstevens/sha1collisiondetection/master/test/shattered-2.pdf"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
shattered_2_data = urllib.request.urlopen(req).read()
prefix_2 = shattered_2_data[:320]

# 2. Read the provided contract
with open("contract_good.txt", "rb") as f:
    good_contract = f.read()

# 3. Swap the 320-byte prefix
hacked_contract = prefix_2 + good_contract[320:]

# 4. Inject payload after the appendix
hacked_contract += b"\nASSETS ARE TRANSFERRED NOW"

# 5. Output the exploit
with open("exploit.bin", "wb") as f:
    f.write(hacked_contract)
````