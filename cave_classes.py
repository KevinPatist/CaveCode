import re
import io
import os

from enum import Enum
from typing import Tuple, TypeVar, List, Type

class TokenTypes(Enum):
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
    ID       = "[a-zA-Z]\w*"
    NUMBER   = "[0-9]+"

class Token:
    def __init__(self, token_type: Type[Enum], value: str, position: Tuple[int,int]):
        """Creates a Token object which contains the tokens type, its value and its position within the code"""
        self.token_type = token_type
        self.content = value
        self.position = position

    def __str__(self) -> str:
        """Returns a string object describing the token"""
        return self.__repr__()

    def __repr__(self) -> str:
        return f"(value: \"{self.value}\", type

