def get_number_from_list(tokens: list[str]):
    for token in tokens:
        if token.isdigit():
            return token
