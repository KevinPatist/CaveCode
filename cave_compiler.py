from argparse import Action
from ctypes import pointer
from venv import create
from cave_runner import *

'''
Stappen:
Aantal variabelen tellen (inclusief parameters)

variabelen tellen:
parameters tellen en daarna in action list naar AssignNodes zoeken

variabelen assignen aan een stack pointer waarde (met intervals van 4, dus #0, #4, #8 enzo)
(^^ dit moet in een dict)

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
def getVariableList(function: FunctionDefNode) -> list[Tuple[str, CompVarNode]]:
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
    pointer_int = rec_depth * 4
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
    """ This function returns two dicts:
        - var_dict: which contains teh variable name and it's value 
        - var_par_to_stack: which contains the variable name and it's assigned stack location 
    """
    variable_list = list(map(getVariableList, function_list.values()))
    flat_var_list = flattenList(variable_list)
    # vars_stack_size = 4 * len(flat_var_list)
    var_dict = addStackPointerToDict(flat_var_list, 0)
    return (var_dict)

@dcDecorator
def initVarToASM(var_dict: Dict[str, CompVarNode], dict_key: str) -> str:
    """ This function creates code to intialise a single variable """
    


@dcDecorator
def initialiseVariables(var_dict: Dict[str, CompVarNode]) -> str:
    """ This function creates Assembly code to initialise variables """
    var_init_code = ""
    var_init_code_list = list(map(lambda var: initVarToASM(var_dict, var), var_dict.keys()))
    return var_init_code
    

@dcDecorator
def caveCompiler(ast: list[FunctionDefNode]) -> str:
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