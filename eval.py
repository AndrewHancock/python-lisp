import dataclasses

from read import TokenTypes


def expect_type(expected: tuple[TokenTypes, str], actual: tuple[TokenTypes, str]):
    expected_type, _ = expected
    actual_type, _ = actual
    if expected != actual:
        raise Exception(f"Expected type not found. Expected: {expected} Actual: {actual}")



def evaluate_exp(tokens: list[tuple[TokenTypes, str]]):
