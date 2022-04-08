# CaveCode
CaveCode is een programmeertaal die is ontworpen door Kevin Patist als deel van een opdracht voor het vak Advanced Technical Programming.

## Turing-compleet
------------------------------
CaveCode is een Turing-complete programmeertaal omdat de volgende dingen mogelijk zijn:
- Binnen CaveCode is conditional branching mogelijk door gebruik te maken van if statements.
  In deze if statements kunnen functies worden aangeroepen, meer if statements plaatsvinden en overige acties worden uitgevoerd.
- Binnen CaveCode zijn while loops mogelijk die oneindig kunnen loopen tot er een stack overflow plaatsvindt of de recursion limit is bereikt.
- Er is geen limiet voor het aantal variabelen dus je kan er zo veel maken als de hardware toelaat en er nog unieke namen beschikbaar zijn.
- In CaveCode kunnen waardes worden teruggegeven via de main functie.
- Input kan worden geleverd door het in de main functie in de code te zetten.

## Functionele code
De lexer, parser en interpreter voor CaveCode zijn in een functionele stijl geschreven en bevatten alleen pure functies die geen shared state aanpassen of gebruiken.

## Loops
CaveCode ondersteund het gebruik van while loops. Hieronder een voorbeeld van een loop die 5 bij a telt zolang a onder de 17 blijft.
```
fdooga plus5 hoooga a hsooga broooga
  whooga hoooga a lesooga 17 hsooga broooga
    a isooga a plooga 5 booga
  brsooga
  result isooga a booga
brsooga
```

## Bevat
- **Classes met inheritance:**
  De classes die gebruikt worden voor de AST binnen CaveCode stammen allemaal af van een base [Node class](https://github.com/KevinPatist/CaveCode/blob/main/cave_classes.py#L58). Uit deze base node erven drie andere classes waaruit weer subclasses erven:
  - [ValueNode](https://github.com/KevinPatist/CaveCode/blob/main/cave_classes.py#L71):
    - [VariableNode](https://github.com/KevinPatist/CaveCode/blob/main/cave_classes.py#L84)
    - [FunctionCallNode](https://github.com/KevinPatist/CaveCode/blob/main/cave_classes.py#L98)
    - [OperatorNode](https://github.com/KevinPatist/CaveCode/blob/main/cave_classes.py#L113)

  - [ActionNode](https://github.com/KevinPatist/CaveCode/blob/main/cave_classes.py#L129)
    - [AssignNode](https://github.com/KevinPatist/CaveCode/blob/main/cave_classes.py#L142)
    - [IfOrWhileNode](https://github.com/KevinPatist/CaveCode/blob/main/cave_classes.py#L157)
    - [ReturnNode](https://github.com/KevinPatist/CaveCode/blob/main/cave_classes.py#L173)

  - [FunctionDefNode](https://github.com/KevinPatist/CaveCode/blob/main/cave_classes.py#L187)
- **Object-printing voor elke class:** Ja
- **Decorator:**
  - [Function definition](https://github.com/KevinPatist/CaveCode/blob/main/cave_classes.py#L11)
  - Toegepast boven elke functie in de lexer, parser en interpreter.
  - [Voorbeeld](https://github.com/KevinPatist/CaveCode/blob/main/cave_parser.py#L19)
- **Type-annotatie:**
  - Haskell-stijl in comments: Ja
  - Python-stijl in functiedefinities: Ja
- **Hogere orde functies:**
  - [Reduce](https://github.com/KevinPatist/CaveCode/blob/main/cave_lexer.py#L97)
  - [Map](https://github.com/KevinPatist/CaveCode/blob/main/cave_lexer.py#L108)
  - [Reduce](https://github.com/KevinPatist/CaveCode/blob/main/cave_parser.py#L140)
  - [Reduce](https://github.com/KevinPatist/CaveCode/blob/main/cave_runner.py#L72)
  - [Reduce](https://github.com/KevinPatist/CaveCode/blob/main/cave_runner.py#L116)


## Interpreter-functionaliteit Must-have:
- **Functies:** Meer per file
- **Functie parameters:** Meegegeven aan interpreter door in de main functie als variabelen toe te voegen en deze bij de functie aanroep mee te geven.
- **Functies kunnen andere functies aanroepen:**

  ```
  fdooga even hoooga n hsooga broooga
    ifooga hoooga n eqooga 0 hsooga broooga
        retooga 0 booga
    brsooga
    m isooga n mooga 1 booga
    retooga odd hoooga m hsooga booga
  brsooga

  fdooga odd hoooga n hsooga broooga
    ifooga hoooga n eqooga 0 hsooga broooga
        retooga 1 booga
    brsooga
    m isooga n mooga 1 booga
    retooga even hoooga m hsooga booga
  brsooga

  fdooga main hoooga hsooga broooga
    retooga odd hoooga 21 hsooga booga
  brsooga
  ```
- **Functie resultaat wordt op de volgende manier weergegeven:**
  - Als return variabele in de variabelen lijst.
  - Uit de main geprint na het runnen van het programma.

## Interpreter-functionaliteit should/could-have:
  - **Error-messaging:** geïmplementeerd door middel van de volgende error classes:
    - [ParseError](https://github.com/KevinPatist/CaveCode/blob/main/cave_parser.py#L3)
    - [RunnerError](https://github.com/KevinPatist/CaveCode/blob/main/cave_runner.py#L6)

## Speciale regels:
- De taal ondersteund geen globale variabelen
- Je mag geen herhalende parameter/variabelen namen hebben in hetzelfde programma
- De reken regels gaan van rechts naar links
- Je mag geen variabelen aanmaken in loops of if statements
- Je mag geen variabelen aanpassen buiten loops of if statements
- Je kan niet delen als je de compiler editie gebruikt

# Gebruik van de taal:
## Python 3.10:
Binnen de interpreter en compiler worden functionaliteiten gebruikt die nieuw zijn in Python 3.10.
Hierom is het dus nodig om je Python versie te updaten naar minimaal versie 3.10.

## Code schrijven:
De code die je schrijft moet je plaatsen in het bestand cave_code.txt om deze te gebruiken met de interpreter of compiler.

## Interpreter gebruiken:
Om de interpreter te gebruiken moet je het cave_runner.py bestand runnen met python.
De interpreter geeft via de terminal/console het resultaat van de code.

# CaveCode Compiler:
## Hoe te compilen:
### Hwlib:
Om de compiler te gebruiken voor embedded systemen heb je de hwlib library nodig samen met zijn dependencies.
Als je systeem runt op Linux kan je gebruik maken van [deze](https://github.com/wovo/installers) github repository om alles te installeren.
Als je Windows runt moet je het handmatig installeren door de repositories die in [dit](https://github.com/wovo/installers/blob/master/ubuntu-20/ubuntu2) bestand worden gecloned, zelf te clonen in dezelfde hoofdmap.
Voor Mac heb ik geen idee hoe je hwlib moet installeren.

### Gebruik van compiler
Voor je de compiler kan gebruiken moet je eerst in de Makefiles een paar dingen aanpassen:
- Makefile.due:
  - SERIAL_PORT: Hier moet je de poort van je arduino aangeven zodat deze geflasht kan worden
  - RTOS: Hierin moet je het relatieve pad naar de RTOS map specificeren
- Makefile.link:
  - TI-SOFTWARE: Hier moet het relatieve pad naar de map met alle geclonede github repositories.

Als je de compiler daadwerkelijk wil runnen kan dit door een terminal te openen in de CaveCode map.
In deze terminal roep je de commando's make clean en make run aan.
makefile aanroepen vanuit CaveCode map
CaveCode code moet in cave_code.txt
