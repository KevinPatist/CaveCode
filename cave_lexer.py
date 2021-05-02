from cave_classes import *

def toToken(keyword_tup: Tuple[int,str], linenr: int) -> Token:
    if keyword_tup[1] == "plooga":
        return Token(TokenTypes.ADD, "plooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "mooga":
        return Token(TokenTypes.SUB, "mooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "kooga":
        return Token(TokenTypes.MUL, "kooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "dooga":
        return Token(TokenTypes.DIV, "dooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "isooga":
        return Token(TokenTypes.ASSIGN, "isooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "ifooga":
        return Token(TokenTypes.IF, "ifooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "elooga":
        return Token(TokenTypes.ELSE, "elooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "whooga":
        return Token(TokenTypes.WHILE, "whooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "eqooga":
        return Token(TokenTypes.EQUALS, "eqooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "greqooga":
        return Token(TokenTypes.GREQ, "greqooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "leeqooga":
        return Token(TokenTypes.LEEQ, "leeqooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "lesooga":
        return Token(TokenTypes.LESSER, "lesooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "grooga":
        return Token(TokenTypes.GREATER, "grooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "neqooga":
        return Token(TokenTypes.NOTEQUAL, "neqooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "booga":
        return Token(TokenTypes.END, "booga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "komooga":
        return Token(TokenTypes.SEP, "komooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "hoooga":
        return Token(TokenTypes.OPENPAR, "hoooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "hsooga":
        return Token(TokenTypes.CLOSEPAR, "hsooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "broooga":
        return Token(TokenTypes.OPENBR, "broooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "brsooga":
        return Token(TokenTypes.CLOSEBR, "brsooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "fdooga":
        return Token(TokenTypes.DEF, "fdooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1] == "retooga":
        return Token(TokenTypes.RETURN, "retooga", (linenr, keyword_tup[0]))
    elif keyword_tup[1].isdigit():
        return Token(TokenTypes.NUMBER, keyword_tup[1], (linenr, keyword_tup[0]))
    elif re.fullmatch("[a-zA-Z]\w*", keyword_tup[1]):
        return Token(TokenTypes.ID, keyword_tup[1], (linenr, keyword_tup[0]))
    

def lineToKeywords(line: str) -> List[Tuple[int,str]]:
    line = line.strip()
    line = line.split()
    enum_line = list(enumerate(line, 1))
    return enum_line


A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def tokenMap(func: Callable[[A, B], C], keywords_list: List[Tuple[int,str]], linenr: int) -> List[Token]:
    if len(keywords_list) == 0:
        return []
    else:
        head, *tail = keywords_list
        return [func(head, linenr)] + tokenMap(func, tail, linenr)


def keywordsToToken(keywords_list: Tuple[int,List[Tuple[int,str]]]) -> List[Token]:
    #(linenr,[(pos,keyword),(pos,keyword)...])
    tokens_list = list(tokenMap(toToken, keywords_list[1], keywords_list[0]))
    return tokens_list


def flattenTokenList(token_list: List[List[Token]]) -> List[Token]:
    flat_list = reduce(lambda x, y: x + y, token_list)
    return flat_list


def caveLexer(code_text: List[List[str]], token_types: Type[Enum] = TokenTypes) -> List[Token]:
    keywords = []
    keywords = list(enumerate(map(lineToKeywords, code_text), 1))
    token_list = list(map(keywordsToToken, keywords))
    flat_token_list = flattenTokenList(token_list)
    return flat_token_list


def main():
    code = open("cave_code.txt", "r")
    code_text = code.readlines()
    code.close()
    print(caveLexer(code_text))

main()