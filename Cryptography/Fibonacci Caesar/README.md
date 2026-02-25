# Fibonacci Caesar

## Challenge

One of the oldest forms of encryption is the Caesar cipher, where each letter is shifted by a secret key.

This time, someone has modified the Caesar cipher using the Fibonacci sequence.

Can you decrypt the flag?

Remember to submit the result in the flag format.
(ddc example flag -> DDC{example_flag})

[Download](https://nextcloud.haaukins.com/s/BfzAcy9ATsDoqAf/download)
sha256: 3a516c2d013845625d5be2132b093c68bf693d23d560583b805ff81adf8cf43f

## Solution

n=47: ddc pisano sequence solves fibonacci caesar

The Fibonacci sequence is defined as follows:

```
F(0) = 0
F(1) = 1
F(2) = 1
F(3) = 2
F(4) = 3
F(5) = 5
F(6) = 8
F(7) = 13
F(8) = 21
F(n) = F(n-1) + F(n-2) for n >
```

key is 2^128

but pisano sequence is periodic with period 60 for modulo 26 (number of letters in the alphabet)

Flag: DDC{pisano_sequence_solves_fibonacci_caesar}