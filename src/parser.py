from tokens import *
from position import ParserPosition

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
    def parse_value(self, allowed=[TOKEN_TYPE.NUMBER, TOKEN_TYPE.IDENTIFIER]):
        next_tk = self.position.peek()
        if next_tk.token_type in allowed:
            self.position.consume()
            return next_tk
        elif next_tk.token_type == "(":
            self.position.consume()
            res = self.parse_expr()
            self.position.get(")")
            return res
        raise SyntaxError(f"Unexpected token: {next_tk}")
    def parse_term(self):
        return self.binop(self.parse_value, ["*","/"])
    def parse_expr(self):
        return self.binop(self.parse_term, ["+","-"])
    def parse_assignment(self, variable_type):
        variable_name = self.parse_value([TOKEN_TYPE.IDENTIFIER])
        if self.position.peek().token_type == "=":
            self.position.get("=")
            return (
                "assign",
                variable_type, 
                variable_name,
                self.parse_expr()
            )
        else:
            return (
                "assign",
                variable_type,
                variable_name,
                None
            )

    def parse_stmt(self):
        if self.position.peek().token_value in ["int"]:
            vartype = self.position.consume()
            stmt=self.parse_assignment(vartype)
            self.position.get(";") #expect a semicolon
            return stmt
        elif self.position.peek().token_value == "exit":
            self.position.consume()
            self.position.get("(")
            res = self.parse_expr()
            self.position.get(")")
            self.position.get(";")
            return ('exit', res)
    def parse_prog(self):
        stmts=[]
        while self.position.peek().token_type!="EOF":
            stmts.append(self.parse_stmt())
        return stmts