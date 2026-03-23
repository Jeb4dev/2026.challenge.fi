# Squeaky Clean 2

> 🔴 **Hard** — 1000 pts

## Challenge Description

So ehmmm… at least you didn’t get root!

## Solution

### Challenge 2: The Squeaky Clean Root (Unsolved)

**Target:** `10.42.2.189` (Containerized)

**Difficulty:** Medium/Hard

**Goal:** Escalate privileges to root.

#### 1. Post-Exploitation Enumeration

After gaining user access, **LinPEAS** was executed to hunt for escalation vectors. The environment was highly restricted ("Squeaky Clean"), with standard tools like `gdb`, `strace`, and `strings` removed. Key findings included:

* The `user` account was a member of the **`sudo` group**.
* A background process was caught running `apt-get update` in rapid bursts.
* **IP Forwarding** was enabled, and the host gateway was `172.17.0.1`.

#### 2. The Distraction: The APT Loop

A noisy background loop was discovered running:
`root /usr/bin/sudo -S /opt/update.sh`

Initial attempts focused on hijacking the `PATH` variable for the `apt-get` command or performing a Man-in-the-Middle attack on the APT repository. However, network analysis via `curl` proved the container had no internet access and DNS was not spoofed. The "burst" behavior was caused by the script instantly crashing and restarting, and the `-S` flag was determined to be a decoy.

#### 3. The Identified Vector: Python Library Hijacking

The most promising vector identified was a root-owned process:
`root su - user -c cd /home/user/app/; python3 /home/user/app/app.py`

This process effectively runs `app.py` as root but initiates from the `/home/user/app` directory, which is **writable by the user**.

Python’s `sys.path` (the search order for modules) was confirmed to start with `''` (the current working directory). This allows for a **Module Hijack**:

1. By creating a malicious `os.py` inside `/home/user/app/`, the root process would import the fake module instead of the standard library version.
2. The malicious module could contain a payload to copy `/bin/bash` to `/tmp/rootbash` and apply the SUID bit (`chmod +s`).

#### 4. Why it remained unsolved

Attempts to kill the `python3` process to trigger a restart caused the entire Docker container to crash, terminating the SSH session. The "Squeaky Clean" nature of the box likely required a more graceful hijack that maintained the application's functionality while executing the payload in the background, or an alternative exploit of the `Post-Invoke` APT hooks found in the `apt-config dump`.

**Potential Root Flag Location:** `/root/root.txt`
