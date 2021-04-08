# -*- coding: UTF-8 -*-

# Different flow values
Keys = ["o", "m", "w", "p", "i"]

#  Define product over Keys : o•o=o; o•m=o; o•w=o; etc…
dicProd = {
    "o": {"o": "o", "m": "o", "w": "o", "p": "o", "i": "o"},

    "m": {"o": "o", "m": "m", "w": "w", "p": "p", "i": "i"},

    "w": {"o": "o", "m": "w", "w": "w", "p": "p", "i": "i"},

    "p": {"o": "o", "m": "p", "w": "p", "p": "p", "i": "i"},

    "i": {"o": "o", "m": "i", "w": "i", "p": "i", "i": "i"}
}

#  Define sum over Keys : o+o=o; o+m=m; o+w=w; etc…
dicSum = {
    "o": {"o": "o", "m": "m", "w": "w", "p": "p", "i": "i"},

    "m": {"o": "m", "m": "m", "w": "w", "p": "p", "i": "i"},

    "w": {"o": "w", "m": "w", "w": "w", "p": "p", "i": "i"},

    "p": {"o": "p", "m": "p", "w": "p", "p": "p", "i": "i"},

    "i": {"o": "i", "m": "i", "w": "i", "p": "i", "i": "i"}
}


# Return prod a•b or an error if a or b ∉ Keys
def ProdMWP(a, b):
    if a in Keys and b in Keys:
        return dicProd[a][b]
    else:
        print("ERROR: trying to use", a, "and", b, "as keys for dicProd…")


# Return sum a+b or an error if a or b ∉ Keys
def SumMWP(a, b):
    if a in Keys and b in Keys:
        return dicSum[a][b]
    else:
        print("ERROR: trying to use", a, "and", b, "as keys for dicSum…")


ZeroMWP = "o"

UnitMWP = "m"
