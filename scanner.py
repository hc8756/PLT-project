temp = "" # holds strings while they are being evaluated
tokens=[]

def transition_from_S0 (current_char):
    global temp
    global tokens
    temp="" #always reset temp string from S0
    if current_char.isalpha():
        temp+=current_char
        return 'KEYWORD_OR_LITERAL'
    if current_char.isdigit(): #even if it turns out to be string later, try finding time
        temp += current_char
        return 'TIME'
    elif current_char in '{"}";':
        tokens.append(('Delimiter', current_char))
        return 'S0'
    elif current_char in '-=#':
        tokens.append(('Operator', current_char))
        return 'S0'
    elif current_char.isspace():
        return 'S0' # just ignore
    else:
        return 'ERROR'

def transition_from_S1(current_char):
    global temp
    global tokens
    if current_char.isalpha() or current_char.isdigit() or current_char.isspace():
        temp += current_char
        if  temp in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Style", "CONT", "heading_color", "rose_pink"]:
            tokens.append(('Keyword', temp))
            return 'S0'
        else:
            return 'KEYWORD_OR_LITERAL'
    elif current_char in '{"}";':
        tokens.append(('Literal', temp))
        tokens.append(('Delimiter', current_char))
        return 'S0'
    elif current_char in '-=#':
        tokens.append(('Literal', temp))
        tokens.append(('Operator', current_char))
        return 'S0'
    else:
        return 'ERROR'

def transition_from_S2 (current_char):
    global temp
    global tokens
    if current_char.isalpha():
        temp += current_char # we thought it might be time, but it's a keyword or literal now
        return 'KEYWORD_OR_LITERAL'
    if current_char.isdigit() or current_char==':': # right now any <=4-char combination of numbers and ':'
        temp += current_char
        if len(temp) >= 5:
            tokens.append(('Time', temp))
            return 'S0'
        return 'TIME'
    elif current_char in '{"}";':
        tokens.append(('Time', temp))
        tokens.append(('Delimiter', current_char))
        return 'S0'
    elif current_char in '-=#':
        tokens.append(('Time', temp))
        tokens.append(('Operator', current_char))
        return 'S0'
    else:
        return 'ERROR'

def lexer(input_program):
    global tokens
    tokens = []
    current_state = 'S0'
    current_position=0
    while current_position < len(input_program): #for each char of the program
        current_char = input_program[current_position]
        if current_state == 'S0':
            current_state=transition_from_S0(current_char)
        elif current_state == 'KEYWORD_OR_LITERAL': # S1 in function naming convention
            current_state=transition_from_S1(current_char)
        elif current_state == 'TIME': # S2 in function naming convention
            current_state=transition_from_S2(current_char)
        elif current_state == 'ERROR':
            print('Unrecognized character. We are at position ' + str(current_position))
            break
        current_position += 1

    return 0

input_program = input("Please enter something: ")
lexer(input_program)
for token in tokens:
    print(token)

