from enum import Enum, auto
from re import compile

from lisp_ast import String, Number, Symbol, Expression, List


class TokenTypes(Enum):
    L_PAREN = auto()
    R_PAREN = auto()
    QUOTE = auto()
    SYMBOL = auto()
    NUMBER = auto()
    STRING = auto()


token_regex = {
    TokenTypes.SYMBOL: compile("[-+*/!@%^&=.a-zA-Z0-9_]+"),
    TokenTypes.NUMBER: compile("[0-9]*[.]?[0-9]+"),
    TokenTypes.STRING: compile('\"[^\"]*\"')
}


Token = tuple[TokenTypes, str]


def tokenize_string(string):
    i = 0
    while i < len(string):
        while (c := string[i]) in " \t\n":
            i += 1

        if c == "(":
            i += 1
            yield TokenTypes.L_PAREN, "("
        elif c == ")":
            i += 1
            yield TokenTypes.R_PAREN, ")"
        elif c == "'":
            i += 1
            yield TokenTypes.QUOTE, "'"
        else:
            found = False
            for token_type in [TokenTypes.NUMBER, TokenTypes.SYMBOL, TokenTypes.STRING]:
                r = token_regex[token_type]
                match = r.match(string, pos=i)
                if match:
                    start, end = match.span()
                    yield token_type, string[start:end]
                    i = end
                    found = True
                    break
            if not found:
                raise Exception("Unknown character {} at {}: {}", c, i, string[i:15])


def parse_exp(tokens: list[Token], acc: list[Expression]) -> list[Expression]:
    if not tokens:
        return acc

    match tokens:
        case [(TokenTypes.SYMBOL, text), *rest]:
            acc.append(Symbol(text))
            return parse_exp(rest, acc)
        case [(TokenTypes.NUMBER, text), *rest]:
            acc.append(Number(float(text)))
            return parse_exp(rest, acc)
        case [(TokenTypes.STRING, text), *rest]:
            acc.append(String(text))
            return parse_exp(rest, acc)
        case [(TokenTypes.L_PAREN, _), *rest]:
            acc.append(TokenTypes.L_PAREN)
            return parse_exp(rest, acc)
        case[(TokenTypes.R_PAREN, _), *rest]:
            for i in range(len(acc) -1, -1, -1):
                if acc[i] == TokenTypes.L_PAREN:
                    acc[i] = List(acc[i + 1:])
                    return parse_exp(rest, acc[:i + 1])
            raise Exception("Unmatched closing paren!")
        case _:
            raise Exception("Unknown form.")


def read_exp():
    s = input()
    tokens = list(tokenize_string(s))
    print(tokens)
    return tokens
