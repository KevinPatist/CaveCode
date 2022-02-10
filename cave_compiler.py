from argparse import Action
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
def getVariableList(function: FunctionDefNode) -> list[Tuple[str, int]]:
    if len(function.parameters) > 0:
        var_list = list(reduce(lambda x, y: [(x, function.parameters[x])] + [(y, function.parameters[y])], function.parameters.keys()))
        new_var_list = list(map(getNewVars, function.action_list))
        pre_var_list = var_list + new_var_list
    else:
        new_var_list = list(map(getNewVars, function.action_list))
        pre_var_list = new_var_list
    total_var_list = list(reduce(lambda x, y: [x] + [y] if y is not None else x, pre_var_list))
    print(total_var_list)

@dcDecorator
def caveCompiler(ast: list[FunctionDefNode]) -> str:
    function_list = dict(map(getFunctionName, ast))
    variable_list = list(map(getVariableList, function_list.values()))
    print(variable_list)

def main():
    code = open("cave_code.txt", "r")
    code_text = code.readlines()
    code.close()

    print(caveCompiler(parser(caveLexer(code_text))))

main()