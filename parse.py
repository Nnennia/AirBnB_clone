#!/usr/bin/python3
import re
from shlex import split
def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [x.strip(",") for x in split(arg)]
        else:
            lexer = split(arg[:brackets.span([0])])
            retl = [x.strip(",") for x in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span([0])])
        retl = [x.strip(",") for x in lexer]
        retl.append(curly_braces.group())
        return retl
