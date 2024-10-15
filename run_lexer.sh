#!/bin/bash

#make surd python is installed - included in README
# python3 -m venv venv
# source venv/bin/activate

# Compile the scanner
gcc -o lexer lexer.c

python scanner.py

echo "Lexer executed. Enter input to tokenize."
