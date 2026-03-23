# Squeaky Clean 1

> 🔴 **Hard** — 1000 pts

## Challenge Description

I made this challenge. It aint much, but it's honest work. Fewer features, fewer unintendeds! That's what I call a clean challenge!

Visit me at: ``http://squeaky-clean.cfire``

## Solution

### Challenge 1: The Secure Dispenser

**Target:** `10.42.2.189`

**Difficulty:** Easy/Medium

**Goal:** Obtain the user flag.

#### 1. Enumeration & Initial Access

The initial scan of the target machine revealed a web application running on Port 80 and a filtered high port (29381). Upon navigating to the website, a standard login form was presented.

Static analysis and manual testing of the login form revealed a **SQL Injection** vulnerability in the `username` field. By utilizing a common tautology payload:
`' OR '1'='1' --`

The application was tricked into bypass authentication, granting access to an internal dashboard.

#### 2. Local File Inclusion (LFI)

The dashboard featured a "Read File" function that accepted a filename as a GET parameter. Testing this for Path Traversal revealed that the application was vulnerable. By navigating to:
`http://10.42.2.189/dashboard?file=../../../../etc/passwd`

The system's passwd file was leaked. Crucially, the web application code itself (`app.py`) was retrieved, revealing the use of a SQLite database and the hardcoded credentials: `admin : PasswordIsNotRelevantForThisChallenge`.

#### 3. Foothold via SSH

The LFI was further exploited to check for SSH keys. An authorized key was discovered in `/home/user/.ssh/authorized_keys`. By copying the corresponding private key found during the reconnaissance phase, an SSH session was established:
`ssh -i ~/.ssh/ctf_key user@10.42.2.189`

#### 4. The User Flag

Inside the user's home directory, a SUID binary named `flag.bin` was found. While standard `strings` and local `strace` analysis suggested it was a secure "dispenser" designed only to read `/root/backend/user.txt`, executing it as the `user` account successfully printed the flag:
**Flag:** `DDC{Sql1te_To_Auth0riz3d?!}`
