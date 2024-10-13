# PLT-project
Keywords: Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday | Style | CONT | heading_color | rose_pink  
Note: for now, we will only implement heading color and color value and add more if successful 
Literals: [A-Za-z0-9  ]+
Times: ([0-1][0-9] | 2[0-3]):[0-5][0-9]
Delimiters:  { | } | “ | ” | ;  
Operators: - | = | # 

Sample inputs that "work":
"Get Ready"= CONT-9:00;
Monday 12:30
Garfield ate a lasagna
Garfield ate a CONT lasagna
Style{heading_color=rose_pink;}


Things we need to fix:
- output format is (Type, Value) not <Type, Value>
- currently time is literally any <=5-char string comprised of numbers and ':' char
- not sure if this is something we need to fix, but there is no main "loop". You have to run program every time you want to try new input. 