from abc import ABC
from dataclasses import dataclass


@dataclass
class Expression(ABC):
    pass

@dataclass
class Symbol(Expression):
    text: str


@dataclass
class Number(Expression):
    value: float


@dataclass
class String(Expression):
    value: str


@dataclass
class List(Expression):
    value: list


@dataclass
class QuotedExpression(Expression):
    expression: Expression