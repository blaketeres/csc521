import sys
import re

specialCases = ["=-", "+-", "--", "*-", "/-", "^-", "-N", "(-", ")-"]

parseTreeInput = []
currentIndex = 0

# Grammar to use parser
# The @ symbol is a custom sybmol used to delineate quirk tokens from quirk grammar tree entries
# "|" branches have been replaced by nested lists
grammarDictionary = {
    "Program": [["Statement", "Program"], ["Statement"]],
    "Statement": [["FunctionDeclaration"], ["Assignment"], ["Print"]],
    "FunctionDeclaration": [["@FUNCTION", "Name", "FunctionParams", "@LBRACE", "FunctionBody", "@RBRACE"]],
    "FunctionParams": [["@LPAREN", "@RPAREN"], ["@LPAREN", "NameList" "@RPAREN"]],
    "FunctionBody": [["Return"], ["Program", "Return"]],
    "Return": [["@RETURN", "ParameterList"]],
    "Assignment": [["SingleAssignment"], ["MultipleAssignment"]],
    "SingleAssignment": [["@VAR", "Name", "@ASSIGN", "Expression"]],
    "MultipleAssignment": [["@VAR", "NameList", "@ASSIGN", "FunctionCall"]],
    "Print": [["@PRINT", "Expression"]],
    "NameList": [["Name"], ["Name", "@COMMA", "NameList"]],
    "ParameterList": [["Parameter"], ["Parameter", "@COMMA", "ParameterList"]],
    "Parameter": [["Name"], ["Expression"]],
    "Expression": [["Term"], ["Expression", "@ADD", "Term"], ["Expression", "@SUB", "Term"]],
    "Term": [["Factor"], ["Term", "@MULT", "Factor"], ["Term", "@DIV", "Factor"]],
    "Factor": [["SubExpression"], ["SubExpression", "@EXP", "Factor"], ["Value", "@EXP", "Factor"], ["Value"], ["FunctionCall"]],
    "FunctionCall": [["Name", "@LPAREN", "ParameterList", "@RPAREN"], ["Name", "@LPAREN", "ParameterList", "@RPAREN", "@COLON", "Number"]],
    "SubExpression": [["@LPAREN", "Expression", "@RPAREN"]],
    "Value": [["Name"], ["Number"]],
    "Name": [["@IDENT"], ["@SUB", "@IDENT"], ["@ADD", "@IDENT"]],
    "Number": [["@NUMBER"], ["@SUB", "@NUMBER"], ["@ADD", "@NUMBER"]]
}


# function to print tokens from grammar structure
def printLiteral(possibleLeafs):
    pattern = "@FUNCTION|@LBRACE|@RBRACE|@LPAREN|@RPAREN|@RETURN|@VAR|@ASSIGN|@PRINT|@COMMA|@ADD|@SUB|@MULT|@DIV|@EXP|@COLON|@IDENT|@NUMBER"
    for value in possibleLeafs:
        # handles branches which are represented above as nested lists
        if isinstance(value, list):
            for subItem in value:
                match = re.match(pattern, subItem)
                if match:
                    tokenToPrint = subItem[1:]
                    print(tokenToPrint)

# main parse tree. All decision making is handled below for each piece of grammar
def findTreeValue(parseTreeInput, currentIndex, dictEntry):
    def checkProgram():
        global currentIndex
        print("Program")
        findTreeValue(parseTreeInput, currentIndex, "Statement")

        # This may need to be changed to parseTreeInput[currentIndex + 1]
        if parseTreeInput[currentIndex] != "EOF":
            findTreeValue(parseTreeInput, currentIndex, "Program")
        else:
            print("Finished Parsing")

    def checkStatement():
        global currentIndex
        print("Statement")
        if parseTreeInput[currentIndex] == "FUNCTION":
            currentIndex += 1
            findTreeValue(parseTreeInput, currentIndex, "FunctionDeclaration")
            return
        beginAssignment = re.match("IDENT:.+", parseTreeInput[currentIndex])
        if beginAssignment:
            currentIndex += 1
            findTreeValue(parseTreeInput, currentIndex, "Assignment")
            return
        if parseTreeInput[currentIndex] == "PRINT":
            currentIndex += 1
            findTreeValue(parseTreeInput, currentIndex, "Print")
            return
        else:
            print("Syntax Error")
            exit()

    def checkFunctionDeclaration():
        global currentIndex
        print("Function Declaration")
        printLiteral(possibleLeafs)
        #if parseTreeInput[currentIndex] ==

    possibleLeafs = grammarDictionary[dictEntry]

    if dictEntry == "Program":
        checkProgram()
    elif dictEntry == "Statement":
        checkStatement()
    elif dictEntry == "FunctionDeclaration":
        checkFunctionDeclaration()
    elif dictEntry == "FunctionParams":
        pass
    elif dictEntry == "FunctionBody":
        pass
    elif dictEntry == "Return":
        pass
    elif dictEntry == "Assignment":
        pass
    elif dictEntry == "SingleAssignment":
        pass
    elif dictEntry == "MultipleAssignment":
        pass
    elif dictEntry == "Print":
        pass
    elif dictEntry == "NameList":
        pass
    elif dictEntry == "ParameterList":
        pass
    elif dictEntry == "Parameter":
        pass
    elif dictEntry == "Expression":
        pass
    elif dictEntry == "Term":
        pass
    elif dictEntry == "Factor":
        pass
    elif dictEntry == "FunctionCall":
        pass
    elif dictEntry == "SubExpression":
        pass
    elif dictEntry == "Value":
        pass
    elif dictEntry == "Name":
        pass
    elif dictEntry == "Number":
        pass
    else:
        pass

def ReadInput():

    parseTreeInput = []
    currentIndex = 0

    tokens = sys.stdin.readlines()

    # loop through lines in quirk file
    for token in tokens:
        # convert tokens to python string
        x = str(token)

        # remove extraneous \n
        y = x.replace("\n", "")
        parseTreeInput.append(y)

    findTreeValue(parseTreeInput, currentIndex, "Program")


if __name__ == '__main__':
    ReadInput()
