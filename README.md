# PLT-project

## Team members: Anita Bui-Martinez (adb2221) and Ashley Cho (hc3455)

### To run: 
Ensure python is installed <br/>
You can do this on Windows or Mac by downloading from: https://www.python.org/downloads/ <br/> 
run `python scanner.py`
or run the shell script
`./run_lexer.sh`

### Lexical Grammar: <br/>
Keywords: Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday | Style | CONT | heading_color | rose_pink <br/>  
Note: for now, we will only implement heading color and color value and add more if successful <br/>
Literals: [A-Za-z0-9  ]+ <br/>
Times: ([0-1][0-9] | 2[0-3]):[0-5][0-9] <br/>
Delimiters:  { | } | “ | ” | ;  <br/>
Operators: - | = | # <br/>

Sample inputs that work: <br/>
"Get Ready"= CONT-9:00; <br/>

```
<Delimiter, """> 
<Literal, "Get Ready">
<Delimiter, """>
<Operator, "=">
<Keyword, "CONT">
<Operator, "-">
<Time, "9:00">
<Delimiter, ";">
```

Monday 12:30 <br/>

```
<Keyword, "Monday">
<Time, "12:30">
```

Garfield ate a lasagna <br/>

```
<Literal, "Garfield ate a lasagna">
```

Garfield ate a CONT lasagna <br/>

```
<Literal, "Garfield ate a ">
<Keyword, "CONT">
<Literal, "lasagna">
```

Style{heading_color=rose_pink;} <br/>

```
<Keyword, "Style">
<Delimiter, "{">
<Keyword, "heading_color">
<Operator, "=">
<Keyword, "rose_pink">
<Delimiter, ";">
<Delimiter, "}">
```
12@30 

```
Unrecognized character. We are at position 3
<Literal, "12">
```

## Description of each step: <br/>

The lexer uses a state machine with different states (S0, KEYWORD_OR_LITERAL, TIME, ERROR) to process the input. Each state defines a specific behavior based on the character being read:

S0 (Initial State):
The lexer starts in state S0 and reads each character from the input.
If it reads an alphabetic character or an underscore (_), it transitions to KEYWORD_OR_LITERAL and starts collecting characters for a possible keyword or literal.
If it reads a digit, it transitions to the TIME state and begins parsing a time token.
If it reads a delimiter or operator, it directly appends the token to the tokens list and remains in state S0.
If an unrecognized character is encountered, it transitions to the ERROR state.

KEYWORD_OR_LITERAL (S1):
This state evaluates whether the current characters form a keyword or a literal.
If a keyword is found within the collected string, it splits the string into a literal (if any) and the keyword, appending both to the tokens list.
If no keyword is found, it continues appending characters until a delimiter, operator, or space is encountered, at which point the collected string is assumed to be a literal.

TIME (S2):
This state attempts to parse a valid time in the format HH:MM.
It checks if the characters form a valid hour and minute combination. If they do, it appends the token as Time. If the characters do not match the time format, it transitions back to KEYWORD_OR_LITERAL since the digits could be part of a literal instead.
ERROR:

When the lexer encounters an unrecognized character, it moves to the ERROR state and prints an error message indicating the position of the problematic character in the input. This halts further processing.

After appending tokens it outputs them along with their token type. 

# Programming Assignment 2 

## To run:
### Requirements 
- Python 3 or above

### Installation and Running 
Clone repository and cd into it.
run 
```
python main.py
```
Enter input to test.

Alternatively, you can run the shell script:
./run_parser.sh

## Our CFG
### Non-terminals:
S: Start <br/>
A: Block(s) defining day and its schedule <br/>
B: Block defining style <br/>
SCH: a day’s schedule <br/>
COM: comment <br/>
C: non-terminal that follows a line of schedule. <br/>
ST: stylistic element-value pair(s) <br/>

### Terminals would be keywords, literals, times, delimiters, and operators defined in assignment 1. 
For brevity following abbreviations are used in grammar below… <br/>
WD: terminal keywords <br/>
LIT: terminal literals <br/>
TIME: terminal times <br/>
EL: stylistic element <br/>
VAL: stylistic value <br/>
<br/>
S→AB <br/>
A→WD{SCH}A | ε <br/>
SCH→LIT=CONT-TIME;C | LIT=TIME-TIME;C <br/>
COM→ #LITC <br/>
C→SCH | COM | ε //this pattern ensures that comment always comes after a schedule <br/>
B→Style{ST} | ε //if B is null, we can default style <br/>
ST→EL=VAL;ST | ε <br/>


## Sample Input Programs 

### Example of correct test case:
Monday{whatever=8:00-9:00;whatever=CONT-10:00;}Tuesday{whatever=8:00-9:00;whatever=CONT-10:00;#take out laundry today # do not forget to separate dark and white } Wednesday{whatever=8:00-9:00;whatever=CONT-10:00;}Style{heading_color=rose_pink;heading_color=rose_pink;}

Expected AST: 
```
S: 
  A:
    WD: Monday
    Delimiter: {
    SCH:
      Literal: whatever
      Operator: =
      Time: 8:00
      Operator: -
      Time: 9:00
      Delimiter: ;
      SCH:
        Literal: whatever
        Operator: =
        Keyword: CONT
        Operator: -
        Time: 10:00
        Delimiter: ;
    Delimiter: }
    A:
      WD: Tuesday
      Delimiter: {
      SCH:
        Literal: whatever
        Operator: =
        Time: 8:00
        Operator: -
        Time: 9:00
        Delimiter: ;
        SCH:
          Literal: whatever
          Operator: =
          Keyword: CONT
          Operator: -
          Time: 10:00
          Delimiter: ;
          COM:
            Operator: #
            Literal: take out laundry today
            COM:
              Operator: #
              Literal: do not forget to separate dark and white
      Delimiter: }
      A:
        WD: Wednesday
        Delimiter: {
        SCH:
          Literal: whatever
          Operator: =
          Time: 8:00
          Operator: -
          Time: 9:00
          Delimiter: ;
          SCH:
            Literal: whatever
            Operator: =
            Keyword: CONT
            Operator: -
            Time: 10:00
            Delimiter: ;
        Delimiter: }
  B:
    Keyword: Style
    Delimiter: {
    ST:
      EL: heading_color
      Operator: =
      VAL: rose_pink
      Delimiter: ;
      ST:
        EL: heading_color
        Operator: =
        VAL: rose_pink
        Delimiter: ;
    Delimiter: }
```

### Example of test case that would throw syntax error:
Monday{whatever=8:00-9:00;whatever=CONT-CONT;}Tuesday{whatever=8:00-9:00;whatever=CONT-10:00;#take out laundry today # do not forget to separate dark and white } Wednesday{whatever=8:00-9:00;whatever=CONT-10:00;}
//second time cannot be CONT.
```
Syntactic error at 12.
```

### Another sample of correct input:
Thursday{lecture=9:00-10:30;study=CONT-12:00;# Complete homework}
```
S:
  A:
    WD: Thursday
    Delimiter: {
    SCH:
      Literal: lecture
      Operator: =
      Time: 9:00
      Operator: -
      Time: 10:30
      Delimiter: ;
      SCH:
        Literal: study
        Operator: =
        Keyword: CONT
        Operator: -
        Time: 12:00
        Delimiter: ;
        COM:
          Operator: #
          Literal: Complete homework
    Delimiter: }
```

### Example of another error - missing semicolon: 
Friday{task1=8:00-9:00 task2=10:00-11:00;}Style{font_color=red;}
```
Syntactic error at 6.
```

### Example of correct input - nexted schedule and multiple comments: 
Tuesday{meeting=10:00-11:00;work=11:00-12:00;# Prepare slides # Check projector}Style{heading_color=rose_pink;} 
```
S:
  A:
    WD: Tuesday
    Delimiter: {
    SCH:
      Literal: meeting
      Operator: =
      Time: 10:00
      Operator: -
      Time: 11:00
      Delimiter: ;
      SCH:
        Literal: work
        Operator: =
        Time: 11:00
        Operator: -
        Time: 12:00
        Delimiter: ;
        COM:
          Operator: #
          Literal: Prepare slides
          COM:
            Operator: #
            Literal: Check projector
    Delimiter: }
  B:
    Keyword: Style
    Delimiter: {
    ST:
      EL: heading_color
      Operator: =
      VAL: rose_pink
      Delimiter: ;
    Delimiter: }
```

