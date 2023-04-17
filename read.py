from collections.abc import Iterable
from enum import Enum, auto
from re import compile
from dataclasses import dataclass
from abc import ABC
from typing import Iterator, Any


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


class RewindableIterator(Iterator):
    def __init__(self, wrapped_iterator: Iterator):
        self._wrapped_iterator = wrapped_iterator
        self._buffer = []
        self._rewind = False
        self._mark = False
        self._idx = -1

    def __next__(self) -> Any:
        if self._mark:
            if self._rewind and self._idx < len(self._buffer):
                next_item = self._buffer[self._idx]
            else:
                next_item = next(self._wrapped_iterator)
                self._buffer.append(next_item)
            self._idx += 1
            return next_item
        return next(self._wrapped_iterator)
        pass

    def rewind(self):
        self._rewind = True
        self._idx = 0

    def mark(self):
        self._mark = True
        self._idx = 0

    def reset(self):
        self._rewind = False
        self._mark = False
        self._buffer.clear()
        self._idx = -1


class ExpressionParser:

    def __init__(self):
        self._tokens = None
        self._idx = -1

    def parse(self, tokens: list[Token], idx=0):
        self._tokens = 0
        self._idx = -1

    def parse_exp(self) -> Expression:
        idx = self._idx

        return self.parse_list()

    def parse_list(self):
        list_stack = []

        while self._idx < len(self._tokens):
            token = self._tokens[self._idx]
            match token:
                case TokenTypes.L_PAREN, _:
                    list_stack.append([])
                case TokenTypes.R_PAREN, _:
                    temp = list_stack.pop()

                    if not list_stack:
                        return temp
                    else:
                        list_stack[-1].append(temp)
                case TokenTypes.SYMBOL, text:
                    list_stack[-1].append(Symbol(text))
                case TokenTypes.NUMBER, text:
                    list_stack[-1].append(float(text))
                case TokenTypes.STRING, text:
                    list_stack[-1].append(text)
        raise Exception("Unterminated list!")




def read_exp():
    s = input()
    tokens = list(tokenize_string(s))
    print(tokens)

    parsed_lists = parse_list(tokens)
    print(parsed_lists)
    return tokens
