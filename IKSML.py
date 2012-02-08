#!/usr/bin/python

"""Behold! The mighty IKSML calculus!

For reference, see http://en.wikipedia.org/wiki/SK_calculus .
"""

import sys
import xml.dom.minidom

def mk_apply(left, right):
    """Build an 'apply' node"""
    node = xml.dom.minidom.Node()
    node.appendChild(left)
    node.appendChild(right)
    node.tagName = 'apply'
    return node

def children(node):
    """Get the 'interesting' children of the node, excluding
    useless text and comments"""
    return [child for child in node.childNodes if \
            child.nodeType == node.ELEMENT_NODE and \
            child.tagName.strip() in ('fun', 'apply', 'S', 'K', 'I')]

def is_apply(node):
    return node.nodeType == node.ELEMENT_NODE \
       and node.tagName.strip() == 'apply'

def is_K(node):
    return node.nodeType == node.ELEMENT_NODE \
       and node.tagName.strip() == 'fun' \
       and children(node)[0].tagName.strip() == 'K'

def is_S(node):
    return node.nodeType == node.ELEMENT_NODE \
       and node.tagName.strip() == 'fun' \
       and children(node)[0].tagName.strip() == 'S'


def is_I(node):
    return node.nodeType == node.ELEMENT_NODE \
       and node.tagName.strip() == 'fun' \
       and children(node)[0].nodeType == node.TEXT_NODE \
       and children(node)[0].tagName.strip() == 'I'

def _one_step(node):
    """If node is a suitable place for rewriting,
    rewrite node and return true. Else, recurse in subterms.
    """
    if not is_apply(node):
        return node
    elif is_apply(children(node)[0]) and \
       is_K(children(children(node)[0])[0]):
        # (Kx)y -> x
        return children(children(node)[0])[1]
    elif is_I(children(node)[0]):
        # Ix -> x
        return children(node)[1]
    elif is_apply(children(node)[0]) and \
         is_apply(children(children(node)[0])[0]) and \
         is_S(children(children(children(node)[0])[0])[0]):
        # pfiu!  ((Sx)y)z -> (xz)(yz)
        x = children(children(children(node)[0])[0])[0]
        y = children(children(node)[0])[0]
        z = children(node)[1]
        return mk_apply(mk_apply(x, z), mk_apply(y, z.cloneNode(True)))
    elif is_apply(node):
        left = children(node)[0]
        right = children(node)[1]
        # try to rewrite left subtermm
        new_left = _one_step(left)
        if new_left != left:
            return mk_apply(new_left, right)
        # try to rewrite right subtermm
        new_right = _one_step(right)
        if new_right != right:
            return mk_apply(left, new_right)
        # no rewriting
        return node
    else:
        return node

def one_step(term):
    """Performs in-place one step of reduction of the given term,
    anywhere in the term. Reductions are:

    (Kx)y -> x
    ((Sx)y)z -> (xz)(yz)
    Ix -> x

    Returns true if the term has been rewritten, false otherwise.
    """
    root = children(term)[0]
    new_root = _one_step(root)
    if new_root != root:
        print "-" * 70
        print "rewriting step:"
        root.writexml(sys.stdout)
        print "to"
        new_root.writexml(sys.stdout)
        print

        term.replaceChild(new_root, root)
        return True
    else:
        return False

def reduce_term(term):
    """Performs reduction steps until the term
    is in normal form
    """
    while True:
        if not one_step(term):
            return

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage: IKSML <file>"
    with open(sys.argv[1]) as f:
        term = xml.dom.minidom.parse(f)
    reduce_term(term)
    term.writexml(sys.stdout)
    print

# vim:shiftwidth=4:tabstop=4:
