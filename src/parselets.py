from tokens import TOKEN_TYPE

class ValueParselet:
    def parse(self, parser, token):
        return token

class BinaryOperatorParselet:
    def __init__(self, precedence):
        self.precedence = precedence

    def parse(self, parser, left, token):
        right = parser.parse_expression(self.precedence)
        return (token.token_type, left, right)

class AssignmentParselet:
    def __init__(self, precedence):
        self.precedence = precedence

    def parse(self, parser, left, token):
        if left.token_type != TOKEN_TYPE.IDENTIFIER:
            parser.error(f"Cannot initialize a value to type: {left.token_type}", left)
        right = parser.parse_expression(self.precedence)
        return (token.token_type, left, right)