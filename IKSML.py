#!/usr/bin/python

"""Behold! The mighty IKSML calculus!

For reference, see http://en.wikipedia.org/wiki/SK_calculus .
"""

import sys
import xml.dom.minidom

class Exit(Exception):
    """How to exit from a tree..."""
    pass

def mk_apply(term, left, right):
    """Build an 'apply' node"""
    node = term.createElement('apply')
    node.appendChild(left)
    node.appendChild(right)
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

def _one_step(term, node):
    """If node is a suitable place for rewriting, rewrite node and raise Exit.
    """
    if not is_apply(node):
        return 
    elif is_apply(children(node)[0]) and \
         is_K(children(children(node)[0])[0]):
        # (Kx)y -> x
        new_node = children(children(node)[0])[1]
        node.parentNode.replaceChild(new_node, node)
        raise Exit
    elif is_I(children(node)[0]):
        # Ix -> x
        new_node = children(node)[1]
        node.parentNode.replaceChild(new_node, node)
        raise Exit
    elif is_apply(children(node)[0]) and \
         is_apply(children(children(node)[0])[0]) and \
         is_S(children(children(children(node)[0])[0])[0]):
        # pfiu!  ((Sx)y)z -> (xz)(yz)
        x = children(children(children(node)[0])[0])[1]
        y = children(children(node)[0])[1]
        z = children(node)[1]
        new_node = mk_apply(term,
            mk_apply(term, x, z),
            mk_apply(term, y, z.cloneNode(True)))
        node.parentNode.replaceChild(new_node, node)
        raise Exit
    else:
        left = children(node)[0]
        right = children(node)[1]
        # try to rewrite left subtermm
        _one_step(left)
        # try to rewrite right subtermm
        _one_step(right)

def one_step(term):
    """Performs in-place one step of reduction of the given term,
    anywhere in the term. Reductions are:

    (Kx)y -> x
    ((Sx)y)z -> (xz)(yz)
    Ix -> x

    Returns true if the term has been rewritten, false otherwise.
    """
    root = children(term)[0]
    try:
        _one_step(term, root)
        return False
    except Exit:
        return True

def reduce_term(term):
    """Performs reduction steps until the term
    is in normal form
    """
    while one_step(term):
        pass  # loop until not rewriting step

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage: IKSML <file>"
    with open(sys.argv[1]) as f:
        term = xml.dom.minidom.parse(f)
    print term.toxml()
    reduce_term(term)
    print '-' * 70
    print "normal form:"
    print term.toprettyxml(indent='  ')

# vim:shiftwidth=4:tabstop=4:
