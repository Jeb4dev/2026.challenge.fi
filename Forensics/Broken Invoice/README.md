# Broken Invoice

## Challenge

I just got an invoice from a company, but it seems to be corrupted.
Can you help me figure out what's wrong with it?

[Download](https://nextcloud.haaukins.com/s/F7Gx9zpPaPY927E/download)



\## Solution



Open file in notepad or use strings command in Linux. Look for `DDC{` 



On line 341 we find the flag.



````txt

/Type /StructElem

/S /H6

/T (DDC{ANOTHER\_INVOICE\_TO\_PRINT})

/E (DDC{ANOTHER\_INVOICE\_TO\_PRINT})

/Pg 7 0 R

/K \[6]

````



\*Flag\*: DDC{ANOTHER\_INVOICE\_TO\_PRINT}

