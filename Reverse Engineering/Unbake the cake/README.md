# Unbake the cake

## Challenge

I found this delicious ASCII cake online, and I really want to try the recipe myself, but one ingredient is missing!

Please help me find the secret string!

Here it is: [Download](https://nextcloud.haaukins.com/s/Wc26J4gJg6sRG4T/download?path=&files=unbake_the_cake.zip)
sha256: bb9024aa72e889c4fa4460d824ef57c0f73fa340e7a525f8cfc67baa95a58735

## Solution

Challenge is simple python script that we need to perform backwards.

````py
def mix(a, b):
    doughmix = list(dough)
    doughmix[a], doughmix[b] = doughmix[b], doughmix[a]
    doughmix = "".join(doughmix)

    return doughmix

dough = "oligrunggflerk__oluubnstagmiagekss" # "baked" flag in the cake
dough = mix(21,24)
dough = mix(12,23)
dough = mix(8,28)
dough = mix(17,28)
dough = mix(29,31)
dough = mix(3,32)
dough = dough.replace("eggs", "")
dough = dough.replace("milk", "")
dough = mix(15,17)
dough = mix(6,19)
dough = mix(2,23)
dough = mix(13,22)
dough = mix(5,18)
dough = mix(2,9)
dough = mix(3,5)
dough = mix(0,2)
dough = dough.replace("flour", "")
dough = dough.replace("sugar", "")
flag = "DDC{" + dough + "}"
print(flag) # DDC{lets_go_unbaking}
````

**Flag**: `DDC{lets_go_unbaking}`
