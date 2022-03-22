from argparse import Action
from inspect import stack
from types import NoneType
from unittest import case
from cave_runner import *

'''
Stappen:
functies neerzetten in dezelfde volgorde als in de code

als variabele nodig voor functie: een load_variable gooien

NIEUW:
Functie zooi aanpassen:
functies moeten aanhouden welke variabelen ze hebben
en welke stack zooi ze daarbinnen hebben

load_variable:
vraagt: 
- register to load to
- variable name
- variable to stack pointer dict

die werkt zo:
zet huidige stack pointer

store_variable:
om de variabele op te slaan op de plek waar die vandaan komt:
- register to save from
- variable name
- variable to stack pointer dict
'''

    
@dcDecorator
def generateMainInit() -> str:
    return_string = "true:\n\t"
    return_string += "ldr R0, #1\n\t"
    return_string += "mov pc, lr\n\n"
    return return_string

@dcDecorator
def getNewVars(action: ActionNode) -> Optional[Tuple[str, int]]:
    if isinstance(action, AssignNode):
        return action.name, action.value
    else:
        return None

@dcDecorator
def convertToNode(var_tup: Tuple[str, int]) -> Tuple[str, CompVarNode]:
    return var_tup[0], CompVarNode(var_tup[0], var_tup[1])

@dcDecorator
def getVariableList(function: FunctionDefNode) -> List[Tuple[str, CompVarNode]]:
    """ This function returns a list of all variables and parameters for the given function 
        It also returns their initial value """
    if len(function.parameters) > 0:
        # var_list = list(reduce(lambda x, y: [(x, function.parameters[x])] + [(y, function.parameters[y])], function.parameters.keys()))
        var_list = list(zip(function.parameters.keys(), function.parameters.values()))
        new_var_list = list(map(getNewVars, function.action_list))
        pre_var_list = var_list + new_var_list
    else:
        new_var_list = list(map(getNewVars, function.action_list))
        pre_var_list = new_var_list
    # total_var_list = list(reduce(lambda x, y: [x] + [y] if y is not None else x, pre_var_list))
    filtered_var_list = list(filter(None, pre_var_list))
    converted_var_list = list(map(convertToNode, filtered_var_list))
    return converted_var_list

@dcDecorator
def addStackPointerToDict(var_list: List[Tuple[str, CompVarNode]], rec_depth: int) -> Optional[Dict[str, CompVarNode]]:
    """ This fucntion updates a Dict to link variables to their reserved stack location. """
    if len(var_list) == 0:
        return None
    pointer_int = (rec_depth + 1) * 4
    pointer_str = '#' + str(pointer_int)
    return_dict = dict()
    if len(var_list) == 1:
        var_list[0][1].setStackPointer(pointer_str)
        return_dict[var_list[0][0]] = var_list[0][1]
    else:
        var_to_assign = var_list.pop()
        var_to_assign[1].setStackPointer(pointer_str)
        return_dict[var_to_assign[0]] = var_to_assign[1]
        return_dict.update(addStackPointerToDict(var_list, rec_depth + 1))
    return return_dict

@dcDecorator
def prepVariableForComp(function_list: List[FunctionDefNode]) -> Tuple[Dict[str, Union[OperatorNode, int]], Dict[str, str]]:
    """ This function returns a dict:
        - var_dict: which contains the variable name and it's value as a CompVarNode 
    """
    variable_list = list(map(getVariableList, function_list.values()))
    flat_var_list = flattenList(variable_list)
    var_dict = addStackPointerToDict(flat_var_list, 0)
    return (var_dict)

@dcDecorator
def loadVar(var_name: str, load_pos: str, var_dict: Dict[str, CompVarNode], stack_offset: Optional[int]) -> str:
    """
    This function loads a variable from the stack into the given register load_pos
    """
    return_string = ""
    return_string += "sub sp, sp, " + var_dict[var_name].pointer + "\n\t"
    return_string += "ldr " + load_pos + ", [sp, #0]\n\t"
    return_string += "add sp, sp, " + var_dict[var_name].pointer + "\n\t"
    return return_string

@dcDecorator
def storeVar(var_name: str, store_pos: str, var_dict: Dict[str, CompVarNode]) -> str:
    """
    This function stores a variable from store_pos to it's assiged stack position
    """
    return_string = ""
    return_string += "sub sp, sp, " + var_dict[var_name].pointer + "\n\t"
    return_string += "str " + store_pos + ", [sp, #0]\n\t"
    return_string += "add sp, sp, " + var_dict[var_name].pointer + "\n\t"
    return return_string

@dcDecorator
def operatorNodeToAsm(node: OperatorNode, var_dict: Dict[str, CompVarNode]) -> str:
    """
    This function translates an OperatorNode into Assembly code
    """
    return_string = ""
    if isinstance(node.lhs.value, str):
        return_string += loadVar(node.lhs.value, "R1", var_dict)
    else:
        return_string += "ldr R1, =" + str(node.lhs.value) + "\n\t"
    if isinstance(node.rhs.value, str):
        return_string += loadVar(node.rhs.value, "R2", var_dict)
    else:
        return_string += "ldr R2, =" + str(node.rhs.value) + "\n\t"
    
    match node.operator:
        case TokenTypes.ADD:
            return_string += "add R0, R1, R2\n\t"
        case TokenTypes.SUB:
            return_string += "sub R0, R1, R2\n\t"
        case TokenTypes.MUL:
            return_string += "mul R0, R1, R2\n\t"
        case TokenTypes.EQUALS:
            return_string += "ldr R3, [pc, #5]\n\t"
            return_string += "mov lr, R3\n\t"
            return_string += "cmp R1, R2\n\t"
            return_string += "beq true\n\t"
            return_string += "ldr R0, #0\n\n"
        case TokenTypes.GREQ:
            return_string += "ldr R3, [pc, #5]\n\t"
            return_string += "mov lr, R3\n\t"
            return_string += "cmp R1, R2\n\t"
            return_string += "bge true\n\t"
            return_string += "ldr R0, #0\n\n"
        case TokenTypes.LEEQ:
            return_string += "ldr R3, [pc, #5]\n\t"
            return_string += "mov lr, R3\n\t"
            return_string += "cmp R1, R2\n\t"
            return_string += "ble true\n\t"
            return_string += "ldr R0, #0\n\n"
        case TokenTypes.LESSER:
            return_string += "ldr R3, [pc, #5]\n\t"
            return_string += "mov lr, R3\n\t"
            return_string += "cmp R1, R2\n\t"
            return_string += "blt true\n\t"
            return_string += "ldr R0, #0\n\n"
        case TokenTypes.GREATER:
            return_string += "ldr R3, [pc, #5]\n\t"
            return_string += "mov lr, R3\n\t"
            return_string += "cmp R1, R2\n\t"
            return_string += "bgt true\n\t"
            return_string += "ldr R0, #0\n\n"
        case TokenTypes.NOTEQUAL:
            return_string += "ldr R3, [pc, #5]\n\t"
            return_string += "mov lr, R3\n\t"
            return_string += "cmp R1, R2\n\t"
            return_string += "bne true\n\t"
            return_string += "ldr R0, 01\n\n"

    return return_string

@dcDecorator
def prepFunctionForComp(function: FunctionDefNode) -> Tuple[str, CompFuncNode]:
    """
    This function turns a FunctionDefNode into Tuple[str, CompFuncNode]
    The CompFuncNode is an alternate FunctionDefNode specialised for use within the compiler
    It's placed in a tuple so it can easily be turned into a dictionary
    """
    # Lijst van alle vars: parameters + vars
    # Stack offset berekenen
    # alle vars plek geven zoals in addStackPointerToDict
    # var_dict naar de nieuwe func node gooien samen met stack offset
    func_var_list = getVariableList(function)
    var_dict = addStackPointerToDict(func_var_list, 0)
    if isinstance(var_dict, NoneType):
        stack_reserved = "#0"
    else:
        stack_reserved = "#" + str(len(var_dict) * 4)
    return (function.name, CompFuncNode(function, var_dict, stack_reserved))

@dcDecorator
def storeParams(function: CompFuncNode, parameter_list: List[str], rec_depth: int) -> Optional[List[str]]:
    return_list = []
    if len(parameter_list) == 0:
        return None
    if len(parameter_list) == 1:
        reg_str = "R" + str(rec_depth)
        return_list.append(storeVar(parameter_list[0], reg_str, function.total_var_dict))
        return return_list
    else:
        param_to_store = parameter_list.pop()
        reg_str = "R" + str(rec_depth)
        return_list.append(storeVar(param_to_store, reg_str, function.total_var_dict))
        return_list.append(storeParams(function, parameter_list, rec_depth + 1))
        flat_list = list(reduce(lambda x, y: [x] + y, return_list))
        return flat_list
        
@dcDecorator
def actionToAsm(action: ActionNode, function: CompFuncNode) -> str:
    return_string = ""
    match action:
        case isinstance(action, AssignNode):
            return_string += assignNodeToAsm(action, function)
        case isinstance(action, IfOrWhileNode):
            return_string += ifOrWhileNodeToAsm(action, function)
        case isinstance(action, ReturnNode):
            return_string += returnNodeToAsm(action, function)

@dcDecorator
def funcToAsm(function: CompFuncNode) -> str:
    # set label
    # set stack offset so stack has reserved space
    # load parameter into it's spot
    # start the code

    # Setting function label
    return_string = function.name + ":\n\t"
    return_string += "add sp, sp, " + function.stack_offset + "\n\t"

    # Storing Parameters/variables
    if not isinstance(function.total_var_dict, NoneType):
        func_param_list = [x for x in function.total_var_dict.keys()]
    else:
        func_param_list = []
    store_param_code_list = storeParams(function, func_param_list, 0)
    return_string += str(reduce(lambda x, y: x + y, store_param_code_list))

    # Creating function code
    function_code_list = list(map(lambda x: actionToAsm(x, function), function.action_list))
    print(function_code_list)
    return return_string



    

@dcDecorator
def generateFullFunctionsCode(func_dict: Dict[str, CompFuncNode]) -> str:
    # call funcToAsm for all nodes in dict
    functions_code_list = list(map(funcToAsm, func_dict.values()))
    print(functions_code_list)

# @dcDecorator
# def initVarToASM(var_dict: Dict[str, CompVarNode], dict_key: str) -> Tuple[str,str]:
#     """ This function creates code to intialise a single variable """
#     return_list = [""]
#     return_list[0] = "\t"
#     if isinstance(var_dict[dict_key].value, OperatorNode):
#         return_list[0] += "sub sp, sp, " + var_dict[dict_key].pointer + "\n\t"
#         return_list[0] += "ldr r0, #0\n\t"
#         return_list[0] += "str r0, [sp, #0]\n\t"
#         return_list[0] += "add sp, sp, " + var_dict[dict_key].pointer + "\n"

#         return_list.append(var_dict[dict_key].name + ":\n\t")
#         var_dict[dict_key].setAssignLabel(var_dict[dict_key].name)
#         return_list[1] += operatorNodeToASM(var_dict[dict_key].value, var_dict)
#         return_list[1] += storeVar(dict_key, "R0", var_dict)
#         return_list[1] += "\n"

#     else:
#         return_list[0] += "sub sp, sp, " + var_dict[dict_key].pointer + "\n\t"
#         return_list[0] += "ldr r0, #" + str(var_dict[dict_key].value) + "\n\t"
#         return_list[0] += "str r0, [sp, #0]\n\t"
#         return_list[0] += "add sp, sp, " + var_dict[dict_key].pointer + "\n"

#     return return_list
    
# @dcDecorator
# def sortVarInit(var_list: List[Union[str, List[str]]]) -> str:
#     """
#     This function takes the raw Variable initialisation code and processes it:
#     The code is first sorted so the stack is filled accordingly.
#     then the assign labels for operator variables is placed.
#     The function puts the whole code segment ito combined_code and returns it.
#     """
#     var_init_list = [x[0] for x in var_list]
#     var_init_list_list = [x[1] for x in var_list if len(x) > 1]
#     combined_code = str(reduce(lambda x, y: x + y, var_init_list))
#     combined_code += "\n"
#     combined_code += str(reduce(lambda x, y: x + y, var_init_list_list))
#     return combined_code

# @dcDecorator
# def initialiseVariables(var_dict: Dict[str, CompVarNode]) -> str:
#     """ This function creates Assembly code to initialise variables """
#     stack_reserved = "#" + str(len(var_dict)*4)
#     var_init_code = "var_init:\n\tadd sp, sp, " + stack_reserved + "\n"
#     # var_init_code_list = list(map(lambda var: initVarToASM(var_dict, var), var_dict.keys()))
#     # sorted_var_init_code = sortVarInit(var_init_code_list)
#     var_init_code += sorted_var_init_code
#     return var_init_code

@dcDecorator
def caveCompiler(ast: List[FunctionDefNode]) -> str:
    func_dict_2 = dict(map(prepFunctionForComp, ast))
    main_init_code = generateMainInit()
    function_code = generateFullFunctionsCode(func_dict_2)
    final_code = main_init_code + function_code
    print(final_code)



def main():
    code = open("cave_code.txt", "r")
    code_text = code.readlines()
    code.close()

    print(caveCompiler(parser(caveLexer(code_text))))

main()