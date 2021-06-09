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
  De classes die gebruikt worden voor de AST binnen CaveCode stammen allemaal af van een base [Node class](watkanjewel.nl). Uit deze base node erven drie andere classes waaruit weer subclasses erven:
  - [ValueNode](watkanjewel.nl):
    - [VariableNode](watkanjewel.nl)
    - [FunctionCallNode](watkanjewel.nl)
    - [OperatorNode](watkanjewel.nl)

  - [ActionNode](watkanjewel.nl)
    - [AssignNode](watkanjewel.nl)
    - [IfOrWhileNode](watkanjewel.nl)
    - [ReturnNode](watkanjewel.nl)

  - [FunctionDefNode](watkanjewel.nl)
- **Object-printing voor elke class:** Ja
- **Decorator:**
  - [Function definition](watkanjewel.nl)
  - Toegepast boven elke functie in de lexer, parser en interpreter.
  - [Voorbeeld](watkanjewel.nl)
- **Type-annotatie:**
  - Haskell-stijl in comments: Ja
  - Python-stijl in functiedefinities: Ja
- **Hogere orde functies:**
  - [Reduce](lexer->flattenTokenList)
  - [Map](lexer->caveLexer)
  - [Reduce](parser->flattenActionList)
  - [Reduce](runner->runIfOrWhile)
  - [Reduce](runner->runFunction)


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
    - [ParseError](parser->ParseError)
    - [RunnerError](runner->RunnerError)
