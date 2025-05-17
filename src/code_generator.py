from io import TextIOWrapper
from pycpp import StringStream
from tokens import TOKEN_TYPE, Token
import sys
import base64

def bs64(s: str):
    return base64.b64encode(s.encode("ascii")).decode("ascii").rstrip("=").replace("+", "__").replace("/", "_")

class CodeGenerator:
    def __init__(self, ast, fp: TextIOWrapper):
        self.ast = ast
        self.fp = fp

        self.stack_loc = 0
        self.variables = []
        self.strings=[]
        self.scopes=[0]

        self.gen()
    def parse_value(self, node):
        if isinstance(node, Token):
            if node.token_type == TOKEN_TYPE.NUMBER:
                return node.token_value
            elif node.token_type == TOKEN_TYPE.STRING:
                decoded = bs64(node.token_value)
                if node.token_value not in [s for _, s in self.strings]:
                    self.strings.append((decoded, node.token_value))
                return decoded
            var_scope = self.get_variable_loc(node.token_value)
            if isinstance(var_scope, int):
                self.code << "mov eax, [ebp-" << var_scope*4+self.scopes[-1]*4<<"]\n" 
                return "eax"
            else:
                self.code << "mov eax, " << var_scope << "\n"
                return var_scope
        elif node[0].token_type in "+/-*":
            left = self.parse_value(node[1])
            self.code<<"mov ebx, "<< left << "\n"
            right = self.parse_value(node[2])
            self.code<<"mov ecx, "<<right << "\n"
            op = node[0].token_type
            if op == "+":
                op="add"
            elif op == "-":
                op="sub"
            elif op == "*":
                op="mul"
            elif op == "/":
                op="div"
            if op in ["add","sub"]:
                self.code << op << " ebx, ecx" << "\n"
                self.code << "mov eax, ebx" << "\n"
            else:
                self.code << "mov eax, ebx" << "\n"
                self.code << op << " ecx\n"
            return "eax"


    def get_variable_loc(self, var_name):
        for var, value in self.strings:
            if var == var_name:
                return f"[{var}]"
        for i, var in enumerate(self.variables, start=1):
            if var == var_name:
                return i
        print(f"Uninitialized variable: {var_name}")
        print(self.variables)
    def start_scope(self):
        self.scopes.append(len(self.variables))
    def end_scope(self):
        pop_count = len(self.variables) - self.scopes[-1]
        if pop_count != 0:
            self.code << "add esp, "<< pop_count * 4 << "\n"
            [self.variables.pop() for _ in range(pop_count)]
        self.stack_loc -= pop_count
        self.scopes.pop()

    def generate_stmt(self, node):
        if node[0] == "assign":
            dt = node[1]
            vn = node[2]
            value = self.parse_value(node[3])

            if vn.token_value in self.variables:
                print("Variable already initialized")
                sys.exit()

            if dt.token_type == "int":
                self.stack_loc += 1
                self.code << "push ebp" << "\n"
                self.code << "mov ebp, esp" << "\n"
                self.code << "sub esp, "<< self.stack_loc*4 << "\n" #reserve 1 variable
                self.code << "mov dword [ebp-"<< self.stack_loc*4 <<"], " << value << "\n"
                self.variables.append(vn.token_value)
            elif dt.token_type == "string":
                self.stack_loc += 1
                self.strings.append((vn.token_value, value))
                self.variables.append(vn.token_value)
        elif node[0] == "function_call":
            if node[1] == "exit":
                exit_code = self.parse_value(node[2])
                self.code << "mov ebx, " << exit_code << "\n"
                self.code << "mov eax, 1" << "\n"
                self.code << "int 0x80" << "\n" 
            elif node[1] == "print":
                msg=self.parse_value(node[2])
                self.code << "mov eax, 4" << "\n"
                self.code << "mov ebx, 1" << "\n"
                self.code << "mov ecx, " << msg << "\n"
                self.code << "mov edx, " << len(msg) << "\n"
                self.code << "int 0x80" << '\n'
        elif node[0] == "scope":
            self.start_scope()
            self.generate_prog(node[1])
            
            self.end_scope()
        else:
            print(f"Unknown statement: {node[0]}")
            return
    def generate_prog(self, stmts=None):
        if stmts is None:
            stmts = self.ast
        for stmt in stmts:
            self.generate_stmt(stmt)

    def gen(self):
        self.code = StringStream()
        self.code << "section .text" << "\n\n"
        self.code << "global _start" << "\n"
        self.code << "_start:" << "\n"

        self.generate_prog()

        if self.strings:
            self.code <<"\nsection .data" << "\n"
            for string, value in self.strings:
                self.code << string.replace(" ","_") << f" db '{value}', 0" << "\n"

        self.fp.write(self.code.value())

        self.fp.close()
