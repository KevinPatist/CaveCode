import re
import io
import os

from enum import Enum
from typing import Tuple, TypeVar, List, Type, Callable, Union, Optional, Dict
from functools import reduce
from copy import deepcopy


def dcDecorator(function):
    def inside(*args):
        return function(*list(map(lambda element: deepcopy(element), args)))
    return inside

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
        self.content = value if not value.isdigit() else int(value)
        self.position = position

    def __str__(self) -> str:
        """Returns a string object describing the token"""
        return self.__repr__()

    def __repr__(self) -> str:
        """ Returns a string containing the token's content, type and position """
        return f"(value: \"{self.content}\", type: {self.token_type}, position: {self.position}\n"


class Node:
    """ Base Node """
    def __init__(self, pos: Tuple[int,int]):
        self.position = pos

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """ Returns a string containing the empty node's position """
        return f"Empty Base Node, position: {self.position}"


class ValueNode(Node):
    """ Node that saves values """
    def __init__(self, pos: Tuple[int,int]):
        Node.__init__(self, pos)

    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        """ Returns a string containing the empty value node's position """
        return f"Empty Value Node, position: {self.position}"


class VariableNode(ValueNode):
    """ Node used to store integers and strings """
    def __init__(self, token: Token):
        ValueNode.__init__(self, token.position)
        self.value = token.content

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """ Returns a string containing the node's value """
        return f"{self.value}"


class FunctionCallNode(ValueNode):
    """ Node used to store function calls """
    def __init__(self, token: Token, parameters: List[Type[Node]]):
        ValueNode.__init__(self, token.position)
        self.function_name = token.content
        self.parameters = parameters

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """ Returns a string containing the functionCallNode's function name and parameters """
        return f"function name: {self.function_name}, parameters: {self.parameters}"


class OperatorNode(ValueNode):
    """ Node used to store operators with rhs and lhs """
    def __init__(self, lhs: ValueNode, operator_token: Token, rhs: ValueNode):
        ValueNode.__init__(self, operator_token.position)
        self.lhs = lhs
        self.operator = operator_token.token_type
        self.rhs = rhs

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """ Returns a string containing the empty OperatorNode's lhs, operator type and rhs """
        return f"lhs: {self.lhs.__str__()}, operator: {self.operator}, rhs: {self.rhs.__str__()}"


class ActionNode(Node):
    """ Nodes used for storing actions """
    def __init__(self, pos: Tuple[int,int]):
        Node.__init__(self, pos)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """ Returns a string containing the empty node's position """
        return f"Empty Action Node, position: {self.position}"


class AssignNode(ActionNode):
    """ Node used for an assigned variable """
    def __init__(self, variable: Token, value: ValueNode):
        ActionNode.__init__(self, variable.position)
        self.name = variable.content
        self.value = value

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """ Returns a string containing the AssignNode's name and value """
        return f"variable name: {self.name}, value: {self.value}"


class IfOrWhileNode(ActionNode):
    """ A node used for storing if statements or while loops """
    def __init__(self, condition_token: ValueNode, action_list: List[ActionNode], is_loop: bool):
        ActionNode.__init__(self, condition_token.position)
        self.condition = condition_token
        self.action_list = action_list
        self.is_loop = is_loop

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """ Returns a string containing the IfOrWhileNode's condition, actionlist and the is_loop bool """
        return f"condition: {self.condition}, actions: {self.action_list}, loop: {self.is_loop}"


class ReturnNode(ActionNode):
    """ A node used to return stuff """
    def __init__(self, value: ValueNode):
        ActionNode.__init__(self, value.position)
        self.return_value = value

    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        """ Returns a string containing the ReturnNode's return value """
        return f"return value: {self.return_value}"
        

class FunctionDefNode(Node):
    """ Node used to store functions with parameters and instructions """
    def __init__(self, token: Token, parameters: Dict[str, int], action_list: List[ActionNode]):
        Node.__init__(self, token.position)
        self.name = token.content
        self.parameters = parameters
        self.action_list = action_list

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """ Returns a string containing the FunctionDefNode's name, parameterlist and actionlist """
        return f"Function {self.name}, with parameters: {self.parameters} and actions: {self.action_list}"