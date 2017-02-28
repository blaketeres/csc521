import sys
import re

specialCases = ["=-", "+-", "--", "*-", "/-", "^-", "-N", "(-", ")-"]

parseTreeInput = []
currentIndex = 0
parserOutput = ["Program"]

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

def addToParseTree(item, secondItem = None):
    def doThis():
        if len(parserOutput) > 1:
            parserOutput[-1].append(temp)
        else:
            parserOutput.append(temp)
        return

    if secondItem != None:
        temp = [item, str(secondItem)]
        doThis()
    else:
        temp = [item]
        doThis()



# function to print tokens from grammar structure
def getLiteral(possibleLeafs):
    output = []
    pattern = "@FUNCTION|@LBRACE|@RBRACE|@LPAREN|@RPAREN|@RETURN|@VAR|@ASSIGN|@PRINT|@COMMA|@ADD|@SUB|@MULT|@DIV|@EXP|@COLON|@IDENT|@NUMBER"
    for value in possibleLeafs:
        # handles branches which are represented above as nested lists
        if isinstance(value, list):
            for subItem in value:
                match = re.match(pattern, subItem)
                if match:
                    tokenToPrint = subItem[1:]
                    output.append(tokenToPrint)
    return output

# main parse tree. All decision making is handled below for each piece of
# grammar
def findTreeValue(parseTreeInput, currentIndex, dictEntry):
    def checkProgram():
        global currentIndex
        print(parserOutput)
        findTreeValue(parseTreeInput, currentIndex, "Statement")

        # This may need to be changed to parseTreeInput[currentIndex + 1]
        if parseTreeInput[currentIndex] != "EOF":
            findTreeValue(parseTreeInput, currentIndex, "Program")
        else:
            print("Finished Parsing")

    def checkStatement():
        global currentIndex
        addToParseTree("Statement")
        print(parserOutput)
        if parseTreeInput[currentIndex] == "FUNCTION":
            currentIndex += 1
            findTreeValue(parseTreeInput, currentIndex, "FunctionDeclaration")
            return
        beginAssignment = re.match("IDENT:.+", parseTreeInput[currentIndex])
        if beginAssignment:
            currentIndex += 1
            findTreeValue(parseTreeInput, currentIndex, "Assignment")
            return
        elif parseTreeInput[currentIndex] == "PRINT":
            currentIndex += 1
            findTreeValue(parseTreeInput, currentIndex, "Print")
            return
        else:
            print("Syntax Error")
            exit()

    def checkFunctionDeclaration():
        global currentIndex
        #tokens = getLiteral(possibleLeafs)
        findTreeValue(parseTreeInput, currentIndex, "Name")
        currentIndex += 1
        if parseTreeInput[currentIndex] == "LPAREN":
            addToParseTree(str(parseTreeInput[currentIndex]))
            currentIndex += 1
            findTreeValue(parseTreeInput, currentIndex, "FunctionParams")
            if parseTreeInput[currentIndex] == "LBRACE":
                currentIndex += 1
                addToParseTree(str(parseTreeInput[currentIndex]))
                findTreeValue(parseTreeInput, currentIndex, "FunctionBody")
                if parseTreeInput[currentIndex] == "RBRACE":
                    currentIndex += 1
                    addToParseTree(str(parseTreeInput[currentIndex]))
                    return
                else:
                    print("Missing right brace")
                    exit()
            else:
                print("Missing left brace")
                exit()
        else:
            print("Missing parentheses after function declaration")
            exit()

    def checkFunctionParams():
        global currentIndex
        #tokens = getLiteral(possibleLeafs)
        addToParseTree(str(parseTreeInput[currentIndex]))
        print(parserOutput)
        if parseTreeInput[currentIndex] == "RPAREN":
            currentIndex += 1
            return
        ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
        if ident:
            currentIndex += 1
            findTreeValue(parseTreeInput, currentIndex, "NameList")
        else:
            print("Syntax Error")
            exit()

    def checkFunctionBody():
        global currentIndex

        print("2")

    def checkReturn():
        global currentIndex
        print("3")

    def checkAssignment():
        global currentIndex
        print("4")

    def checkSingleAssignment():
        global currentIndex
        print("5")

    def checkMultipleAssignment():
        global currentIndex
        print("6")

    def checkPrint():
        global currentIndex
        print("7")

    def checkNameList():
        global currentIndex
        print("8")

    def checkParameterList():
        global currentIndex
        print("Function 9")

    def checkParameter():
        global currentIndex
        print("Function 10")

    def checkExpression():
        global currentIndex
        print("Function 11")

    def checkTerm():
        global currentIndex
        print("Function 12")

    def checkTerm():
        global currentIndex
        print("Function 13")

    def checkFactor():
        global currentIndex
        print("Function 14")

    def checkFunctionCall():
        global currentIndex
        print("Function 15")

    def checkSubExpression():
        global currentIndex
        print("Function 16")

    def checkValue():
        global currentIndex
        print("Function 17")

    def checkName():
        global currentIndex
        ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
        if ident:
            addToParseTree("Function Declaration", str(parseTreeInput[currentIndex]))
            print(parserOutput)
            return
        if parseTreeInput == "SUB" or parseTreeInput == "ADD":
            currentIndex += 1
            addToParseTree(str(parseTreeInput[currentIndex]))
            ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
            if ident:
                addToParseTree(str(parseTreeInput[currentIndex]))
                return
            else:
                print("Syntax Error")
                exit()

    def checkNumber():
        global currentIndex
        print("Function 19")

    possibleLeafs = grammarDictionary[dictEntry]

    if dictEntry == "Program":
        checkProgram()
    elif dictEntry == "Statement":
        checkStatement()
    elif dictEntry == "FunctionDeclaration":
        checkFunctionDeclaration()
    elif dictEntry == "FunctionParams":
        checkFunctionParams()
    elif dictEntry == "FunctionBody":
        checkFunctionBody()
    elif dictEntry == "Return":
        checkReturn()
    elif dictEntry == "Assignment":
        checkAssignment()
    elif dictEntry == "SingleAssignment":
        checkSingleAssignment()
    elif dictEntry == "MultipleAssignment":
        checkMultipleAssignment()
    elif dictEntry == "Print":
        checkPrint()
    elif dictEntry == "NameList":
        checkNameList()
    elif dictEntry == "ParameterList":
        checkParameterList()
    elif dictEntry == "Parameter":
        checkParameter()
    elif dictEntry == "Expression":
        checkExpression()
    elif dictEntry == "Term":
        checkTerm()
    elif dictEntry == "Factor":
        checkFactor
    elif dictEntry == "FunctionCall":
        checkFunctionCall()
    elif dictEntry == "SubExpression":
        checkSubExpression()
    elif dictEntry == "Value":
        checkValue()
    elif dictEntry == "Name":
        checkName()
    elif dictEntry == "Number":
        checkNumber()
    else:
        print("BOY YOU GOT SOMETHING WRONG")


def ReadInput():

    global output
    tokens = sys.stdin.readlines()

    # loop through lines in quirk file
    for token in tokens:
        # convert tokens to python string
        x = str(token)

        # remove extraneous \n
        y = x.replace("\n", "")
        parseTreeInput.append(y)

    findTreeValue(parseTreeInput, currentIndex, "Program")
    print(parserOutput)


if __name__ == '__main__':
    ReadInput()
