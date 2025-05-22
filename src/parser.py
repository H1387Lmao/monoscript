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
    def parse_value(self, allowed=[TOKEN_TYPE.NUMBER, TOKEN_TYPE.IDENTIFIER, TOKEN_TYPE.STRING]):
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
    def parse_condition(self):
        if self.position.peek().token_type == "(":
            self.position.consume()
            left=self.parse_expr()
            compareOperation = self.position.consume()
            right = self.parse_expr()
            self.position.get(")")
            return (compareOperation, left, right)
    def parse_if_stmt(self):
        condition = self.parse_condition()
        return ("if", condition, self.parse_stmt())
    def parse_stmt(self):
        if self.position.peek().token_type in ["int", "string"]:
            vartype = self.position.consume()
            stmt=self.parse_assignment(vartype)
            self.position.get(";") #expect a semicolon
            return stmt
        elif self.position.peek().token_type == TOKEN_TYPE.IDENTIFIER:
            if self.position.peek(2).token_type == '(':
                var_name = self.position.consume().token_value
                self.position.get("(")
                res = self.parse_expr()
                self.position.get(")")
                self.position.get(";")
                return ("function_call", var_name, res)
        elif self.position.peek().token_type == "{":
            self.position.consume()
            res = self.parse_prog("}")
            self.position.get("}")
            return ("scope", res)
        elif self.position.peek().token_type in "if":
            self.position.consume()
            return self.parse_if_stmt()
        else:
            print("WTF IS THIS", self.position.peek().token_type)
    def parse_prog(self, token_type ="EOF"):
        stmts=[]
        while self.position.peek().token_type!=token_type:
            stmts.append(self.parse_stmt())
        return stmts