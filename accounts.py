from tree import *
from screen import *
from mlist import *

import os.path

def safe_float(str) :
    success = True
    try :
        f = float(str)
    except ValueError :
        print "accounts: safe_float: invalid number. Substituting 0."
        f = 0.0
        success = False
    return (f, success)

def encode_item_name(itnm) :
    lenitnm = len(itnm)
    encitnm = ""
    for c in itnm :
        # print c, encitnm, itnm
        if c == '$' :
            encitnm = encitnm + "#d"
        elif c == "." :
            encitnm = encitnm + "#p"
        elif c == "#" :
            encitnm = encitnm + "##"
        elif c == " " :
            encitnm = encitnm + "#s"
        else :
            encitnm = encitnm + c
    return encitnm

def decode_item_name(encitnm) :
    lei = len(encitnm)
    itnm = ""
    interpret = False
    for i in range(lei) :
        c = encitnm[i]
        if interpret :
            if c == 'd' :
                itnm = itnm + "$"
            elif c == 'p' :
                itnm = itnm + '.'
            elif c == 's' :
                itnm = itnm + ' '
            elif c == '#' :
                itnm = itnm + '#'
            else :
                print "accounts: decode_item_name: ignoring # command: {:s}.".format(c)
                itnm = itnm + c
            interpret = False
        else :
            if c == '#' :
                if i == lei - 1 :
                    print "accounts: decode_item_name: {:s} is not complete.".format(encitnm)
                else :
                    interpret = True
            else :
                itnm = itnm + c
    return itnm

def encode_item_price(iptup) :
    encstr = "{:s}${:012.4f}".format(iptup[0], 0.0)
    if abs(iptup[1]) > 10**7 :
        print "accounts: encode_item_price: price is too high for this code."
    else :
        encstr = "{:s}${:012.4f}".format(encode_item_name(iptup[0]), iptup[1])
    return encstr

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
            (price, succ) = safe_float(str[(i+1):])
            if not succ :
                print "accounts: decode_item_price: price `{:s}' is absurd.".format(str[(i+1):])
    return (item, price)

def output_item_price(str) :
    (it, p) = decode_item_price(str)
    error = False
    if it == "DIPError" :
        error = True
        retstr = "Error decoding line"
    else :
        retstr = "{:12s} ({:9.4f})".format(decode_item_name(it), p)
    return retstr

class AccList(MList) :
    """
        This is an extension of the mlist. It will mostly use mlist
        functions. But some functions have to be modified to take care of
        the price entry.
    """

    def __init__(cls, afile="acc.txt") :
        cls.t = Tree('acc')
        cls.s = Screen()
        cls.afile = afile
        if os.path.isfile(afile) :
            cls.t.load(afile)

    # def display_and_ask(cls, scheme, lstpage=1, optpage=1) :

