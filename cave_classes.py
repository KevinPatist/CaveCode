import re
import io
import os

from typing import list, Tuple, TypeVar

class TokenTypes(enum):
    ADD      = "plooga"
    SUB      = "mooga"
    MUL      = "kooga"
    DIV      = "dooga"
    ASSIGN   = "isooga"
    IF       = "ifooga"
    ELSE     = "elooga"
    WHILE    = "whooga"
    EQUALS   = "eqooga"
    GREQ     = "greqooga"
    LEEQ     = "leeqooga"
    LESSER   = "lesooga"
    GREATER  = "grooga"
    NOTEQUAL = "neqooga"
    END      = "booga"
    SEP      = "komooga"
    OPENPAR  = "hoooga"
    CLOSEPAR = "hsooga"
    OPENBR   = "broooga"
    CLOSEBR  = "brsooga"
    DEF      = "fdooga"
    RETURN   = "retooga"

