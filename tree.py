def find_base(s):
    l = len(s)
    # find the last .
    i = l-1
    while i >=0 and s[i] != '.':
        i -= 1
    if i != -1:
        base = s[:i]
    else:
        base = s
    return base

def find_name(s):
    l = len(s)
    # find the last .
    i = l-1
    while i >=0 and s[i] != '.':
        i -= 1
    if i != -1:
        base = s[(i+1):]
    else:
        base = s
    return base

def extract_node_from_tail(t):
    l = len(t)
    i = 0
    while i < l and t[i] != '.':
        i += 1
    if i == l:
        nd = t
    else:
        nd = t[:i]
    return nd

def set_like_list(l):
    k = []
    for o in l:
        if not (o in k):
            k.append(o)
    return k

def is_substring(sstr, lstr):
    l = len(sstr)
    return (sstr == lstr[:l])

def replace(longstr, originit, newinit):
    """Replace initial part of longstr given by originit by newinit"""
    if is_substring(originit, longstr):
        l = len(originit)
        retval = newinit + longstr[l:]
    else :
        retval = None
    return retval

def strip_newline(s):
    l = len(s)
    if s[l-1] == '\n':
        retval = s[:l-1]
    else :
        retval = s
    return retval

class Tree:
    """
        Class to implement a tree. The tree is stored in a list.
        Attributes
            tree = list containing the tree.
            tree_root = name of the root. Default 'r'
            curr_node = current node.
        Methods
            currnode = Show the current node
            jump_to node = descend to node
            go_up = go up one level
            root = go back to the root
            list = list all entries in the present node.
            add element = add element to current node.
            add element = adds element to current node as a leaf
            add_to_node node element = adds element to node as a leaf
            change_root rootname = change root to rootname. This is
                discouraged.
            isleaf name = returns True if it is a leaf (no subbranches) else
                False
            is_represented node: if node, the full node, is represented in
                the tree as a subpath of some node.
            rmleaf name = remove curr_node.name. Will do nothing if the node
                is not a leaf.
            rec_rm_node node = recursively delete a node and all its
                subbranches.
            edit node newname = rename the node to newname.
    """
    def __init__(cls, custom_root='r'):
        """Initialise the tree class"""
        cls.tree_root = custom_root
        cls.tree = [cls.tree_root]
        cls.curr_node = cls.tree_root

    def error(cls, s):
        print "Tree: " + s

    def currnode(cls):
        return cls.curr_node

    def add(cls, elt):
        cls.tree.append(cls.curr_node + "." + elt)

    def add_to_node(cls, node, elt):
        cls.tree.append(node + "." + elt)

    def root(cls):
        cls.curr_node = cls.tree_root

    def is_subpath(cls, spath, lpath):
        return is_substring(spath + ".", lpath + ".")

    def jump_to(cls, node):
        new_node = cls.curr_node + "." + node
        # is new_node a valid path
        is_new_node_path = False
        for path in cls.tree:
            if cls.is_subpath(new_node, path):
                is_new_node_path = True
        if is_new_node_path:
            cls.curr_node = new_node
        else:
            cls.error("jump_to: No such node as: " + new_node)

    def go_up(cls):
        cn = cls.curr_node
        if cn == cls.tree_root:
            cls.error("go_up: Already at root")
            base = cn
        else:
            base = find_base(cn)
        cls.curr_node = base

    def list(cls):
        l = []
        n = len(cls.curr_node)
        for e in cls.tree:
            if e[:(n+1)] == cls.curr_node + ".":
                l.append(e[(n+1):])
        k = []
        for e in l:
            k.append(extract_node_from_tail(e))
        return set_like_list(k)

    def fulltree_simple(cls):
        for n in cls.tree:
            print n

    def change_root(cls, newroot):
        cls.error("change_root: Root is being changed to: " + newroot)
        cls.tree_root = newroot
        cls.root()

    def isleaf(cls, node):
        if node in cls.list():
            cls.jump_to(node)
            if len(cls.list()) == 0:
                retval = True
            else:
                retval = False
            cls.go_up()
        else :
            cls.error("isleaf: no such node as " + node)
            retval = False
        return retval

    def is_represented(cls, node):
        isrep = False
        for p in cls.tree:
            isrep = isrep or cls.is_subpath(node, p)
        return isrep

    def rmleaf(cls, node):
        fullnode = cls.curr_node + "." + node
        if fullnode in cls.tree:
            if cls.isleaf(node):
                fnindex = cls.tree.index(fullnode)
                del cls.tree[fnindex]
                if not cls.is_represented(cls.curr_node):
                    cls.tree.append(cls.curr_node)
            else :
                cls.error("rmleaf: not a leaf: " + fullnode)
        else:
            error_line1 = "rmleaf: there is no leaf as: "
            error_line2 = fullnode
            cls.error(error_line1 + error_line2)

    def rec_rm_node(cls, node, debug = False):
        if cls.isleaf(node):
            cls.rmleaf(node)
        elif node in cls.list():
            level = 0
            rmls = [(level, node)]
            base = cls.currnode()
            while len(rmls) > 0:
                l, n = rmls.pop()
                if debug:
                    print "rec_rm_node debug: (l, n): ", l, n
                while l < level:
                    cls.go_up()
                    level -= 1
                if cls.isleaf(n):
                    cls.rmleaf(n)
                else :
                    rmls.append((level, n))
                    cls.jump_to(n)
                    level += 1
                    for m in cls.list():
                        rmls.append((level, m))
                if debug :
                    print "rec_rm_node debug: rmls: ", rmls
        else :
            cls.error("rec_rm_node: No such node as: " + node)

    def edit(cls, node, replacement):
        orig_str = cls.curr_node + "." + node
        new_str = cls.curr_node + "." + replacement
        if cls.is_represented(orig_str):
            for i in range(len(cls.tree)):
                if is_substring(orig_str, cls.tree[i]):
                    repval = replace(cls.tree[i], orig_str, new_str)
                    if repval == None :
                        cls.error("edit: " + orig_str + " is not a part of the node.")
                    else :
                        cls.tree[i] = repval
        else :
            cls.error("edit: no such node as: " + cls.currnode() + "." + node)

    def find_root(cls, str):
        if '.' in str :
            i = str.index('.')
            rt = str[:i]
        else:
            rt = str
        return rt

    def load(cls, filename):
        with open(filename, 'r') as lf :
            cls.tree = []
            for line in lf :
                cls.tree.append(strip_newline(line))
        if len(cls.tree) > 0 :
            # print cls.tree[0]
            cls.tree_root = cls.find_root(cls.tree[0])
            cls.curr_node = cls.tree_root

    def write_out(cls, filename):
        with open(filename, 'w') as wf:
            for line in cls.tree :
                wf.write(line)
                wf.write('\n')

if __name__ == "__main__":
    t = Tree()
    t.add("ab")
    t.add("bc")
    t.add("cd")
    print "First tree dump"
    t.fulltree_simple()
    print "-"*20
    t.add_to_node("ab", "xy")
    print "Second tree dump"
    t.fulltree_simple()
    print "-"*20
    print
    t.jump_to("ab")
    print "Node after  first jump_to: " + t.currnode()
    t.jump_to("cd")
    print "Node after second jump_to: " + t.currnode()
    t.go_up()
    print "Node after  first go_up: " + t.currnode()
    t.go_up()
    print "Node after second go_up: " + t.currnode()

    t.jump_to("ab")
    t.add("xy")
    t.add("wz")
    t.go_up()

    print "List at " + t.currnode() + ": ",
    print t.list()
    t.jump_to("ab")
    print "List at " + t.currnode() + ": ",
    print t.list()

    print
    print "An almost final tree dump"
    t.fulltree_simple()
    print "-"*20

    t.change_root('ab')
    t.go_up()
    t.go_up()
    print "Current node: " + t.currnode() + "."
    t.root()
    print "List at " + t.currnode() + ":",
    print t.list()
    t.add('test')
    print "List at " + t.currnode() + ":",
    print t.list()
    print
    print "Final tree dump before remove"
    t.fulltree_simple()

    print "Removing"
    t.rmleaf('xy')
    print "List at " + t.currnode() + ":",
    print t.list()
    t.rmleaf('test1')
    print "Final tree dump:"
    t.fulltree_simple()

    t.tree = t.tree + ['r.ab.1', 'r.ab.2', 'r.ab.3', \
            'r.ab.1.11.111.1111.11111', 'r.ab.1.12.121.1211', \
            'r.ab.2.22.222.2222.22222']
    print "Checking rmleaf and rec_rm_node"
    t.fulltree_simple()
    print "Saving tree for future recovery"
    t.write_out('treetest.txt')
    print "-"*20
    t.change_root('r')
    t.jump_to('ab')
    t.jump_to('2')
    t.jump_to('22')
    t.jump_to('222')
    t.rmleaf('2222')
    t.jump_to('2222')
    t.rmleaf('22222')
    t.fulltree_simple()
    print
    print "and for rec_rm_node"
    t.root()
    t.rec_rm_node('ab')
    t.fulltree_simple()
    print "-" * 20
    t.root()
    t.edit('bc', 'newname')
    print t.list()
    print "-" * 20 + "\n Reversing deletes:\n" + "-" * 20
    t.load('treetest.txt')
    t.fulltree_simple()
