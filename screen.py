import math

class Screen:
    """
        This class creates a text based screen for the basic i/o.
        Attributes:
            h = height
            w = width
            s = list of characters corresponding to the screen.

        Methods:
            setht(n) : set height to n
            setwd(n) : set width to n
            putchar(c, m, n) : put character c at coordinates (m, n)
            putline(l, indent, m) : print string l in line m after indenting
                by indent. If length of l is more than the width the extra
                characters will not be printed. Last column will have a +.
            clear_line(n): Clears line no n.
            clear_page(n): Clears the whole page.
            center_string string line : Centers the string on line line.
            rt_justify_string string line : Right justifies the string in
                line line.
            create_body(string_of_lines, clear_head, indent) : Create the
                body by putting the lines one after another starting from
                line no. clear_head. If the number of lines + clear_head
                exceed h - 3, extra lines are ignored.
            create_footer(list_of_opt_pairs) : Given a list of (option,
                function) pairs, it forms the 2-line footer containing 3
                options in each line. Note you can have at most six options.
            display_page(string_of_lines, list_of_opt_pairs) : Displays the
                page. 
            clear_display_page(string_of_lines, list_of_opt_pairs) : Clears
                the page before displaying the options.
            no_of_pages n = gives the number of pages which a list of length
                n will require in the screen.
            no_of_opts n = gives the number of pages which a list with n
                options will take.
            display_list(list, list_of_obj_pair, page_number)
            clear_display_list(list, list_of_obj_pair, page_number): Clears
                the page before displaying the list
            clear_display_list_w_opt(list, list_of_obj_pair, page_number,
                    opt_page_number): Clears
                the page before displaying the list. This can handle any
                number of options. Each page has the following options:
                n - next page of list elements,
                o - other options.
            display_error(string): Displays the error string.
            display(): Just displays the present page.
    """

    def __init__(cls, ht=12, wd=40) :
        """Initialize the screen"""
        cls.h = ht
        cls.w = wd
        slen = cls.h * cls.w
        cls.s = []
        for _ in range(slen):
            cls.s.append(' ')

    def setht(cls, n):
        """Set height to n"""
        cls.h = n
        slen = cls.h * cls.w
        cls.s = []
        for _ in range(slen):
            cls.s.append(' ')

    def setwd(cls, n):
        """Set height to n"""
        cls.w = n
        slen = cls.h * cls.w
        cls.s = []
        for _ in range(slen):
            cls.s.append(' ')

    def putchar(cls, c, m, n):
        """
        Position character appropriately
        cls.putchar(char, ht_m_from_top, wd_n_from_left)
        """
        if m < 0 or m >= cls.h or n < 0 or n >= cls.w:
            cls.display_error("class Screen: putchar: position out of range.")
        else:
            pos_in_string = m*cls.w + n
            cls.s[pos_in_string] = c

    def putline(cls, l, i, m):
        """
        Print line
        cls.putline(line, indent, at_line_number_from_top)
        """
        lenline = len(l)
        for p in range(min((lenline+i), cls.w) - i):
            cls.putchar(l[p], m, p+i)

    def display(cls):
        """
        display the current screen.
        """
        for i in range(cls.h):
            string_of_line=""
            for j in range(cls.w):
                string_of_line += cls.s[(cls.w) * i + j]
            print string_of_line
        print cls.w*"-"

    def display_error(cls, l):
        """
        Display errors
        """
        cls.putline(" "*cls.w, 0, 2)
        cls.putline(" "*cls.w, 0, 3)
        cls.putline("ERROR", (cls.w / 2 - 3), 3)
        cls.putline(" "*cls.w, 0, 4)
        cls.putline(" "*cls.w, 0, 5)
        cls.putline("!     ", 0, 5)
        cls.putline(l, 3, 5)
        cls.putline(" "*cls.w, 0, 6)
        cls.putline(" "*cls.w, 0, 7)
        cls.display()

    def create_body(cls, str_ln, ch, ind):
        no_lines = len(str_ln)
        eff_no_lines = min(no_lines+ch+2, cls.h) - ch - 2
        for i in range(eff_no_lines):
            cls.putline(str_ln[i], ind, ch+i)

    def clear_line(cls, n):
        cls.putline(' ' * (cls.w), 0, n)

    def clear_page(cls):
        for i in range(cls.h):
            cls.clear_line(i)

    def center_string(cls, st, line):
        lenst = len(st)
        indent_needed = (cls.w - lenst) / 2
        cls.putline(st, indent_needed, line)

    def rt_justify_string(cls, st, line):
        lenst = len(st)
        indent_needed = cls.w - lenst
        cls.putline(st, indent_needed, line)

    def ob_pair_to_str(cls, lop):
        ret_list = []
        for ob in lop:
            ret_list += [ob[0] + ":" + ob[1]]
        return ret_list

    def create_footer(cls, l_ob_pair):
        no_footer_entry = len(l_ob_pair)
        cls.clear_line(cls.h - 2)
        cls.clear_line(cls.h - 1)

        if no_footer_entry == 0:
            cls.center_string("No options", cls.h - 1)
        elif no_footer_entry == 1:
            req_st = l_ob_pair[0][0] + ":" + l_ob_pair[0][1]
            cls.center_string(req_st, cls.h - 1)
        elif no_footer_entry == 2:
            l_of_opt = cls.ob_pair_to_str(l_ob_pair)
            cls.putline(l_of_opt[0], 0, cls.h - 1)
            cls.rt_justify_string(l_of_opt[1], cls.h - 1)
        elif no_footer_entry == 3:
            l_of_opt = cls.ob_pair_to_str(l_ob_pair)
            cls.putline(l_of_opt[0], 0, cls.h - 1)
            cls.center_string(l_of_opt[1], cls.h - 1)
            cls.rt_justify_string(l_of_opt[2], cls.h - 1)
        elif no_footer_entry == 4:
            l_of_opt = cls.ob_pair_to_str(l_ob_pair)
            cls.putline(l_of_opt[0], 0, cls.h - 2)
            cls.center_string(l_of_opt[1], cls.h - 2)
            cls.rt_justify_string(l_of_opt[2], cls.h - 2)
            cls.center_string(l_of_opt[3], cls.h - 1)
        elif no_footer_entry == 5:
            l_of_opt = cls.ob_pair_to_str(l_ob_pair)
            cls.putline(l_of_opt[0], 0, cls.h - 2)
            cls.center_string(l_of_opt[1], cls.h - 2)
            cls.rt_justify_string(l_of_opt[2], cls.h - 2)
            cls.putline(l_of_opt[3], 0, cls.h - 1)
            cls.rt_justify_string(l_of_opt[4], cls.h - 1)
        elif no_footer_entry == 6:
            l_of_opt = cls.ob_pair_to_str(l_ob_pair)
            cls.putline(l_of_opt[0], 0, cls.h - 2)
            cls.center_string(l_of_opt[1], cls.h - 2)
            cls.rt_justify_string(l_of_opt[2], cls.h - 2)
            cls.putline(l_of_opt[3], 0, cls.h - 1)
            cls.center_string(l_of_opt[4], cls.h - 1)
            cls.rt_justify_string(l_of_opt[5], cls.h - 1)
        else:
            cls.display_error("Screen: create_footer: No of footer options can only be at most 6")

    def display_page(cls, str_lines, l_obj_pair):
        cls.create_body(str_lines, 0, 0)
        cls.create_footer(l_obj_pair)
        cls.display()

    def clear_display_page(cls, str_lines, l_obj_pair):
        cls.clear_page()
        cls.display_page(str_lines, l_obj_pair)

    def no_of_pages(cls, n) :
        no_entries_per_page = cls.h - 5
        no_pg = int(math.ceil(float(n) / no_entries_per_page))
        return no_pg

    def display_list_prim(cls, lst, l_obj_pair, page_no):
        l_obj_pair.append(('n', 'Next'))
        if len(l_obj_pair) < 4:
            no_entries_per_page = cls.h - 4
        else :
            no_entries_per_page = cls.h - 5
        no_pages = int(math.ceil(float(len(lst)) / no_entries_per_page))
        # print "no_entries_per_page = {:d}".format(no_entries_per_page)
        # print "no_pages = {:d}".format(no_pages)
        str_ln = []
        if 0 < page_no and page_no <= no_pages:
            first_entry = no_entries_per_page * (page_no - 1)
            last_entry = min(no_entries_per_page * page_no, len(lst))
            # print "last_entry = {:d}".format(last_entry)
            str_ln.append("Page {:d}/{:d}:".format(page_no, no_pages))
            str_ln.append("")
            for i in range(first_entry, last_entry):
                # print i
                str_to_append = "{:3d}. ".format(i+1) + lst[i]
                str_ln.append(str_to_append)
        else :
            cls.display_error("Screen: display_list: page_no out of range: {:d}".format(page_no))
        cls.display_page(str_ln, l_obj_pair)

    def display_list(cls, lst, l_obj_pair, page_no) :
      if len(lst) != 0 :
        cls.display_list_prim(lst, l_obj_pair, page_no)
      else :
        cls.display_error("Screen: display_list: list is empty")

    def clear_display_list(cls, lst, l_obj_pair, page_no):
        cls.clear_page()
        cls.display_list(lst, l_obj_pair, page_no)

    def no_of_opts(cls, n) :
        return int(math.ceil(float(n) / 4))

    def clear_display_list_w_opt(cls, lst, l_obj_pair, page_no, opt_page):
        lopt = len(l_obj_pair)
        llst = len(lst)
        if lopt < 6:
            cls.clear_display_list(lst, l_obj_pair, page_no)
        else :
            no_opt_per_page = 4
            no_opt_pages = int(math.ceil(float(lopt) / no_opt_per_page))
            if 0 < opt_page and opt_page <= no_opt_pages:
                begin_opt = (opt_page - 1) * no_opt_per_page
                end_opt = opt_page * no_opt_per_page
                part_l_obj_pair = l_obj_pair[begin_opt:end_opt]
                part_l_obj_pair.append(('o', 'Other opts'))
                cls.clear_display_list(lst, part_l_obj_pair, page_no)
            else :
                cls.display_error("Screen: clear_display_list_w_opt: opt_page out of range: {:d}".format(opt_page))


if __name__ == '__main__':
    text=["Twinkle twinkle little star", "How I wonder what you are?"]
    scr = Screen(12, 40)
    scr.putline("0123456789"*4, 0, 0)
    for i in range(1,12):
        scr.putline(str(i % 10),0, i)
    scr.display()
    # scr.setht(20)
    # scr.setwd(60)
    scr.create_body(text, 3, 2)
    # scr.create_footer([('o', 'OK'), ('c', 'Cancel'), ('C', 'continue'), ('a', 'Abort'), ('b', 'Break'), ('d', 'Debug'), ('e', 'Elephant')])
    scr.create_footer([('C', 'continue'), ('a', 'Abort'), ('b', 'Break'), ('d', 'Debug'), ('e', 'Elephant')])
    scr.display()
    scr.display_page(text + [" "] + text, [])
    new_list = []
    for i in range(30):
        new_list.append("Item number {:d}".format(i+1))
    scr.display_list(new_list, [('s', 'Something bogus')], 0)
    scr.clear_page()
    scr.display_list(new_list, [('s', 'Something bogus')], 1)
    scr.display_list(new_list, [('s', 'Something bogus')], 2)
    scr.display_list(new_list, [('s', 'Something bogus')], 3)
    scr.display_list(new_list, [('s', 'Something bogus')], 4)
    scr.display_list(new_list, [('s', 'Something bogus')], 5)
    scr.clear_display_list(new_list, [('s', 'Something bogus')], 6)
    long_opt_list = [('a', 'abort'), ('b', 'break'), ('c', 'continue'), ('d', 'debug'), ('e', 'end'), ('f', 'force'), ('g', 'grid'), ('h', 'halt'), ('i', 'input')]
    for i in range(1,7) :
        for j in range(0,4):
            scr.clear_display_list_w_opt(new_list, long_opt_list, i, j)

