from constants import keywords

class Scanner:
    def __init__(self):
        self.temp="" # holds strings while they are being evaluated
        self.tokens=[]
        
    def transition_from_S0 (self, current_char):
        if current_char.isalpha() or current_char=='_':
            self.temp+=current_char
            return 'KEYWORD_OR_LITERAL'
        if current_char.isdigit(): #even if it turns out to be string later, try finding time
            self.temp += current_char
            return 'TIME'
        elif current_char in '{};':
            self.tokens.append(('Delimiter', current_char))
            self.temp = ""
            return 'S0'
        elif current_char in '-=#':
            self.tokens.append(('Operator', current_char))
            self.temp = ""
            return 'S0'
        elif current_char.isspace():
            return 'S0' # just ignore
        else:
            return 'ERROR'
    
    def transition_from_S1(self, current_char):
        if current_char.isalpha() or current_char.isdigit() or current_char.isspace() or current_char=='_':
            self.temp += current_char
            for keyword in keywords:
                if keyword in self.temp: #if keyword is identified, add split self.temp into literal (may be nothing) and keyword and add both self.tokens
                    keyword_start = self.temp.find(keyword)
                    if(keyword_start>0):
                        self.tokens.append(("Literal", self.temp[:keyword_start]))
                    self.tokens.append(("Keyword", self.temp[ keyword_start:]))
                    self.temp = ""
                    return 'S0'
            else:
                return 'KEYWORD_OR_LITERAL'
        elif current_char in '{};':
            self.tokens.append(('Literal', self.temp))
            self.tokens.append(('Delimiter', current_char))
            self.temp = ""
            return 'S0'
        elif current_char in '-=#':
            self.tokens.append(('Literal', self.temp))
            self.tokens.append(('Operator', current_char))
            self.temp = ""
            return 'S0'
        else:
            return 'ERROR'
    
    def transition_from_S2 (self, current_char):
        if current_char.isalpha() or current_char.isspace() or current_char=='_':
            self.temp += current_char # we thought it might be time, but it's a keyword or literal now
            return 'KEYWORD_OR_LITERAL'
        if current_char.isdigit() or current_char==':': # right now any <=4-char combination of numbers and ':'
            self.temp += current_char
            if len(self.temp) == 5:
                hours = self.temp[:2]
                minutes = self.temp[3:]
                if hours.isdigit() and minutes.isdigit(): 
                    if 0 <= int(hours) <= 23 and 0 <= int(minutes) <= 59:
                        self.tokens.append(('Time', self.temp))
                        self.temp = ""
                        return 'S0'
            return 'TIME'
        elif current_char in '{};':
            self.tokens.append(('Time', self.temp))
            self.tokens.append(('Delimiter', current_char))
            self.temp = ""
            return 'S0'
        elif current_char in '-=#':
            self.tokens.append(('Time', self.temp))
            self.tokens.append(('Operator', current_char))
            self.temp = ""
            return 'S0'
        else:
            return 'ERROR'
    
    def lexer(self, input_program):
        current_state = 'S0'
        current_position=0
        while current_position < len(input_program): # for each char of the program
            current_char = input_program[current_position]
            if current_state == 'S0':
                current_state=self.transition_from_S0(current_char)
            elif current_state == 'KEYWORD_OR_LITERAL': # S1 in function naming convention
                current_state=self.transition_from_S1(current_char)
            elif current_state == 'TIME': # S2 in function naming convention
                current_state=self.transition_from_S2(current_char)
            elif current_state == 'ERROR':
                print('Unrecognized character at position ' + str(current_position))
                break
            current_position += 1
        if self.temp: # anything left in self.temp at this point would be literal
            self.tokens.append(('Literal', self.temp))
        return self.tokens
    
    
    
