import sys
import re
import json

def ReadInput():
    # get input from quirk file
    lines = sys.stdin.readlines()

    # loop through lines in quirk file
    for i, line in enumerate(lines):

        # convert input from line to standard python string
        x = str(line)

        # filter out obvious errors by checking for illegal characters not defined in the grammar
        syntaxError = re.match("^((?!var |function |return |print |=|\+|\-|\*|/|\^|\(|\)|\{|\}|,|:|[+-]?\d+(?:\.\d+)?|[a-zA-Z]+[a-zA-Z0-9_]*).)*$", x)
        if syntaxError:
            print("Syntax Error")
            exit()

        # find keywords in grammar
        y = re.findall("var |function |return |print |=|\+|\-|\*|/|\^|\(|\)|\{|\}|,|:|[+-]?\d+(?:\.\d+)?|[a-zA-Z]+[a-zA-Z0-9_]*", x)

        # iterate through and find matches, then output them for the parser
        # use "continue" to break loop as soon as a match is found
        for lexeme in y:
            if lexeme == "var ":
                print("VAR")
                continue
            elif lexeme == "function ":
                print("FUNCTION")
                continue
            elif lexeme == "return ":
                print("RETURN")
                continue
            elif lexeme == "print ":
                print("PRINT")
                continue
            elif lexeme == "=":
                print("ASSIGN")
                continue
            elif lexeme == "+":
                print("ADD")
                continue
            elif lexeme == "-":
                print("SUB")
                continue
            elif lexeme == "*":
                print("MULT")
                continue
            elif lexeme == "/":
                print("DIV")
                continue
            elif lexeme == "^":
                print("EXP")
                continue
            elif lexeme == "(":
                print("LPAREN")
                continue
            elif lexeme == ")":
                print("RPAREN")
                continue
            elif lexeme == "{":
                print("LBRACE")
                continue
            elif lexeme == "}":
                print("RBRACE")
                continue
            elif lexeme == ",":
                print("COMMA")
                continue
            elif lexeme == ":":
                print("COLON")
                continue

            # handle numbers and strings after all keywords have been searched for
            else:
                number = re.fullmatch("[+-]?\d+(?:\.\d+)?", lexeme)
                if number:
                    print("NUMBER:" + lexeme)
                    continue
                ident = re.fullmatch("[a-zA-Z]+[a-zA-Z0-9_]*", lexeme)
                if ident:
                    print("IDENT:" + lexeme)
                    continue


if __name__ == '__main__':
    ReadInput()
