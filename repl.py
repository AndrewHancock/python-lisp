from read import read_exp, TokenTypes

while True:
    tokens = None

    while not tokens or tokens[1] != (TokenTypes.SYMBOL, "quit"):
        print("--> ", end="")
        tokens = read_exp()

