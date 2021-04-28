from cave_classes import *

def toToken(keyword_tup: Tuple[int,str], linenr: int) -> Token:
    if keyword_tup[1] == "plooga":
        return Token(TokenTypes.ADD, "plooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "mooga":
        return Token(TokenTypes.SUB, "mooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "kooga":
        return Token(TokenTypes.MUL, "kooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "dooga":
        return Token(TokenTypes.DIV, "dooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "isooga":
        return Token(TokenTypes.ASSIGN, "isooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "ifooga":
        return Token(TokenTypes.IF, "ifooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "elooga":
        return Token(TokenTypes.ELSE, "elooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "whooga":
        return Token(TokenTypes.WHILE, "whooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "eqooga":
        return Token(TokenTypes.EQUALS, "eqooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "greqooga":
        return Token(TokenTypes.GREQ, "greqooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "leeqooga":
        return Token(TokenTypes.LEEQ, "leeqooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "lesooga":
        return Token(TokenTypes.LESSER, "lesooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "grooga":
        return Token(TokenTypes.GREATER, "grooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "neqooga":
        return Token(TokenTypes.NOTEQUAL, "neqooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "booga":
        return Token(TokenTypes.END, "booga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "komooga":
        return Token(TokenTypes.SEP, "komooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "hoooga":
        return Token(TokenTypes.OPENPAR, "hoooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "hsooga":
        return Token(TokenTypes.CLOSEPAR, "hsooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "broooga":
        return Token(TokenTypes.OPENBR, "broooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "brsooga":
        return Token(TokenTypes.CLOSEBR, "brsooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "fdooga":
        return Token(TokenTypes.DEF, "fdooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == "retooga":
        return Token(TokenTypes.RETURN, "retooga", tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1].isdigit():
        return Token(TokenTypes.NUMBER, keyword_tup[1], tuple(linenr, keyword_tup[0]))
    elif keyword_tup[1] == re.fullmatch("[a-zA-Z]\w*"):
        return Token(TokenTypes.ID, keyword_tup[1], tuple(linenr, keyword_tup[0]))
    

def lineToKeywords(line: str) -> List[Tuple[int,str]]:
    line = line.strip()
    line = line.split()
    enum_line = list(enumerate(line, 1))
    return enum_line


def keywordsToToken(keywords_list: Tuple[int,Tuple[int,str]], linenr: int) -> List[Token]:
    #(linenr,[(pos,keyword)...])
    tokens_list = list(map(toToken, keywords_list[1], keywords_list[0]))
    return tokens_list


def caveLexer(code_text: List[List[str]], token_types: Type[Enum] = TokenTypes) -> List[Token]:
    keywords = []
    keywords = list(enumerate(map(lineToKeywords, code_text), 1))
    token_list = list(map(keywordsToToken, keywords))
    return keywords


def main():
    code = open("cave_code.txt", "r")
    code_text = code.readlines()
    code.close()
    print(caveLexer(code_text))
    