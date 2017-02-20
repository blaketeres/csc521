import sys
import re
import json

def ReadInput():
    lines = sys.stdin.readlines()
    for line in lines:
        x = str(line)
        y = re.findall("var |function |return |print |=|\+|\-|\*|/|\^|\(|\)|\{|\}|,|:|[+-]?\d+(?:\.\d+)?|[a-zA-Z]+[a-zA-Z0-9_]*", x)
        for lexeme in y:
            #print (lexeme)
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
            else:
                number = re.fullmatch("[+-]?\d+(?:\.\d+)?", lexeme)
                if number:
                    print("NUMBER:" + lexeme)
                    continue
                ident = re.fullmatch("[a-zA-Z]+[a-zA-Z0-9_]*", lexeme)
                if ident:
                    print("IDENT:" + lexeme)
                    continue
                else:
                    print("Syntax Error")
                    exit()



if __name__ == '__main__':
    ReadInput()
