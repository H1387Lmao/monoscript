class TOKEN_TYPE:
    IDENTIFIER=0
    NUMBER=1

class Token:
    def __init__(self, token_type, token_value, position):
        self.token_type=token_type
        self.token_value = tokem_value
        self.position=position
    def __repr__(self):
        if self.token_value is None:
            return f"Token({self.token_type})"
        return "Token({self.token_type},{self.token_value})"
