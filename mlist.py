from tree import *
from screen import *

import os.path

def concat_list_str(ls):
    return '\n'.join(ls)

def safe_int(str):
    try :
        a = int(str)
    except ValueError :
        a = -1
    return a

class MList:
    """
        This is the main class which implements mlist. It includes a tree
        object t and a screen object s. It has methods to interact and
        accordingly store things in t.
        
        Objects :
            t = the tree object to store the lists
            s = screen to print.
            mfile = file in which the data is stored
            
        Methods :
            save = Saves the file in mfile.
            options = returns options given the scheme.
    """

    def __init__(cls, mfile="mlist.txt"):
        cls.t = Tree('mlist')
        cls.s = Screen()
        cls.mfile = mfile
        if os.path.isfile(mfile):
            cls.t.load(mfile)

    def __repr__(cls):
        return concat_list_str(cls.t.tree)

    def __str__(cls):
        return concat_list_str(cls.t.list())

    def error(cls, err_str):
        err = "mlist: " + err_str
        cls.s.display_error(err)
        raw_input('press enter to continue.')

    def save(cls):
        cls.t.write_out(cls.mfile)

    def options(cls, scheme='default'):
        optList = []
        if scheme == 'default' :
            optList.append(('a', 'add'))
            optList.append(('d', 'delete'))
            optList.append(('e', 'edit'))
            optList.append(('s', 'sublist'))
            optList.append(('u', 'go up'))
            optList.append(('m', 'mark'))
            optList.append(('q', 'quit'))
        elif scheme == 'accounts' :
            optList.append(('a', 'add'))
            optList.append(('d', 'delete'))
            optList.append(('e', 'edit'))
            optList.append(('p', 'price'))
            optList.append(('s', 'sublist'))
            optList.append(('u', 'go up'))
            optList.append(('m', 'mark'))
            optList.append(('r', 'refresh'))
            optList.append(('q', 'quit'))
        else :
            cls.error("options: scheme does not exist: " + scheme)
        return optList

    def display_and_ask(cls, scheme, lstpage=1, optpage=1):
        cls.s.clear_display_list_w_opt(cls.t.list(), cls.options(scheme), lstpage, optpage)
        cls.s.rt_justify_string(cls.t.currnode(), 0)
        cls.s.display()
        a = raw_input('mlist> ')
        return a

    def add_entry(cls):
        new_entry = raw_input('Item> ')
        cls.t.add(new_entry)

    def delete_entry(cls):
        entry_no = raw_input('Entry number> ')
        int_entry = safe_int(entry_no)
        if int_entry != -1 :
            if 1 <= int_entry and int_entry <= len(cls.t.list()):
                cls.t.rmleaf(cls.t.list()[int_entry - 1])
            else :
                cls.error("delete_entry: Number out of range.")
        else :
            cls.error('delete_entry: invalid input')

    def descend(cls):
        desc_to_str = raw_input('Descend to item> ')
        desc_to = safe_int(desc_to_str)
        if desc_to != -1 :
            if 1 <= desc_to and desc_to <= len(cls.t.list()):
                cls.t.jump_to(cls.t.list()[desc_to - 1])
            else :
                cls.error("descend: {:d} is out of range.".format(desc_to))
        else :
            cls.error("descend: {:s} is not a number.".format(desc_to_str))


    def edit_entry(cls) :
        entry_no_str = raw_input('Edit item number> ')
        entry_no = safe_int(entry_no_str)
        if entry_no != -1 :
            if 1 <= entry_no and entry_no <= len(cls.t.list()) :
                entry_string = cls.t.list()[entry_no - 1]
                rep_prompt = "Repace {:s} by > ".format(entry_string)
                alt_string = raw_input(rep_prompt)
                cls.t.edit(entry_string, alt_string)
            else :
                cls.error('edit_entry: entry number out of range')
        else :
            cls.error('edit_entry: item number should be a number.')

    def default_act(cls, reply):
        cls.error("Unknown command: {:s}.".format(reply))
        # raw_input()

    def interact_todo(cls):
        scheme = 'default'
        reply = cls.display_and_ask(scheme)
        opt = 1
        page = 1
        while reply != 'q' :
            if reply == 'a' :
                cls.add_entry()
            elif reply == 'd' :
                cls.delete_entry()
            elif reply == 's' :
                cls.descend()
            elif reply == 'u' :
                cls.t.go_up()
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
                cls.edit_entry()
            else :
                cls.default_act(reply)
            cls.save()
            reply = cls.display_and_ask(scheme, page, opt)
        print "Good bye"

if __name__ == '__main__':
    m = MList()
    # reply = m.display_and_ask('default')
    # print "Reply is {:s}.".format(reply)
    m.interact_todo()
