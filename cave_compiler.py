from unittest import case
from cave_runner import *

'''
Stappen:
functies neerzetten in dezelfde volgorde als in de code

als variabele nodig voor functie: een load_variable gooien

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
    return_string += "ldr R0, #0\n\t"
    return_string += "mov pc, lr\n\t"

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
def addStackPointerToDict(var_list: List[Tuple[str, CompVarNode]], rec_depth: int) -> Dict[str, CompVarNode]:
    """ This fucntion updates a Dict to link variables to their reserved stack location. """
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
def loadVar(var_name: str, load_pos: str, var_dict: Dict[str, CompVarNode]) -> str:
    """
    This function loads a variable from the stack into the given register load_pos
    """
    return_string = "sub sp, sp, " + var_dict[var_name].pointer + "\n\t"
    return_string += "ldr " + load_pos + ", [sp, #0]\n\t"
    return_string += "add sp, sp, " + var_dict[var_name].pointer + "\n\t"
    return return_string

@dcDecorator
def storeVar(var_name: str, store_pos: str, var_dict: Dict[str, CompVarNode]) -> str:
    """
    This function stores a variable from store_pos to it's assiged stack position
    """
    return_string = "sub sp, sp, " + var_dict[var_name].pointer + "\n\t"
    return_string += "str " + store_pos + ", [sp, #0]\n\t"
    return_string += "add sp, sp, " + var_dict[var_name].pointer + "\n\t"
    return return_string

@dcDecorator
def operatorNodeToASM(node: OperatorNode, var_dict: Dict[str, CompVarNode]) -> str:
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
    
    # match node.operator:
    #     case TokenTypes.ADD:
    #         return_string += "add R0, R1, R2"
    #     case TokenTypes.SUB:
    #         return_string += "sub R0, R1, R2"
    #     case TokenTypes.MUL:
    #         return_string += "mul R0, R1, R2"
    #     case TokenTypes.EQUALS:
    #         return_string += "cmp R1, R2\n\t"
    #         return_string += "mov lr, pc\n\t"
    #         return_string += "beq true\n\t"
    #     case TokenTypes.GREQ:
    #         return_string += "cmp R1, R2\n\t"
    #         return_string += "mov lr, pc\n\t"
    #         return_string += "bge true\n\t"
    #     case TokenTypes.LEEQ:
    #         return_string += "cmp R1, R2\n\t"
    #         return_string += "mov lr, pc\n\t"
    #         return_string += "ble true\n\t"
    #     case TokenTypes.LESSER:
    #         return_string += "cmp R1, R2\n\t"
    #         return_string += "mov lr, pc\n\t"
    #         return_string += "blt true\n\t"
    #     case TokenTypes.GREATER:
    #         return_string += "cmp R1, R2\n\t"
    #         return_string += "mov lr, pc\n\t"
    #         return_string += "bgt true\n\t"
    #     case TokenTypes.NOTEQUAL:
    #         return_string += "cmp R1, R2\n\t"
    #         return_string += "mov lr, pc\n\t"
    #         return_string += "bne true\n\t"


    return return_string


@dcDecorator
def initVarToASM(var_dict: Dict[str, CompVarNode], dict_key: str) -> Tuple[str,str]:
    """ This function creates code to intialise a single variable """
    return_list = [""]
    return_list[0] = "\t"
    if isinstance(var_dict[dict_key].value, OperatorNode):
        return_list[0] += "sub sp, sp, " + var_dict[dict_key].pointer + "\n\t"
        return_list[0] += "ldr r0, #0\n\t"
        return_list[0] += "str r0, [sp, #0]\n\t"
        return_list[0] += "add sp, sp, " + var_dict[dict_key].pointer + "\n"

        return_list.append(var_dict[dict_key].name + ":\n\t")
        var_dict[dict_key].setAssignLabel(var_dict[dict_key].name)
        return_list[1] += operatorNodeToASM(var_dict[dict_key].value, var_dict)
        return_list[1] += "\n"
        # return_list[1] += "sub sp, sp, " + var_dict[dict_key].pointer + "\n\t"
        # return_list[1] += "str r0, [sp, #0]\n\t"
        # return_list[1] += "add sp, sp, " + var_dict[dict_key].pointer + "\n\n"
    else:
        return_list[0] += "sub sp, sp, " + var_dict[dict_key].pointer + "\n\t"
        return_list[0] += "ldr r0, #" + str(var_dict[dict_key].value) + "\n\t"
        return_list[0] += "str r0, [sp, #0]\n\t"
        return_list[0] += "add sp, sp, " + var_dict[dict_key].pointer + "\n"

    return return_list
    
@dcDecorator
def sortVarInit(var_list: List[Union[str, List[str]]]) -> str:
    """
    This function takes the raw Variable initialisation code and processes it:
    The code is first sorted so the stack is filled accordingly.
    then the assign labels for operator variables is placed.
    The function puts the whole code segment ito combined_code and returns it.
    """
    var_init_list = [x[0] for x in var_list]
    var_init_list_list = [x[1] for x in var_list if len(x) > 1]
    combined_code = str(reduce(lambda x, y: x + y, var_init_list))
    combined_code += "\n"
    combined_code += str(reduce(lambda x, y: x + y, var_init_list_list))
    return combined_code

@dcDecorator
def initialiseVariables(var_dict: Dict[str, CompVarNode]) -> str:
    """ This function creates Assembly code to initialise variables """
    stack_reserved = "#" + str(len(var_dict)*4)
    var_init_code = "var_init:\n\tadd sp, sp, " + stack_reserved + "\n"
    var_init_code_list = list(map(lambda var: initVarToASM(var_dict, var), var_dict.keys()))
    sorted_var_init_code = sortVarInit(var_init_code_list)
    var_init_code += sorted_var_init_code
    return var_init_code

@dcDecorator
def caveCompiler(ast: List[FunctionDefNode]) -> str:
    function_list = dict(map(getFunctionName, ast))
    variable_dict = prepVariableForComp(function_list)
    main_init_code = generateMainInit()
    var_init_code = initialiseVariables(variable_dict)
    print(var_init_code)



def main():
    code = open("cave_code.txt", "r")
    code_text = code.readlines()
    code.close()

    print(caveCompiler(parser(caveLexer(code_text))))

main()