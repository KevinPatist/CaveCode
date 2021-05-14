from cave_lexer import *

class ParseError(Exception):
    def __init__(self, wanted: str, gotten: Optional[Token]):
        self.wanted = wanted
        if gotten:
            self.gotten_value = gotten.content
            self.gotten_type = gotten.token_type.name
            self.position = gotten.position
            super().__init__(f"Message: {self.wanted}, but got {self.gotten_value}. "
                             f"Which is a(n) {self.gotten_type}, at position {self.position}.")
        
        else:
            super().__init__(f"Expected {self.wanted}, but got nothing.")


@dcDecorator
def isFirst(token_list: List[Token], token_type: List[TokenTypes]) -> bool:
    """ Checks if the first item in token_list has a type in token_type
        Returns True is the first item in token_list is of a given token type """
    if len(token_list) != 0:
        return token_list[0].token_type in token_type
    raise ParseError(f"isFirst wanted tokens of types: [{token_type}]", token_list[0] if len(token_list) != 0 else None)


@dcDecorator
def getToken(token_list: List[Token], wanted_types: List[TokenTypes]) -> Tuple[Token, List[Token]]:
    """ if the first token in the list is of the wanted TokenType this function returns the first token as well as the remaining list 
        If the first token isn't of the wanted type, and error is raised """
    if isFirst(token_list, wanted_types):
        return token_list[0], token_list[1:]
    else:
        raise ParseError(f"getToken wanted TokenTypes: {wanted_types}", token_list[0])


@dcDecorator
def getParameters(token_list: List[Token]) -> Tuple[Dict[str, int], List[Token]]:
    if isFirst(token_list, [TokenTypes.ID]):
        parameters = {token_list.pop(0).content: 0}
    elif isFirst(token_list, [TokenTypes.CLOSEPAR]):
        return {}, token_list[1:]

    if isFirst(token_list, [TokenTypes.SEP]):
        other_parameters, token_list1 = getParameters(token_list[1:])
        return {**parameters, **other_parameters}, token_list1
    elif isFirst(token_list, [TokenTypes.CLOSEPAR]):
        return parameters, token_list[1:]
    else:
        raise ParseError(f"getParameters wanted Token of types: [ID, SEP or CLOSEPAR]", token_list[0] if len(token_list) != 0 else None)
        

@dcDecorator
def getCallParameters(token_list: List[Token]) -> Tuple[List[Union[int, str, float]], List[Token]]:
    if isFirst(token_list, [TokenTypes.CLOSEPAR]):
        return [], token_list[1:]

    elif isFirst(token_list, [TokenTypes.SEP]):
        return getCallParameters(token_list[1:])

    elif isFirst(token_list, [TokenTypes.ID, TokenTypes.NUMBER]):
        parameters = [token_list[0]]
        token_list1 = token_list[1:]
        other_parameters, token_list1 = getCallParameters(token_list[1:])
        parameters += other_parameters
        
        return parameters, token_list1
    
    else:
        raise ParseError(f"getCallParameters wanted Token of types: [CLOSEPAR, SEP, ID or NUMBER]", token_list[0] if len(token_list) != 0 else None)


@dcDecorator      
def getParseValue(token_list: List[Token], first: bool=False, operator: Optional[Token]=None, lhs: Optional[ValueNode]=None) -> Tuple[Node, List[Token]]:
    
    if isFirst(token_list, [TokenTypes.ID]):
        if isFirst(token_list[1:], [TokenTypes.OPENPAR]):
            name = token_list[0]
            if isFirst(token_list[2:], [TokenTypes.CLOSEPAR]):
                value = FunctionCallNode(name, [])
                token_list1 = token_list[3:]

            else:
                parameters, token_list1 = getCallParameters(token_list[2:])
                value = FunctionCallNode(name, parameters)

        else:
            value = VariableNode(token_list[0])
            token_list1 = token_list[1:]

    elif isFirst(token_list, [TokenTypes.NUMBER]):
        value = VariableNode(token_list[0])
        token_list1 = token_list[1:]

    else:
        raise ParseError(f"getParseValue wanted Token of types: [ID, NUMBER]", token_list[0] if len(token_list) != 0 else None)


    maths = [TokenTypes.ADD, TokenTypes.SUB, TokenTypes.MUL, TokenTypes.DIV]
    compare = [TokenTypes.GREATER, TokenTypes.LESSER, TokenTypes.EQUALS, TokenTypes.GREQ, TokenTypes.LEEQ]

    if isFirst(token_list1,  maths + compare):
        if operator is not None and lhs is not None:
            rhs, token_list2 = getParseValue(token_list1[1:], False, token_list1[0], value)
            value2 = OperatorNode(lhs, token_list1[0], rhs)

        else:
            value2, token_list2 = getParseValue(token_list1[1:], False, token_list1[0], value)
            value3 = OperatorNode(value, token_list1[0], value2)
            value2 = value3

        value = value2
        token_list1 = token_list2

    if isFirst(token_list1, [TokenTypes.END, TokenTypes.CLOSEPAR]):
        if first:
            return value, token_list1[1:]
        else:
            return value, token_list1
    
    else:
        raise ParseError(f"getParseValue", token_list[0] if len(token_list) != 0 else None)


@dcDecorator
def flattenActionList(action_list: List[List[ActionNode]]) -> List[ActionNode]:
    flat_list = reduce(lambda x, y: [x] + y, action_list)
    return flat_list


@dcDecorator
def getActions(token_list: List[Token]) -> Tuple[Optional[Union[None,List[ActionNode]]],List[Token]]:
    """ Function to parse actions inside of a function """
    if isFirst(token_list, [TokenTypes.CLOSEBR]):
        return None,token_list

    action_list = []
    if isFirst(token_list, [TokenTypes.ID]):
        if isFirst(token_list[1:], [TokenTypes.ASSIGN]):
            variable, token_list1 = getParseValue(token_list[2:], True)
            action_list.append(AssignNode(token_list[0], variable))

        return_actions, return_tokens = getActions(token_list1)
        if return_actions is not None:
            action_list.append(return_actions)
            action_list = flattenActionList(action_list)
        return action_list, return_tokens

    elif isFirst(token_list, [TokenTypes.IF, TokenTypes.WHILE]):
        is_loop = TokenTypes.WHILE == token_list[0].token_type

        _, token_list1 = getToken(token_list[1:], [TokenTypes.OPENPAR])
        condition, token_list2 = getParseValue(token_list1)
        _, token_list3 = getToken(token_list2, [TokenTypes.CLOSEPAR])
        _, token_list4 = getToken(token_list3, [TokenTypes.OPENBR])
        actions, token_list5 = getActions(token_list4)
        _, token_list6 = getToken(token_list5, [TokenTypes.CLOSEBR])
        action_list.append(IfOrWhileNode(condition, actions, is_loop))

        return_actions, return_tokens = getActions(token_list6)
        if return_actions is not None:
            action_list.append(return_actions)
            action_list = flattenActionList(action_list)
        return action_list, return_tokens

    elif isFirst(token_list, [TokenTypes.RETURN]):
        value, token_list1 = getParseValue(token_list[1:], True)
        action_list.append(ReturnNode(value))
        return_actions, return_tokens = getActions(token_list1)
        if return_actions is not None:
            action_list.append(return_actions)
            action_list = flattenActionList(action_list)
        return action_list, return_tokens
        
    else:
        raise ParseError(f"getActions wanted Token of types: [ID, RETURN, IF, WHILE, CLOSEBR]", token_list[0] if len(token_list) != 0 else None)


@dcDecorator
def parser(token_list: List[Token]) -> List[FunctionDefNode]:
    """ This function keeps parsing functions until there are no more tokens or an error occurs """
    _, token_list1 = getToken(token_list, [TokenTypes.DEF])
    func_name, token_list2 = getToken(token_list1, [TokenTypes.ID])
    _, token_list3 = getToken(token_list2, [TokenTypes.OPENPAR])
    parameters, token_list4 = getParameters(token_list3)
    _, token_list5 = getToken(token_list4, [TokenTypes.OPENBR])
    actions, token_list6 = getActions(token_list5)
    _, token_list7 = getToken(token_list6, [TokenTypes.CLOSEBR])

    function_definition = [FunctionDefNode(func_name, parameters, actions)]
    if len(token_list7) != 0:
        return function_definition + parser(token_list7)
    else:
        return function_definition