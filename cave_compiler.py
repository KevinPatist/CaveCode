from cave_runner import *

# generateGlobalFuncLabel :: CompFuncNode -> str
@dcDecorator
def generateGlobalFuncLabel(func_to_globalise: CompFuncNode) -> str:
    """
    This function creates the .global label for the given function
    This function is made for use within the generateMainInit function's map
    """
    return_string = ".global " + func_to_globalise.name + "\n"
    return return_string

# generateMainInit :: Dict[str, CompFuncNode] -> str
@dcDecorator
def generateMainInit(func_dict: Dict[str, CompFuncNode]) -> str:
    """
    This function generates some initialising code for the ASM file
    It also creates a "true" label for branching to when a condition is true
    """
    return_string = ".cpu cortex-m0\n.text\n"
    global_func_list = list(map(lambda x: generateGlobalFuncLabel(x), func_dict.values()))
    if len(global_func_list) > 0:
        if len(global_func_list) > 1:
            return_string += str(reduce(lambda x, y: x + y, global_func_list))
        else:
            return_string += global_func_list[0]
        return_string += "\n"
    return_string += "true:\n\t"
    return_string += "mov R0, #1\n\t"
    return_string += "mov pc, lr\n\n"
    return return_string

# getNewVars :: ActionNode -> Optional[Tuple[str, int]]
@dcDecorator
def getNewVars(action: ActionNode) -> Optional[Tuple[str, int]]:
    """
    This function gets new variables made within a function and returns the list containing them
    """
    if isinstance(action, AssignNode):
        return action.name, action.value
    else:
        return None

# convertToNode :: Tuple[str, int] -> Tuple[str, CompVarNode]
@dcDecorator
def convertToNode(var_tup: Tuple[str, int]) -> Tuple[str, CompVarNode]:
    """
    This function converts a tuple to a CompVarNode
    """
    return var_tup[0], CompVarNode(var_tup[0], var_tup[1])

# getNewVariableList :: FunctionDefNode -> List[Tuple[str, CompVarNode]]
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

# addStackPointerToDict :: List[Tuple[str, CompVarNode]] -> int -> Optional[Dict[str, CompVarNode]]
@dcDecorator
def addStackPointerToDict(var_list: List[Tuple[str, CompVarNode]], rec_depth: int) -> Optional[Dict[str, CompVarNode]]:
    """ This fucntion updates a Dict to link variables to their reserved stack location. """
    if len(var_list) == 0:
        return None
    pointer_int = (rec_depth) * 4
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

# prepVariableForComp :: List[FunctionDefNode] -> Tuple[Dict[str, Union[OperatorNode, int]], Dict[str, str]]
@dcDecorator
def prepVariableForComp(function_list: List[FunctionDefNode]) -> Tuple[Dict[str, Union[OperatorNode, int]], Dict[str, str]]:
    """ This function returns a dict:
        - var_dict: which contains the variable name and it's value as a CompVarNode 
    """
    variable_list = list(map(getVariableList, function_list.values()))
    flat_var_list = flattenList(variable_list)
    var_dict = addStackPointerToDict(flat_var_list, 0)
    return (var_dict)

# loadVar :: str -> str -> Dict[str, CompVarNode] -> str
@dcDecorator
def loadVar(var_name: str, load_pos: str, var_dict: Dict[str, CompVarNode]) -> str:
    """
    This function loads a variable from the stack into the given register load_pos
    """
    return_string = "\n\t"
    return_string += "add sp, sp, " + var_dict[var_name].pointer + "\n\t"
    return_string += "ldr " + load_pos + ", [sp, #0]\n\t"
    return_string += "sub sp, sp, " + var_dict[var_name].pointer + "\n\t"
    return return_string

# storeVar :: str -> str -> Dict[str, CompVarNode] -> str
@dcDecorator
def storeVar(var_name: str, store_pos: str, var_dict: Dict[str, CompVarNode]) -> str:
    """
    This function stores a variable from store_pos to it's assiged stack position
    """
    return_string = "\n\t"
    return_string += "add sp, sp, " + var_dict[var_name].pointer + "\n\t"
    return_string += "str " + store_pos + ", [sp, #0]\n\t"
    return_string += "sub sp, sp, " + var_dict[var_name].pointer + "\n\t"
    return return_string

# operatorNodeToAsm :: OperatorNode -> CompFuncNode -> bool=False -> str
@dcDecorator
def operatorNodeToAsm(node: OperatorNode, calling_func: CompFuncNode, in_conditional: bool=False) -> str:
    """
    This function translates an OperatorNode into Assembly code
    """
    return_string = ""
    if isinstance(node.lhs.value, str):
        return_string += loadVar(node.lhs.value, "R1", calling_func.total_var_dict)
    else:
        return_string += "mov R1, #" + str(node.lhs.value) + "\n\t"
    if isinstance(node.rhs.value, str):
        return_string += loadVar(node.rhs.value, "R2", calling_func.total_var_dict)
    else:
        return_string += "mov R2, #" + str(node.rhs.value) + "\n\t"
    
    if in_conditional:
        pointer_increase = 6
    else:
        pointer_increase = 4

    match node.operator:
        case TokenTypes.ADD:
            return_string += "add R0, R1, R2\n\t"
        case TokenTypes.SUB:
            return_string += "sub R0, R1, R2\n\t"
        case TokenTypes.MUL:
            return_string += "mul R0, R1, R2\n\t"
        case TokenTypes.EQUALS:
            return_string += "cmp R1, R2\n\t"
            return_string += "beq true\n\t"
        case TokenTypes.GREQ:
            return_string += "cmp R1, R2\n\t"
            return_string += "bge true\n\t"
        case TokenTypes.LEEQ:
            return_string += "cmp R1, R2\n\t"
            return_string += "ble true\n\t"
        case TokenTypes.LESSER:
            return_string += "cmp R1, R2\n\t"
            return_string += "blt true\n\t"
        case TokenTypes.GREATER:
            return_string += "cmp R1, R2\n\t"
            return_string += "bgt true\n\t"
        case TokenTypes.NOTEQUAL:
            return_string += "cmp R1, R2\n\t"
            return_string += "bne true\n\t"

    return return_string

# prepFunctionForComp :: FunctionDefNode -> Tuple[str, CompFuncNode]
@dcDecorator
def prepFunctionForComp(func_to_prep: FunctionDefNode) -> Tuple[str, CompFuncNode]:
    """
    This function turns a FunctionDefNode into Tuple[str, CompFuncNode]
    The CompFuncNode is an alternate FunctionDefNode specialised for use within the compiler
    It's placed in a tuple so it can easily be turned into a dictionary
    """
    # Lijst van alle vars: parameters + vars
    # Stack offset berekenen
    # alle vars plek geven zoals in addStackPointerToDict
    # var_dict naar de nieuwe func node gooien samen met stack offset
    func_var_list = getVariableList(func_to_prep)
    var_dict = addStackPointerToDict(func_var_list, 0)
    if isinstance(var_dict, NoneType):
        stack_reserved = "#0"
    else:
        stack_reserved = "#" + str(len(var_dict) * 4)
    return (func_to_prep.name, CompFuncNode(func_to_prep, var_dict, stack_reserved))

# storeParams :: CompFuncNode -> List[str] -> int -> Optional[List[str]]
@dcDecorator
def storeParams(function: CompFuncNode, parameter_list: List[str], rec_depth: int) -> Optional[List[str]]:
    """
    This function stores the parameters received by a function in their assigned registers.
    """
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

# giveParams :: CompFuncNode -> List[Type[Node]] -> int -> Optional[str]
@dcDecorator
def giveParams(calling_func: CompFuncNode, parameter_list: List[Type[Node]], rec_depth: int) -> Optional[str]:
    """
    This function places parameters for a function that is about to be called.
    It places the parameters in registers so the function can store them
    """
    return_string = ""
    if len(parameter_list) == 0:
        return None
    if len(parameter_list) == 1:
        reg_str = "R" + str(rec_depth)
        parameter = parameter_list[0]
        if isinstance(parameter.content, int):
            return_string += "mov " + reg_str + ", #" + str(parameter.content) + "\n\t"
        else:
            return_string += loadVar(parameter.content, reg_str, calling_func.total_var_dict)
        return return_string
    else:
        param_to_store = parameter_list.pop()
        reg_str = "R" + str(rec_depth)
        if isinstance(param_to_store.content, int):
            return_string += "mov " + reg_str + ", #" + str(parameter.content) + "\n\t"
        else:
            return_string += loadVar(parameter.content, reg_str, calling_func.total_var_dict)
        return_string += (giveParams(parameter_list, rec_depth + 1))
        return return_string

# convertIfOrWhileToName :: IfOrWhileNode -> CompFuncNode -> str
@dcDecorator
def convertIfOrWhileToName(action: IfOrWhileNode, calling_func: CompFuncNode) -> str:
    """
    This function creates a name base to be used in assembly labels for if statements or while loops
    """
    return_string = ""
    return_string += calling_func.name + "_"
    match action.condition:
        case action.condition if isinstance(action.condition, OperatorNode):
            match action.condition.operator:
                case TokenTypes.EQUALS:
                    operator_string = "eqooga"
                case TokenTypes.GREQ:
                    operator_string = "greqooga"
                case TokenTypes.LEEQ:
                    operator_string = "leeqooga"
                case TokenTypes.LESSER:
                    operator_string = "lesooga"
                case TokenTypes.GREATER:
                    operator_string = "grooga"
                case TokenTypes.NOTEQUAL:
                    operator_string = "neqooga"        
            return_string += str(action.condition.lhs.value) + "_" + operator_string + "_" + str(action.condition.rhs.value)
        case action.condition if isinstance(action.condition, FunctionCallNode):
            return_string += action.condition.name
        case action.condition if isinstance(action.condition, VariableNode):
            return_string += str(action.condition.value)
    return return_string

# assignNodeToAsm :: AssignNode -> CompFuncNode -> str
@dcDecorator
def assignNodeToAsm(action: AssignNode, calling_func: CompFuncNode) -> str:
    """
    This function converts an AssignNode to assembly code.
    It checks what kind of value is assigned to the variable and places that in R0
    Then R0 is stored at the variable's stack position
    """
    return_string = ""
    if isinstance(action.value, OperatorNode):
        return_string += operatorNodeToAsm(action.value, calling_func)
    elif isinstance(action.value, VariableNode):
        return_string += "mov R0, #" + str(action.value.value) + "\n\t"
    # else:
        # Error: assign node krijgt geen correcte waarde geassigned
    return_string += storeVar(action.name, "R0", calling_func.total_var_dict)
    return return_string

# returnNodeToAsm :: ReturnNode -> CompFuncNode -> str
@dcDecorator
def returnNodeToAsm(action: ReturnNode, calling_func: CompFuncNode) -> str:
    """
    This function creates Assembly code from a ReturnNode
    """
    return_string = ""
    match action.return_value:
        case action.return_value if isinstance(action.return_value, FunctionCallNode):
            return_string += giveParams(calling_func, action.return_value.parameters, 0)
            return_string += "bl " + action.return_value.function_name + "\n\t"
        case action.return_value if isinstance(action.return_value, OperatorNode):
            return_string += operatorNodeToAsm(action.return_value, calling_func)
        case action.return_value if isinstance(action.return_value, VariableNode):
            if isinstance(action.return_value.value, int):
                return_string += "mov R0, #" + str(action.return_value.value) + "\n\t"
            else:
                return_string += loadVar(action.return_value.value, "R0", calling_func.total_var_dict)
    return_string += "b " + calling_func.name + "_end"
    return return_string 

# ifOrWhileNodeToAsm :: IfOrWhileNode -> CompFuncNode -> str
@dcDecorator
def ifOrWhileNodeToAsm(action: IfOrWhileNode, calling_func: CompFuncNode) -> str:
    """
    This function converts an IfOrWhileNode to assembly code
    """
    #============================================
    # Coditional check en branchen naar eind if false
    #============================================
    return_string = ""
    label_name_base = convertIfOrWhileToName(action, calling_func)
    if action.is_loop:
        return_string += "\n" + label_name_base + "_condition:\n\t"
    else:
        return_string += "\t"
    
    return_string += operatorNodeToAsm(action.condition, calling_func, True)
    if action.condition.operator == TokenTypes.NOTEQUAL:
        return_string += "cmp R0, #0\n\t"
    else:
        return_string += "cmp R0, #1\n\t"
    return_string += "bne " + label_name_base + "_end\n\t"
    
    # actions omzetten in lijst met ASM code
    action_code_list = list(map(lambda x: actionToAsm(x, calling_func), action.action_list))

    # actions lijst omzetten tot code en bij retrun string toevoegen
    actions_code = str(reduce(lambda x, y: x + y, action_code_list))
    return_string += actions_code

    # als node een while loop is het actie blok eindigen met branch naar condition label
    if action.is_loop:
        return_string += "b " + label_name_base + "_condition\n\t"
    
    # end label maken
    return_string += "\n" + label_name_base + "_end:\n\t"

    return return_string

# actionToAsm :: ActionNode -> CompFuncNode -> str
@dcDecorator
def actionToAsm(action: ActionNode, calling_func: CompFuncNode) -> str:
    """
    This function turns an ActionNode to assembly code
    """
    return_string = ""
    match action:
        case action if isinstance(action, AssignNode):
            return_string += assignNodeToAsm(action, calling_func)
        case action if isinstance(action, IfOrWhileNode):
            return_string += ifOrWhileNodeToAsm(action, calling_func)
        case action if isinstance(action, ReturnNode):
            return_string += returnNodeToAsm(action, calling_func)

    return return_string

# funcToAsm :: CompFuncNode -> str
@dcDecorator
def funcToAsm(func_to_convert: CompFuncNode) -> str:
    """
    This functionn turns a function into assembly code
    """
    # set label
    # set stack offset so stack has reserved space
    # load parameter into it's spot
    # start the code

    # Setting function label
    return_string = func_to_convert.name + ":\n\t"
    return_string += "push {lr}\n\t"
    return_string += "sub sp, sp, " + func_to_convert.stack_offset + "\n\t"

    # Storing Parameters/variables
    if not isinstance(func_to_convert.total_var_dict, NoneType):
        func_param_list = [x for x in func_to_convert.total_var_dict.keys()]
    else:
        func_param_list = []
    store_param_code_list = storeParams(func_to_convert, func_param_list, 0)
    if not isinstance(store_param_code_list, NoneType):
        if len(store_param_code_list) > 1:
            return_string += str(reduce(lambda x, y: x + y, store_param_code_list))
        else:
            return_string += store_param_code_list[0]
        return_string += "\n"

    # Creating function code
    function_code_list = list(map(lambda x: actionToAsm(x, func_to_convert), func_to_convert.action_list))
    function_code_string = str(reduce(lambda x, y: x + y, function_code_list))
    return_string += function_code_string

    # creating end label with function end
    return_string += "\n" + func_to_convert.name + "_end:\n\t"
    # hier stond add i.p.v. sub
    return_string += "add sp, sp, " + func_to_convert.stack_offset + "\n\t"
    return_string += "pop {pc}\n\n"
    return return_string

# generateFullFunctionsCode :: Dict[str, CompFuncNode] -> str
@dcDecorator
def generateFullFunctionsCode(func_dict: Dict[str, CompFuncNode]) -> str:
    """
    This function turns a dict containing function nodes into assembly code
    """
    # call funcToAsm for all nodes in dict
    functions_code_list = list(map(funcToAsm, func_dict.values()))
    full_functions_code = str(reduce(lambda x, y: x + y, functions_code_list))
    return full_functions_code

# caveCompiler :: List[FunctionDefNode] -> str
@dcDecorator
def caveCompiler(ast: List[FunctionDefNode]) -> str:
    func_dict_2 = dict(map(prepFunctionForComp, ast))
    main_init_code = generateMainInit(func_dict_2)
    function_code = generateFullFunctionsCode(func_dict_2)
    final_code = main_init_code + function_code
    # print(final_code)
    code_file = open('cave_code.asm', 'w')
    code_file.write(final_code)
    code_file.close()
    return final_code



def main():
    code = open("cave_code.txt", "r")
    code_text = code.readlines()
    code.close()

    caveCompiler(parser(caveLexer(code_text)))

main()