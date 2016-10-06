from tree import *
from screen import *
from mlist import *

import os.path

def safe_float(str) :
    try :
        f = float(str)
    except ValueError :
        print "accounts: safe_float: invalid number. Substituting 0."
        f = 0.0
    return f

def decode_item_price(str) :
    lenstr = len(str)
    # We set the error condition.
    item = "DIPError"
    price = 0.0
    if lenstr == 0 :
        print "decode_item_price: empty string."
        item = "DIPError"
        price = 0.0
    else :
        dollarpos = []
        for i in range(lenstr) :
            if str[i] == '$' :
                dollarpos.append(i)
        if len(dollarpos) == 0 :
            print "accounts: decode_item_price: not an account entry."
        elif len(dollarpos) > 1 :
            print "accounts: decode_item_price: multiple $ signs."
        else :
            i = dollarpos[0]
            item = str[:i]
            price = safe_float(str[(i+1):])
    return (item, price)

def encode_item_price(iptup) :
    encstr = "{:s}${:012.4f}".format(iptup[0], 0.0)
    if abs(iptup[1]) > 10**7 :
        print "accounts: encode_item_price: price is too high for this code."
    else :
        encstr = "{:s}${:012.4f}".format(iptup[0], iptup[1])
    return encstr

class AccList(MList) :
    """
        This is an extension of the mlist. It will mostly use mlist
        functions. But some functions have to be modified to take care of
        the price entry.
    """
