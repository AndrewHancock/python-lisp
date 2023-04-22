from enum import Enum, auto
from re import compile
from typing import Callable

from lisp_ast import String, Number, Symbol, Expression, List, QuotedExpression


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


class ReduceType(Enum):
    LIST = auto()
    QUOTE = auto()


def reduce_expression(acc: list[Expression | ReduceType],
                      reduce_type: ReduceType,
                      reduce: Callable[[list[Expression]], Expression]
                      ) -> list[Expression | ReduceType]:
    for i in range(len(acc) - 1, -1, -1):
        if acc[i] == reduce_type:
            exp = reduce(acc[i + 1:])
            return push_exp(acc[:i], exp)
    raise Exception("Expected ReduceType not found.")


def push_exp(stack: list[Expression | ReduceType], exp: Expression) -> list[Expression | ReduceType]:
    if stack and stack[-1] == ReduceType.QUOTE:
        stack[-1] = QuotedExpression(exp)
    else:
        stack.append(exp)
    return stack


def parse_exp(tokens: list[Token], acc: list[Expression | ReduceType]) -> list[Expression]:
    if not tokens:
        return acc

    match tokens:
        case [(TokenTypes.SYMBOL, text), *rest]:
            push_exp(acc, Symbol(text))
            return parse_exp(rest, acc)
        case [(TokenTypes.NUMBER, text), *rest]:
            push_exp(acc, Number(float(text)))
            return parse_exp(rest, acc)
        case [(TokenTypes.STRING, text), *rest]:
            push_exp(acc, String(text))
            return parse_exp(rest, acc)
        case [(TokenTypes.L_PAREN, _), *rest]:
            acc.append(ReduceType.LIST)
            return parse_exp(rest, acc)
        case [(TokenTypes.R_PAREN, _), *rest]:
            acc = reduce_expression(acc,
                                    ReduceType.LIST,
                                    List)
            return parse_exp(rest, acc)
        case [(TokenTypes.QUOTE, _), *rest]:
            acc.append(ReduceType.QUOTE)
            return parse_exp(rest, acc)
        case _:
            raise Exception("Unknown form.")


def read_exp():
    s = input()
    tokens = list(tokenize_string(s))
    print(tokens)
    return tokens
