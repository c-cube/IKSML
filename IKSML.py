#!/usr/bin/python

"""Behold! The mighty IKSML calculus!

For reference, see http://en.wikipedia.org/wiki/SK_calculus .
"""

import xml.dom.minidom

def reduce_term(term):
    """Performs reduction steps until the term
    is in normal form
    """
    return term  # TODO

if __name__ == '__main__':
    if len(sys.argv != 2):
        print "usage: IKSML <file>"
    with open(sys.argv[1]) as f:
        term = xml.dom.minidom.parse(f)
    new_term = reduce_term(term)
    print new_term
