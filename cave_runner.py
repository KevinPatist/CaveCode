from cave_parser import *
import operator
import sys
sys.setrecursionlimit(10000)

class RunnerError(Exception):
    """ Class for raising errors that occur while running the code """
    def __init__(self, message: str):
        super().__init__(message)


@dcDecorator
def getOperatorFunction(token_type: TokenTypes) -> Callable:
    """ Return the operator function belonging to the operator type """
    operators = {TokenTypes.ADD: operator.add,
                TokenTypes.SUB: operator.sub,
                TokenTypes.MUL: operator.mul,
                TokenTypes.DIV: operator.floordiv,
                TokenTypes.EQUALS: operator.eq,
                TokenTypes.GREQ: operator.ge,
                TokenTypes.LEEQ: operator.le,
                TokenTypes.LESSER: operator.lt,
                TokenTypes.GREATER: operator.gt,
                TokenTypes.NOTEQUAL: operator.ne,}
    return operators[token_type]


@dcDecorator
def getRunnerValue(action: ValueNode, variable_list: Dict[str, Union[int,str]], function_list: Dict[str, FunctionDefNode]) -> Union[str,int]:
    """ Returns a value from a valuenode """
    value = 0
    if isinstance(action, OperatorNode):
        lhs = getRunnerValue(action.lhs, variable_list, function_list)
        rhs = getRunnerValue(action.rhs, variable_list, function_list)
        if lhs in variable_list.keys():
            lhs = variable_list[lhs]
        if rhs in variable_list.keys():
            rhs = variable_list[rhs]

        value = getOperatorFunction(action.operator)(lhs,rhs)
    
    elif isinstance(action, VariableNode):
        if isinstance(action.value, int):
            value = action.value
        elif action.value not in variable_list.keys():
            raise RunnerError(f"Variable \"{action.value}\" at position: {action.position} is not defined")
        else:
            value = variable_list[action.value]

    elif isinstance(action, FunctionCallNode):
        if action.function_name not in function_list.keys():
            raise RunnerError(f"Function \"{action.function_name}\" called at position: {action.position} is not defined")
        parameters = list(map(lambda val: val.content, action.parameters))
        if len(parameters) != len(function_list[action.function_name].parameters.keys()):
            raise RunnerError(f"Parameters for function \"{action.function_name}\" at position: {action.position} aren't correct")

        parameters = dict(zip(function_list[action.function_name].parameters.keys(), parameters))
        value = runFunction(action.function_name, variable_list, function_list, parameters)

    return value


@dcDecorator
def runIfOrWhile(node: IfOrWhileNode, variable_list: Dict[str, Union[int,str]], function_list: Dict[str, FunctionDefNode]) -> Dict[str,Union[str,int]]:
    """ execute an if statement or while loop """
    if getRunnerValue(node.condition, variable_list, function_list) != 0:
        if len(node.action_list) > 1:
            new_variable_list = reduce(lambda variables, actions: runAction(variables, function_list, actions), node.action_list, variable_list)
        else:
            new_variable_list = runAction(variable_list, function_list, node.action_list[0])
        if node.is_loop:
            return runIfOrWhile(node, new_variable_list, function_list)
        return new_variable_list
    return variable_list


@dcDecorator
def runAction(variable_list: Dict[str, Union[int,str]], function_list: Dict[str, FunctionDefNode], action: List[ActionNode], parameters: Optional[Dict[str,Union[str,int]]]=None) -> Dict[str, Union[int,str]]:
    """ execute and action and return the variable list with updated variables """
    if "return" in variable_list.keys():
        return variable_list

    if isinstance(action, AssignNode):
        new_variable_list = variable_list
        temp_variable_list = {**{action.name: getRunnerValue(action.value, variable_list, function_list)}}
        new_variable_list.update(temp_variable_list)
        
    elif isinstance(action, ReturnNode):
        new_variable_list = deepcopy(variable_list)
        if parameters is not None:
            parameters.update(variable_list)
            new_variable_list["return"] = getRunnerValue(action.return_value, parameters, function_list)
        else:
            new_variable_list["return"] = getRunnerValue(action.return_value, variable_list, function_list)
    else:
        if parameters is not None:
            variable_list.update(parameters)
        new_variable_list = runIfOrWhile(action, variable_list, function_list)
    return new_variable_list


@dcDecorator
def runFunction(function_name: str, variable_list: Dict[str, Union[int,str]], function_list: Dict[str, FunctionDefNode], parameters: Optional[Dict[str, Union[str,int]]]=None) -> Union[str,int]:
    """ run a function if it exists and return it's result """
    if function_name not in function_list.keys():
        raise RunnerError(f"Function \"{function_name}\" is not defined")

    if parameters is not None:
        function_variable_list = reduce(lambda var, action: runAction(var, function_list, action, parameters), function_list[function_name].action_list, variable_list)
    else:
        function_variable_list = reduce(lambda var, action: runAction(var, function_list, action), function_list[function_name].action_list, variable_list)

    if "return" in function_variable_list.keys():
        return function_variable_list["return"]

    raise RunnerError(f"Function \"{function_name}\" does have a return value")


@dcDecorator
def getFunctionName(function: FunctionDefNode) -> Tuple[str, FunctionDefNode]:
    return function.name, function


@dcDecorator
def runner(ast: List[FunctionDefNode]) -> None:
    """ Runs the main function from the given AST and prints the result"""
    function_list = dict(map(getFunctionName, ast))
    print(function_list)
    result = runFunction("main", {}, function_list)
    print(f"Finished running code.\n Result: {result}")
    return None


def main():
    code = open("cave_code.txt", "r")
    code_text = code.readlines()
    code.close()

    print(runner(parser(caveLexer(code_text))))

main()