from read import read_exp, TokenTypes, parse_exp


while True:
    tokens = None
    while not tokens or tokens[1] != (TokenTypes.SYMBOL, "quit"):
        print("--> ", end="")
        tokens = read_exp()
        expression = parse_exp(tokens, [])
        print(expression)

