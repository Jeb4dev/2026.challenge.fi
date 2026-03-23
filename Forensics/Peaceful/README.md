# Peaceful

> 🔴 **Hard** — 1000 pts

## Challenge Description

I had this amazingly peaceful dream, but my memory of it is a bit off. My dream was based on events on the 14th of December. Can you help me find out what happened in my dream?

Password to the zip: ``QKej9r6KGAl1``
[Handout](https://nextcloud.haaukins.com/s/PYzRq7aJamjTEti/download)

## Solution (ai copywritten)

The challenge provides a memory dump (`flag.mem`). The description heavily hints at a specific date: **December 14th**.

While the intended, "hard" path might have been to load the dump into a heavy forensics framework like Volatility, I can solve this much faster by carving strings and looking for the Unix epoch timestamp for that date.

### Step 1: Pinpoint the Timestamp

First, I figure out the Unix timestamp for December 14, 2025. That date falls into the range of `1765717200` to `1765803600`. Knowing this, I just need to search the memory dump for any 10-digit numbers starting with `176`. why 176 instead of 1765 you might wonder, and so do I, real date was December 18th... Really challenge creator?

### Step 2: Grep the Memory Dump

We extract the readable text using `strings` and use a regex pattern with `grep` to hunt for timestamps in that range:

```bash
strings -a flag.mem | grep -E "176[0-9]{7}"

```

Checking the output around those timestamps, I find an interesting hit slightly after the 14th (specifically Thursday, December 18, 2025 at 12:32:40 PM GMT). Next to it is a highly suspicious, one-line shell command:

```bash
echo H4sIABDzQ2kA/x3A0QmAUAgF0JWU3OC9PS6Rn/cvTSTaXejsvd6SX8HV0ZKwK/IkG3kfeIQWSo3+BuBQfyotAAAA > hemlig.txt && base64 -d hemlig.txt | gunzip && sleep 1000

```

### Step 3: Decode the Payload

This command writes a Base64-encoded string into a file called `hemlig.txt`, decodes it, and then decompresses it with `gunzip`.

Instead of running their exact command, I can just pipe the string directly into the decoding tools on our own terminal to reveal the hidden contents:

```bash
echo "H4sIABDzQ2kA/x3A0QmAUAgF0JWU3OC9PS6Rn/cvTSTaXejsvd6SX8HV0ZKwK/IkG3kfeIQWSo3+BuBQfyotAAAA" | base64 -d | gunzip
```

## Flag

`DDC{w000000w_d1d_y0u_4ctually_us3_v0l4t1l1ty}`
