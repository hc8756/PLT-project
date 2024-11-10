from constants import days, elements, values

# Boilerplate code for creating and printing nodes of tree
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
        raise Exception(f"Syntactic error at {self.curr_pos}.")

    def parse(self):
        if self.current_token() is None: # no input no tree
            return None
        return self.parse_S() # if input return

    def parse_S(self):
        ast = ASTNode("S")
        ast.add_child(self.parse_A())  # Parse block A
        ast.add_child(self.parse_B())  # Parse block B
        self.curr_pos += 1 # Make sure there isn't anything after
        if self.current_token() is not None:
            self.syntax_error()
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
                                ast.add_child(self.parse_C())
                                return ast
                            else:
                                self.syntax_error()
                        else:
                            self.syntax_error()
                    else:
                        self.syntax_error()
            else:
                self.syntax_error()

    def parse_COM(self):
        ast = ASTNode("COM")
        if self.current_token() is not None and self.current_token()[1] == '#':
            ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
            self.curr_pos+=1
            if self.current_token() is not None and self.current_token()[0] == "Literal":
                ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
                self.curr_pos += 1
                ast.add_child(self.parse_C())
                return ast
            else:
                self.syntax_error()

    #return result of parse_SCH, parse_COM, or nothing depending on first of input
    def parse_C(self):
        if self.current_token() is not None and self.current_token()[1] == '#':
            return self.parse_COM()
        elif self.current_token() is not None and self.current_token()[0] == 'Literal':
            return self.parse_SCH()
        else:
            return None

    def parse_B(self):
        ast = ASTNode("B")
        if self.current_token() is None:
            return None
        if self.current_token()[1] == "Style":
            ast.add_child(ASTNode(self.current_token()[0],self.current_token()[1]))
            self.curr_pos += 1
            if self.current_token() is not None and self.current_token()[1]=="{":
                ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
                self.curr_pos += 1
                ast.add_child(self.parse_ST())
                if self.current_token() is not None and self.current_token()[1]=="}":
                    ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
                    return ast
                else:
                    self.syntax_error()
            else:
                self.syntax_error()
        else:
            self.syntax_error()

    def parse_ST(self):
        ast = ASTNode("ST")
        if self.current_token() is not None and self.current_token()[1] in elements:
            ast.add_child(ASTNode('EL',self.current_token()[1]))
            self.curr_pos += 1
            if self.current_token() is not None and self.current_token()[1]=="=":
                ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
                self.curr_pos += 1
                if self.current_token() is not None and self.current_token()[1] in values:
                    ast.add_child(ASTNode('VAL', self.current_token()[1]))
                    self.curr_pos += 1
                    if self.current_token() is not None and self.current_token()[1]==";":
                        ast.add_child(ASTNode(self.current_token()[0], self.current_token()[1]))
                        self.curr_pos += 1
                        ast.add_child(self.parse_ST())
                        return ast
                    else:
                        self.syntax_error()
                else:
                    self.syntax_error()
            else:
                self.syntax_error()
        else:
            return None