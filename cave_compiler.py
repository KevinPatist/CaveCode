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
    print(converted_var_list)
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
    print(var_dict)
    return (var_dict)

@dcDecorator
def loadVar(var_name: str, var_dict: Dict[str, CompVarNode]) -> str:
    return_string = ""
    if isinstance(var_dict[var_name].value, OperatorNode):
        return_string += ""


@dcDecorator
def operatorNodeToASM(node: OperatorNode, var_dict: Dict[str, CompVarNode]) -> str:
    return_string = ""
    if isinstance(node.lhs, str):
        return_string += loadVar(node.lhs, var_dict)

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
        return_list[1] += "sub sp, sp, " + var_dict[dict_key].pointer + "\n\t"
        return_list[1] += "str r0, [sp, #0]\n\t"
        return_list[1] += "add sp, sp, " + var_dict[dict_key].pointer + "\n\n"
    else:
        return_list[0] += "sub sp, sp, " + var_dict[dict_key].pointer + "\n\t"
        return_list[0] += "ldr r0, #" + str(var_dict[dict_key].value) + "\n\t"
        return_list[0] += "str r0, [sp, #0]\n\t"
        return_list[0] += "add sp, sp, " + var_dict[dict_key].pointer + "\n"
    # ToDo:
    # steps:
    # Assign labels for operator variables
    # code for said variables
    # Initialisation of the other variables:
    # placing them on the stack according to their pointer values
    # returning stack pointer to original value
    # return_string += "\n"
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
    var_init_code = initialiseVariables(variable_dict)
    print(var_init_code)



def main():
    code = open("cave_code.txt", "r")
    code_text = code.readlines()
    code.close()

    print(caveCompiler(parser(caveLexer(code_text))))

main()