# PLT-project

# Programming Assignment 3 

## Team members: Anita Bui-Martinez (adb2221) and Ashley Cho (hc3455)

### Requirements 
- Python 3 or above

### Installation and Running 
Clone repository and cd into it.
Run 
```
python test.py
```
Enter input to test.

Alternatively, you can run the shell script:
```
.\run_generator.sh
```

## Sample Input Programs

### Correct Test Case
Monday{work=9:00-11:00;study=CONT-1:00;} Style{heading_color=rose_pink;}

Expected output.html: 
```
<!DOCTYPE html>
    <html>
    <head>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed
            }
            th {
                text-align: left;
                padding: 10px;
                border: 1px solid black;
            }
            td {
                padding: 8px;
                border: 1px solid black;     
            }
            tr {
                display: table-row;
            }
              
        </style>
    </head>
    <body>
        <table><tr><th colspan='2'>Monday</th></tr><tr><td>9:00-11:00</td><td>work</td></tr><tr><td>11:00-1:00</td><td>study</td></tr></table><br>
    </body>
    </html>
```

### Correct Test Case: multiple comments 
Tuesday{task=8:00-9:00;task=CONT-10:00;#first comment #nested comment inside}

Expected output.html: 
```
<!DOCTYPE html>
    <html>
    <head>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed
            }
            th {
                text-align: left;
                padding: 10px;
                border: 1px solid black;
            }
            td {
                padding: 8px;
                border: 1px solid black;     
            }
            tr {
                display: table-row;
            }
              
        </style>
    </head>
    <body>
        <table><tr><th colspan='2'>Tuesday</th></tr><tr><td>8:00-9:00</td><td>task</td></tr><tr><td>9:00-10:00</td><td>task<br><span style='color: gray; font-size: smaller;'>first comment </span><br><span style='color: gray; font-size: smaller;'>nested comment inside</span></td></tr></table><br>
    </body>
    </html>
```

### Correct Test Case: multiple days
Monday{work=9:00-11:00;study=CONT-1:00;}Tuesday{work=12:00-5:00;family time=CONT-8:00;}

Expected output.html: 
```
<!DOCTYPE html>
    <html>
    <head>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed
            }
            th {
                text-align: left;
                padding: 10px;
                border: 1px solid black;
            }
            td {
                padding: 8px;
                border: 1px solid black;     
            }
            tr {
                display: table-row;
            }
              
        </style>
    </head>
    <body>
        <table><tr><th colspan='2'>Monday</th></tr><tr><td>9:00-11:00</td><td>work</td></tr><tr><td>11:00-1:00</td><td>study</td></tr></table><br><table><tr><th colspan='2'>Tuesday</th></tr><tr><td>12:00-5:00</td><td>work</td></tr><tr><td>5:00-8:00</td><td>family time</td></tr></table><br>
    </body>
    </html>
```

### Correct Test Case 
Monday{work=9:00-11:00;study=CONT-1:00;}Tuesday{work=12:00-5:00;family time=CONT-8:00;}Wednesday{meeting=10:00-12:00; #bring USB cord}

Expected output.html: 
```
<!DOCTYPE html>
    <html>
    <head>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed
            }
            th {
                text-align: left;
                padding: 10px;
                border: 1px solid black;
            }
            td {
                padding: 8px;
                border: 1px solid black;     
            }
            tr {
                display: table-row;
            }
              
        </style>
    </head>
    <body>
        <table><tr><th colspan='2'>Monday</th></tr><tr><td>9:00-11:00</td><td>work</td></tr><tr><td>11:00-1:00</td><td>study</td></tr></table><br><table><tr><th colspan='2'>Tuesday</th></tr><tr><td>12:00-5:00</td><td>work</td></tr><tr><td>5:00-8:00</td><td>family time</td></tr></table><br><table><tr><th colspan='2'>Wednesday</th></tr><tr><td>10:00-12:00</td><td>meeting<br><span style='color: gray; font-size: smaller;'>bring USB cord</span></td></tr></table><br>
    </body>
    </html>
```

### Incorrect Test Case 
Monday{work=9:00-11:00Tuesday{work=12:00-5:00;family time=CONT-8:00;}Wednesday{meeting=10:00-12:00; #bring USB cord}

Expected output (no html generated): 
```
Lexical Analysis...
Tokens: [('Keyword', 'Monday'), ('Delimiter', '{'), ('Literal', 'work'), ('Operator', '='), ('Time', '9:00'), ('Operator', '-'), ('Time', '11:00'), ('Keyword', 'Tuesday'), ('Delimiter', '{'), ('Literal', 'work'), ('Operator', '='), ('Time', '12:00'), ('Operator', '-'), ('Time', '5:00'), ('Delimiter', ';'), ('Literal', 'family time'), ('Operator', '='), ('Keyword', 'CONT'), ('Operator', '-'), ('Time', '8:00'), ('Delimiter', ';'), ('Delimiter', '}'), ('Keyword', 'Wednesday'), ('Delimiter', '{'), ('Literal', 'meeting'), ('Operator', '='), ('Time', '10:00'), ('Operator', '-'), ('Time', '12:00'), ('Delimiter', ';'), ('Operator', '#'), ('Literal', 'bring USB cord'), ('Delimiter', '}')]
Parsing...
Parsing Error: Syntactic error at 7.

```

## Code Generator Steps

CodeGenerator class takes ast passed as parameter and creates a html visualization. 

In the generate function, the ast is traversed. The results populate the styles and body_content strings which are inserted into html skeleton code.

The traverse function itself recursively traverses AST nodes. We designed our AST nodes to have types depending on their role in our CFG. We can now (recursively if necessary) traverse node type A to extract schedule information and node type B to extract style information.
Children are processed differently depending on their type. For example, if a child of type WD (weekday) is identified, a new table is added to the html body. Separate functions have been defined for children of type that require more complex processing.

The first of these would be the process_schedule function. This will parse out the tasks and their start and end times, adding them to the html body string as well. Any nested schedules will be recursively processed.
The extract_comments function will similarly parse out comments from nodes type COM and add to output with a different style.

Finally, the resulting html code is written to a file and opened on a browser in save_to_file and execute.
All these processes are triggered in the run_pipeline function.
### Demo Video:
https://cvn.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=3ac90d6c-cb02-4725-a0b1-b240017bea6c