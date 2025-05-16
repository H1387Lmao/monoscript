from parser import Parser
from lexer import Lexer
from code_generator import CodeGenerator
from pprint import pprint

while True:
    inp = input(">>> ")
    if inp == "exit": break
    lexer = Lexer(inp)
    parser = Parser(lexer=lexer, debug=True)
    try:
        ast = parser.parse_prog()
        pprint(ast)
        if ast is not None:
            code_Gen = CodeGenerator(ast, open("./codegen/out.asm", "w"))
    except Exception as e:
        print("Error occured")
        print(e)