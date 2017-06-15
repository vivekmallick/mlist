from tree import *
from screen import *
from mlist import *

import os.path
import time

def path_to_seq_nodes(str) :
    seqnodes = []
    nodename = ""
    pos = 0
    if len(str) > 0 :
        while pos < len(str) :
            if str[pos] == '.' :
                seqnodes.append(nodename)
                nodename = ""
            else :
                nodename += str[pos]
            pos += 1
        if len(nodename) > 0 :
            seqnodes.append(nodename)
    else :
        print "accounts: cannot proccess empty paths."
    return seqnodes

def sep_last_word(str):
    l = len(str)
    b = l
    stay_in_loop = True
    while b >= 1 and stay_in_loop :
        if str[b - 1] == ' ' :
            lw = str[b:]
            rt = str[:b-1]
            stay_in_loop = False
        else :
            b -= 1
    if b == 0 :
        lw = str
        rt = ""
    return (rt, lw)


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
    price_zero = encode_item_name("{:012.4f}".format(0.0))
    encstr = "{:s}${:s}".format(encode_item_name(iptup[0]), price_zero)
    if abs(iptup[1]) > 10**7 :
        print "accounts: encode_item_price: price is too high for this code."
    else :
        str_itm = encode_item_name(iptup[0])
        str_p = encode_item_name("{:012.4f}".format(iptup[1]))
        encstr = "{:s}${:s}".format(str_itm, str_p)
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
            (price, succ) = safe_float(decode_item_name(str[(i+1):]))
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
        retstr = "({:9.2f}) {:s}".format(p, decode_item_name(it))
    return retstr

def updated_node(node, lst_nodes) :
    (item, price) = decode_item_price(node)
    possible_node = None
    for nd in lst_nodes :
        (itnd, itp) = decode_item_price(nd)
        if item == itnd :
            possible_node = nd
    return possible_node

def name_in_list(name, lst_nodes) :
    is_name_in_list = False
    for node in lst_nodes :
        (it, pr) = decode_item_price(node)
        if name == decode_item_name(it) :
            is_name_in_list = True
    return is_name_in_list

class AccList(MList) :
    """
        This is an extension of the mlist. It will mostly use mlist
        functions. But some functions have to be modified to take care of
        the price entry.
    """

    def __init__(cls, afile="/mnt/m_internal_storage/com.hipipal.qpyplus/scripts/acc.txt") :
        cls.t = Tree('acc$0#p0')
        cls.s = Screen()
        cls.afile = afile
        if os.path.isfile(afile) :
            cls.t.load(afile)

    
    def error(cls, err_str) :
        err = "accounts: " + err_str
        cls.s.display_error(err)
        raw_input("press enter to continue")

    def info(cls, inf_str) :
        inf = "account: " + inf_str
        cls.s.display_error(inf)
        time.sleep(1)

    def save(cls) :
        cls.t.write_out(cls.afile)

    def display_and_ask(cls, scheme, total_str, lstpage=1, optpage=1) :
        list_of_prices = []
        for items in cls.t.list() :
            list_of_prices.append(output_item_price(items))
        cls.s.clear_display_list_w_opt(list_of_prices, cls.options(scheme), lstpage, optpage)
        curritemprice = decode_item_price(find_name(cls.t.currnode()))
        curritem = decode_item_name(curritemprice[0])
        currprice = "{:9.2f}".format(curritemprice[1])
        cls.s.rt_justify_string(currprice, 0)
        cls.s.center_string(curritem, 0)
        cls.s.display()
        a = raw_input('acc> ')
        return a

    def jump_to_last_page(cls) :
        last_page = cls.s.no_of_pages(len(cls.t.list()))
        return last_page

    def add_entry_base(cls, itm, str_prc) :
        (prc, succ_conv) = safe_float(str_prc)
        if name_in_list(itm, cls.t.list()) :
            cls.error("add_entry: item is already listed. Nothing added")
        else :
            if succ_conv :
                entry = encode_item_price((itm, prc))
            else :
                cls.error("add_entry: price should be a floating number.")
                entry = encode_item_price((itm, 0.0))
            cls.t.add(entry)

    def add_entry(cls) :
        itm = raw_input(' Item> ')
        str_prc = raw_input('Price> ')
        cls.add_entry_base(itm, str_prc)

    def edit_item_name(cls) :
        ent_no_str = raw_input('Item number> ')
        ent_no = safe_int(ent_no_str)
        if ent_no != -1 :
            if 1 <= ent_no and ent_no <= len(cls.t.list()) :
                ent_string = cls.t.list()[ent_no - 1]
                (enc_itm_name, price) = decode_item_price(ent_string)
                itm_name = decode_item_name(enc_itm_name)
                print "Replace: {:s}".format(itm_name)
                rep_str = raw_input("     by> ")
                enc_rep_str = encode_item_price((rep_str, price))
                cls.t.edit(ent_string, enc_rep_str)
            else :
                cls.error("edit_item_name: number out of range")
        else :
            cls.error("edit_item_name: please enter a number")

    def edit_item_price(cls) :
        ent_no_str = raw_input('Item number> ')
        ent_no = safe_int(ent_no_str)
        if ent_no != -1 :
            if 1 <= ent_no and ent_no <= len(cls.t.list()) :
                ent_string = cls.t.list()[ent_no - 1]
                (enc_itm_name, old_price) = decode_item_price(ent_string)
                itm_name = decode_item_name(enc_itm_name)
                print "Replace: {:7.2f}".format(old_price)
                rep_str = raw_input("     by> ")
                (price, succ) = safe_float(rep_str)
                if succ :
                    enc_rep_str = encode_item_price((itm_name, price))
                    cls.t.edit(ent_string, enc_rep_str)
                else :
                    cls.error("edit_item_price: price is a float.")
            else :
                cls.error("edit_item_price: number out of range")
        else :
            cls.error("edit_item_price: please enter a number")

    def descend_base (cls, desc_to) :
        if 1 <= desc_to and desc_to <= len(cls.t.list()):
            cls.t.jump_to(cls.t.list()[desc_to - 1])
        else :
            cls.error("descend: {:d} is out of range.".format(desc_to))

    def descend(cls) :
        desc_to_str = raw_input('Descend to item> ')
        desc_to = safe_int(desc_to_str)
        if desc_to != -1 :
            cls.descend_base(desc_to)
        else :
            cls.error("descend: {:s} is not a number.".format(desc_to_str))

    def default_act(cls, reply) :
        if reply != '' :
            no_if_so = safe_int(reply)
            if no_if_so == -1 :
                # The entry is not a number. Treat it as a new item.
                # First try to extract price.
                (rest, lw) = sep_last_word(reply)
                (pr, suc) = safe_float(lw)
                if suc :
                    cls.info("default: adding " + rest + " with price " + lw)
                    cls.add_entry_base(rest, lw)
                else :
                    cls.info("default: adding " + reply + ". Input price.")
                    str_prc = raw_input('Price> ')
                    cls.add_entry_base(reply, str_prc)
            else :
                cls.info("default: descending to " + reply)
                cls.descend_base(no_if_so)

    def compute_sums(cls) :
        save_curr_node = cls.t.currnode()

        # Get to root
        cls.t.root()
        level = 0
        itno = []
        itno.append(0)
        sum = []
        sum.append(0)
        stayInWhile = True
        while stayInWhile :
            print sum[:level+1]
            if itno[level] == len(cls.t.list()) :
                if level > 0 :
                    cls.t.go_up()
                    level -= 1
                    parent_item = cls.t.list()[itno[level]]
                    (par_itm_name_code, par_itm_pr) = decode_item_price(parent_item)
                    par_itm_name = decode_item_name(par_itm_name_code)
                    updated_entry = encode_item_price((par_itm_name, sum[level + 1]))
                    cls.t.edit(parent_item, updated_entry)
                    itno[level] += 1
                    sum[level] += sum[level + 1]
                    # print "Levelling down ", level, sum[level+1]
                else :
                    total_expenditure = sum[level]
                    stayInWhile = False
            else :
                item = cls.t.list()[itno[level]]
                if cls.t.isleaf(item) :
                    price = decode_item_price(item)[1]
                    sum[level] += price
                    itno[level] += 1
                else :
                    level += 1
                    if level < len(itno) :
                        itno[level] = 0
                    else :
                        itno.append(0)

                    if level < len(sum) :
                        sum[level] = 0
                    else :
                        sum.append(0)

                    cls.t.jump_to(item)
            # print item, level, itno[level], sum[level]

        cls.t.root()
        seqnodes = path_to_seq_nodes(save_curr_node)
        # print seqnodes
        for node in seqnodes[1:] :
            update_node = updated_node(node, cls.t.list())
            if update_node == None :
                cls.error("Some bug in software.")
            else :
                cls.t.jump_to(update_node)

        return total_expenditure

        
    def interact_acc(cls):
        scheme = 'accounts'
        tot_exp_str = "{:12.2f}".format(cls.compute_sums())
        reply = cls.display_and_ask(scheme, tot_exp_str)
        opt = 1
        page = 1
        # In the following the call to jump_to_last_page is not very smooth.
        # Find a better way to handle it in the corresponding functions.
        # May be all functions return the page number.
        while reply != 'q' :
            if reply == 'a' :
                cls.add_entry()
                page = cls.jump_to_last_page()
            elif reply == 'd' :
                cls.delete_entry()
            elif reply == 's' :
                cls.descend()
                page = cls.jump_to_last_page()
            elif reply == 'u' :
                cls.t.go_up()
                page = cls.jump_to_last_page()
            elif reply == 'm' :
                cls.error("interact: mark not implemented")
            elif reply == 'o' :
                no_opt_pg = cls.s.no_of_opts(len(cls.options(scheme)))
                # print opt,
                if no_opt_pg > 0 :
                    opt = (opt % no_opt_pg) + 1
                else :
                    cls.error("interact: no options")
                # print no_opt_pg, opt
            elif reply == 'n' :
                no_pages = cls.s.no_of_pages(len(cls.t.list()))
                if no_pages > 0 :
                    page = (page % no_pages) + 1
                else :
                    cls.error("interact: no entries")
            elif reply == 'e' :
                cls.edit_item_name()
            elif reply == 'p' :
                cls.edit_item_price()
            elif reply == 'r' :
                tot_exp_str = "{:12.2f}".format(cls.compute_sums())
            else :
                cls.default_act(reply)
                page = cls.jump_to_last_page()
            cls.save()
            # tot_exp_str = "{:12.2f}".format(cls.compute_sums())
            reply = cls.display_and_ask(scheme, tot_exp_str, page, opt)
        print "Good bye"


if __name__ == '__main__' :
    a = AccList()
    a.interact_acc()
