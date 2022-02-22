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
def getVariableList(function: FunctionDefNode) -> list[Tuple[str, Union[OperatorNode, int]]]:
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
    print(filtered_var_list)
    return filtered_var_list

@dcDecorator
def createStackPointerDict(var_list: List[Tuple[str, Union[OperatorNode, int]]], rec_depth: int) -> Dict[str, str]:
    pointer_int = rec_depth * 4
    pointer_str = '#' + str(pointer_int)
    return_dict = dict()
    if len(var_list) == 1:
        return_dict[var_list[0][0]] = pointer_str
    else:
        var_to_assign = var_list.pop()
        return_dict[var_to_assign[0]] = pointer_str
        return_dict.update(createStackPointerDict(var_list, rec_depth + 1))
    return return_dict

@dcDecorator
def prepVariableForComp(function_list: List[FunctionDefNode]) -> Tuple[Dict[str, Union[OperatorNode, int]], Dict[str, str]]:
    variable_list = list(map(getVariableList, function_list.values()))
    flat_var_list = flattenList(variable_list)
    var_dict = dict(flat_var_list)
    vars_stack_size = 4 * len(flat_var_list)
    var_par_to_stack = createStackPointerDict(flat_var_list, 0)
    return (var_dict, var_par_to_stack)

@dcDecorator
def initialiseVariables(var_dict: Dict[str, Union[OperatorNode, int]], pointer_dict: Dict[str, str]) -> str:
    
    

@dcDecorator
def caveCompiler(ast: list[FunctionDefNode]) -> str:
    function_list = dict(map(getFunctionName, ast))
    variable_dict, var_to_stack_dict = prepVariableForComp(function_list)
    var_init_code = initialiseVariables(variable_dict, var_to_stack_dict)



def main():
    code = open("cave_code.txt", "r")
    code_text = code.readlines()
    code.close()

    print(caveCompiler(parser(caveLexer(code_text))))

main()