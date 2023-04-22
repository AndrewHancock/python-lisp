from typing import Optional

from lisp_ast import Expression, Symbol, Number, String, List
from read import TokenTypes, Token


class TokenParser:
    def __init__(self, tokens: list[Token], pos=0):
        self._tokens = tokens
        self._pos = pos

    def token(self) -> Token:
        return self._tokens[self._pos]

    def token_type(self) -> TokenTypes:
        token_type, _ = self.token()
        return token_type

    def token_value(self) -> str:
        _, token_value = self.token()
        return token_value

    def eof(self) -> bool:
        return self._pos >= len(self._tokens)

    def advance(self, i=1):
        self._pos += i

    def match_token_types(self, token_types: list[TokenTypes]) -> Optional[list[str]]:
        result = []
        for token_type in token_types:
            if self.eof():
                return None
            elif token_type == self.token_type():
                result.append(self.token_value())
                self.advance()
            else:
                return None
        return result

    def parse_exp_rest(self) -> Optional[list[Expression]]:
        result_list = []
        while not self.eof() and self.token_type() != TokenTypes.R_PAREN:
            if self.token_type() == TokenTypes.L_PAREN:
                result_list.append(self.parse_exp())
            elif self.token_type() == TokenTypes.SYMBOL:
                result_list.append(Symbol(self.token_value()))
                self.advance()
            elif self.token_type() == TokenTypes.NUMBER:
                result_list.append(Number(float(self.token_value())))
                self.advance()
            elif self.token_type() == TokenTypes.STRING:
                result_list.append(String(self.token_value()))
                self.advance()

        if self.token_type() == TokenTypes.R_PAREN:
            self.advance()
            return result_list
        else:
            return None

    def parse_exp(self) -> Optional[Expression]:
        if self.token_type() != TokenTypes.L_PAREN:
            return None
        else:
            self.advance()

        rest = self.parse_exp_rest()
        return List(rest)




