from io import TextIOWrapper
from pycpp import StringStream
from tokens import TOKEN_TYPE, Token

class CodeGenerator:
    def __init__(self, ast, fp: TextIOWrapper):
        self.ast = ast
        self.fp = fp

        self.stack_loc = 0
        self.variables = []

        self.gen()
    def parse_value(self, node):
        if isinstance(node, Token):
            if node.token_type == TOKEN_TYPE.NUMBER:
                return node.token_value
            self.code << "mov eax, [ebp-" << self.get_variable_loc(node.token_value)*4<<"]\n" 
            return "eax"
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
            self.code << op << " ebx, ecx" << "\n"
            self.code << "mov eax, ebx" << "\n"
            return "eax"


    def get_variable_loc(self, var_name):
        for i, var in enumerate(self.variables, start=1):
            if var == var_name:
                return i
        print(f"Uninitialized variable: {var_name}")
        print(self.variables)
    def generate_stmt(self, node):
        if node[0] == "assign":
            dt = node[1]
            vn = node[2]
            value = self.parse_value(node[3])

            if dt.token_value == "int":
                self.stack_loc += 1
                self.code << "push ebp" << "\n"
                self.code << "mov ebp, esp" << "\n"
                self.code << "sub esp, "<< self.stack_loc*4 << "\n" #reserve 1 variable
                self.code << "mov dword [ebp-"<< self.stack_loc*4 <<"], " << value << "\n"
                self.variables.append(vn.token_value)
        elif node[0] == "exit":
            exit_code = self.parse_value(node[1])
            self.code << "mov ebx, " << exit_code << "\n"
            self.code << "mov eax, 1" << "\n"
            self.code << "int 0x80" << "\n" 
    def generate_prog(self):
        prog = self.ast
        for stmt in prog:
            self.generate_stmt(stmt)
    def gen(self):
        self.code = StringStream()
        self.code << "global _start" << "\n"
        self.code << "_start:" << "\n"

        self.generate_prog()

        self.fp.write(self.code.value())

        self.fp.close()
