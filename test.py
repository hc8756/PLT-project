from scanner import Scanner
from parser import Parser
from code_generator import CodeGenerator

def main():
    #print("Please input a schedule: ")
    input_program = input("Please enter a schedule:")

    # tokenize 
    print("Lexical Analysis...")
    scanner = Scanner()
    tokens = scanner.lexer(input_program)
    print("Tokens:", tokens)

    # parse
    print("Parsing...")
    parser = Parser(tokens)
    try:
        ast = parser.parse()
        print("AST Generated:\n", ast)
    except Exception as e:
        print(f"Parsing Error: {str(e)}")
        return

    # code gen and pipe
    print("Code Generation and Execution...")
    code_generator = CodeGenerator(ast)
    code_generator.run_pipeline()

if __name__ == "__main__":
    main()
