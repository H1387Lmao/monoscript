from position import TokenPosition
from tokens import *
import sys

class Lexer:
    def __init__(self, source):
        self.position = TokenPosition(1, -1, -1, source)
        self.source = source
    def get_type(self, token):
        if token.isdigit(): 
            return (TOKEN_TYPE.NUMBER, int(token))
        else: 
            return (TOKEN_TYPE.IDENTIFIER, token)
    def add(self, name, value=None):
        if name == "EOF":
            self.position.consume()
        self.tokens.append(Token(name, value, self.position.copy()))
    def try_current_token(self):
        if self.current_token:
            self.add(*self.get_type(self.current_token))
            self.current_token=""
    def tokenize(self):
        self.current_token = ""
        self.current_char = ""
        self.tokens=[]
        while self.current_char is not None:
            self.current_char = self.position.peek()
            if self.current_char is None:
                break
            self.position.consume()
            if self.current_char in "\n\t ":
                continue

            if self.current_char in "+-*/=;(){}":
                self.try_current_token()
                self.add(self.current_char)
            else:
                if self.current_char == '"':
                    string = ""
                    while self.position.peek()!='"':
                        string += self.position.consume()
                    self.add("STRING", string)
                    self.position.consume()
                    continue

                self.current_token+=self.current_char
                if self.current_token in KEYWORDS:
                    self.add(self.current_token)
                    self.current_token=""
        self.try_current_token()
        self.add("EOF")
        return self.tokens