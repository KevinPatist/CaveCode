from cave_parser import *

'''
Stappen:
Aantal variabelen tellen (inclusief parameters)

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
