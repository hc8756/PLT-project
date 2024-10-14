# PLT-project
Team members: Anita Bui-Martinez (adb2221) and Ashley Cho (hc3455)

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

Detailed description of each step: <br/>



Things we need to fix: <br/>
- not sure if this is something we need to fix, but there is no main "loop". You have to run program every time you want to try new input. <br/>
