class TOKEN_TYPE:
    IDENTIFIER="IDENTIFIER"
    NUMBER="NUMBER"
    STRING = "STRING"

KEYWORDS = ("int", "string", "if")

class Token:
    def __init__(self, token_type, token_value, position):
        self.token_type=token_type
        self.token_value = token_value
        self.position=position
    def __repr__(self):
        value = f"Token('{self.token_type}', " if self.token_value is None else f"Token({self.token_type}, '{self.token_value}', "
        value += ", ".join([str(self.position.ln), str(self.position.start)])+")"
        return value
