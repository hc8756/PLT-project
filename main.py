#from scanner import Scanner
from scanner import Scanner
from parser import Parser

def main():
    input_program = input("Please enter something: ")
    scanner = Scanner()
    tokens=scanner.lexer(input_program)
    # uncomment to test out scanner
    '''
    for token in tokens:
        print("<" + token[0] + ", \"" + token[1] + "\">")
    '''
    try:
        parser = Parser(tokens)
        ast = parser.parse()
        if ast:
            print(ast)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()