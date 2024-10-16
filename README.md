# PLT-project

## Team members: Anita Bui-Martinez (adb2221) and Ashley Cho (hc3455)

## To run: 
make sure python is installed <br/>
run `python scanner.py`
or run the shell script
`./run_lexer.sh`

Lexical Grammar: <br/>
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
