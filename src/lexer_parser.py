from position import TokenPosition, ParserPosition
from tokens import *
from parselets import *
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
        self.debug = debug
        self.tokens = lexer.tokenize()
        self.position = ParserPosition(-1, self.tokens)
        self.prefix_parselets = {}
        self.infix_parselets = {}

        self.register_prefix("NUMBER", ValueParselet())
        self.register_prefix("IDENTIFIER", ValueParselet())
        self.register_infix("=", AssignmentParselet(50))
        self.register_infix("+", BinaryOperatorParselet(10))
        self.register_infix("-", BinaryOperatorParselet(10))
        self.register_infix("*", BinaryOperatorParselet(20))
        self.register_infix("/", BinaryOperatorParselet(20))

        if self.debug:
            print(self.tokens)
    def error(self, message, token):
        print(f"Error at line: {token.position.ln}")
        print(">>  "+token.position.highlight_line())
        print(message)

        sys.exit()
    def register_prefix(self, token_type, parselet):
        self.prefix_parselets[token_type] = parselet

    def register_infix(self, token_type, parselet):
        self.infix_parselets[token_type] = parselet
    def parse_expression(self, precedence=0):
        token = self.position.consume()
        prefix = self.prefix_parselets.get(token.token_type)
        if prefix is None:
            raise Exception(f"No prefix parselet for {token.token_type}")
        prefix=prefix.parse
        left = prefix(self, token)
        while precedence < self.get_precedence():
            token = self.position.consume()
            infix = self.infix_parselets.get(token.token_type)
            if infix is None:
                raise ValueError(f"No infix parselet for {token.token_type}")
            left = infix.parse(self, left, token)
        return left
    def get_precedence(self):
        next_token = self.position.peek()
        if next_token.token_type in self.infix_parselets:
            return self.infix_parselets[next_token.token_type].precedence
        return 0

lexer = Lexer("a=10")
parser = Parser(lexer=lexer, debug=True)
print(parser.parse_expression())