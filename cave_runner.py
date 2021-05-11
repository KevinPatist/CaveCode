from cave_parser import *
import operator

class RunnerError(Exception):
    """ Class for raising errors that occur while running the code """
    def __init__(self, message: str):
        super().__init__(message)


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


def getRunnerValue(action: ValueNode, variable_list: Dict[str, Union[int,str]], function_list: Dict[str, FunctionDefNode]) -> Union[str,int]:
    """ Returns a value from a valuenode """
    value = 0
    if isinstance(action, OperatorNode):
        lhs = getRunnerValue(action.lhs, variable_list, function_list)
        rhs = getRunnerValue(action.rhs, variable_list, function_list)
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
        value = runFunction(action.function_name, parameters, function_list)

    return value


def runIfOrWhile(node: IfOrWhileNode, variable_list: Dict[str, Union[int,str]], function_list: Dict[str, FunctionDefNode]) -> Dict[str,Union[str,int]]:
    """ execute an if statement or while loop """
    if getRunnerValue(node.condition, variable_list, function_list) != 0:
        new_variable_list = reduce(lambda var, action: runAction(var, function_list, action), node.action_list, variable_list)
        if node.is_loop:
            return runIfOrWhile(node, new_variable_list, function_list)
        return new_variable_list
    return variable_list


def runAction(variable_list: Dict[str, Union[int,str]], function_list: Dict[str, FunctionDefNode], action: [ActionNode]) -> Dict[str, Union[int,str]]:
    """ execute and action and return the variable list with updated variables """
    if "return" in variable_list.keys():
        return variable_list

    if isinstance(action, AssignNode):
        new_variable_list = {**variable_list, **{action.name: getRunnerValue(action.value, variable_list, function_list)}}
    elif isinstance(action, ReturnNode):
        new_variable_list = variable_list
        new_variable_list["return"] = getRunnerValue(action.return_value, variable_list, function_list)
    else:
        new_variable_list = runIfOrWhile(action, variable_list, function_list)
    return new_variable_list


def runFunction(function_name: str, variable_list: Dict[str, Union[int,str]], function_list: Dict[str, FunctionDefNode], parameters: Optional[List[Union[str,int]]]=None) -> Union[str,int]:
    """ run a function if it exists and return it's result """
    if function_name not in function_list.keys():
        raise RunnerError(f"Function \"{function_name}\" is not defined")

    new_variable_list = reduce(lambda var, action: runAction(var, function_list, action), function_list[function_name].action_list, variable_list)

    if "return" in new_variable_list.keys():
        return new_variable_list["return"]

    raise RunnerError(f"Function \"{function_name}\" does have a return value")


def getFunctionName(function: FunctionDefNode) -> Tuple[str, FunctionDefNode]:
    return function.name, function


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