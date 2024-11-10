temp = "" # holds strings while they are being evaluated
tokens=[]
keywords=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Style", "CONT", "heading_color", "rose_pink"]
days= ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
elements= ["heading_color"]
values= ["rose_pink"]

def transition_from_S0 (current_char):
    global temp
    global tokens
    if current_char.isalpha() or current_char=='_':
        temp+=current_char
        return 'KEYWORD_OR_LITERAL'
    if current_char.isdigit(): #even if it turns out to be string later, try finding time
        temp += current_char
        return 'TIME'
    elif current_char in '{};':
        tokens.append(('Delimiter', current_char))
        temp = ""
        return 'S0'
    elif current_char in '-=#':
        tokens.append(('Operator', current_char))
        temp = ""
        return 'S0'
    elif current_char.isspace():
        return 'S0' # just ignore
    else:
        return 'ERROR'

def transition_from_S1(current_char):
    global temp
    global tokens
    if current_char.isalpha() or current_char.isdigit() or current_char.isspace() or current_char=='_':
        temp += current_char
        for keyword in keywords:
            if keyword in temp: #if keyword is identified, add split temp into literal (may be nothing) and keyword and add both tokens
                keyword_start = temp.find(keyword)
                if(keyword_start>0):
                    tokens.append(("Literal", temp[:keyword_start]))
                tokens.append(("Keyword", temp[ keyword_start:]))
                temp = ""
                return 'S0'
        else:
            return 'KEYWORD_OR_LITERAL'
    elif current_char in '{};':
        tokens.append(('Literal', temp))
        tokens.append(('Delimiter', current_char))
        temp = ""
        return 'S0'
    elif current_char in '-=#':
        tokens.append(('Literal', temp))
        tokens.append(('Operator', current_char))
        temp = ""
        return 'S0'
    else:
        return 'ERROR'

def transition_from_S2 (current_char):
    global temp
    global tokens
    if current_char.isalpha() or current_char.isspace() or current_char=='_':
        temp += current_char # we thought it might be time, but it's a keyword or literal now
        return 'KEYWORD_OR_LITERAL'
    if current_char.isdigit() or current_char==':': # right now any <=4-char combination of numbers and ':'
        temp += current_char
        if len(temp) == 5:
            hours = temp[:2]
            minutes = temp[3:]
            if hours.isdigit() and minutes.isdigit(): 
                if 0 <= int(hours) <= 23 and 0 <= int(minutes) <= 59:
                    tokens.append(('Time', temp))
                    temp = ""
                    return 'S0'
        return 'TIME'
    elif current_char in '{};':
        tokens.append(('Time', temp))
        tokens.append(('Delimiter', current_char))
        temp = ""
        return 'S0'
    elif current_char in '-=#':
        tokens.append(('Time', temp))
        tokens.append(('Operator', current_char))
        temp = ""
        return 'S0'
    else:
        return 'ERROR'

def lexer(input_program):
    global tokens
    tokens = []
    current_state = 'S0'
    current_position=0
    while current_position < len(input_program): # for each char of the program
        current_char = input_program[current_position]
        if current_state == 'S0':
            current_state=transition_from_S0(current_char)
        elif current_state == 'KEYWORD_OR_LITERAL': # S1 in function naming convention
            current_state=transition_from_S1(current_char)
        elif current_state == 'TIME': # S2 in function naming convention
            current_state=transition_from_S2(current_char)
        elif current_state == 'ERROR':
            print('Unrecognized character at position ' + str(current_position))
            break
        current_position += 1
    if temp: # anything left in temp at this point would be literal
        tokens.append(('Literal', temp))
    return 0

# Assignment 2 code starts here
# TODO: implement class for lexer like you did for parser
# TODO: change documentation to not recognize quotations, they serve no function
# TODO: move parser to its own script
# TODO: create a main script that imports scanner and parser

# Boilerplate code for creating and representing nodes of tree
class ASTNode:
    def __init__(self, node_type, value=""):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child):
        if child is not None:
            self.children.append(child)

    def __repr__(self, level=0):
        indent = "  " * level
        repr_str = f"{indent}{self.node_type}: {self.value}\n"
        for child in self.children:
            repr_str += child.__repr__(level + 1)
        return repr_str

class Parser:
    def __init__(self, tokens, curr_pos=0):
        self.tokens=tokens
        self.curr_pos=0

    def current_token(self):
        if self.curr_pos < len(self.tokens):
            return self.tokens[self.curr_pos]
        return None

    def syntax_error(self):
        print("Syntactic error at " + str(self.curr_pos)+". Tree so far:")
        return None

    def parse(self):
        if self.current_token() is None: # no input no tree
            return None
        return self.parse_S() # if input return

    def parse_S(self):
        ast = ASTNode("S")
        ast.add_child(self.parse_A())  # Parse block A
        #ast.add_child(self.parse_B())  # Parse block B
        return ast

    def parse_A(self):
        ast = ASTNode("A")
        if self.current_token() is not None and self.current_token()[1] in days:
            ast.add_child(ASTNode('WD',self.current_token()[1]))
            self.curr_pos += 1
            if self.current_token() is not None and self.current_token()[1]=="{":
                ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
                self.curr_pos += 1
                ast.add_child(self.parse_SCH())
                #self.curr_pos += 1
                if self.current_token() is not None and self.current_token()[1]=="}":
                    ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
                    self.curr_pos += 1
                    ast.add_child(self.parse_A())
                    return ast
                else:
                    self.syntax_error()
            else:
                self.syntax_error()
        else:
            return None

    def parse_SCH(self):
        ast = ASTNode("SCH")
        if self.current_token() is not None and self.current_token()[0] == 'Literal':
            ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1])) # add the triggering literal
            self.curr_pos+=1
            if self.current_token() is not None and self.current_token()[1] == "=":
                ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
                self.curr_pos += 1
                if self.current_token() is not None and (self.current_token()[0] =="Time" or self.current_token()[1] =="CONT"):
                    ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
                    self.curr_pos += 1
                    if self.current_token() is not None and self.current_token()[1] == "-":
                        ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
                        self.curr_pos += 1
                        if self.current_token() is not None and self.current_token()[0] =="Time":
                            ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
                            self.curr_pos += 1
                            if self.current_token() is not None and self.current_token()[1] == ";":
                                ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
                                self.curr_pos += 1
                                ast.add_child(self.parse_SCH())
                                return ast
                            else:
                                self.syntax_error()
                        else:
                            self.syntax_error()
                    else:
                        self.syntax_error()
            else:
                self.syntax_error()
        else:
            return None

input_program = input("Please enter something: ")
lexer(input_program)

#uncomment to test out lexer
"""
for token in tokens:
    print("<" + token[0] + ", \"" + token[1] + "\">")
"""
parser = Parser(tokens)
ast = parser.parse()
if ast:
    print(ast)