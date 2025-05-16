from position import TokenPosition, ParserPosition
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
                return

            if self.current_char in "+-*/=":
                self.try_current_token()
                self.add(self.current_char)
            else:
                self.current_token+=self.current_char
                if self.current_token in KEYWORDS:
                    self.add("KEYWORD",self.current_token)
        self.try_current_token()
        self.add("EOF")
        return self.tokens

class Parser:
    def __init__(self, lexer, debug=False):
        self.tokens = lexer.tokenize()
        self.position=ParserPosition(-1,self.tokens)
        if debug: print(self.tokens)
    def binop(self, func, tokens):
        left = func()
        while self.position.peek().token_type in tokens:
            operation=self.position.consume()
            right = func()
            left = (operation, left, right)
        return left
    def parse_value(self):
        next_tk = self.position.peek()
        if next_tk.token_type in [TOKEN_TYPE.NUMBER,
                                  TOKEN_TYPE.IDENTIFIER]:
            self.position.consume()
            return next_tk
        raise SyntaxError(f"Unexpected token: {next_tk}")
    def parse_term(self):
        return self.binop(self.parse_value, ["*","/"])
    def parse_expr(self):
        return self.binop(self.parse_term, ["+","-"])

lexer = Lexer("10+10")
parser = Parser(lexer=lexer, debug=True)
print(parser.parse_expr())
