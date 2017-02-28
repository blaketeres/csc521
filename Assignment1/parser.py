import sys
import re

specialCases = ["=-", "+-", "--", "*-", "/-", "^-", "-N", "(-", ")-"]

parseTreeInput = []
currentIndex = 0
parserOutput = ["Program"]
print(parserOutput)

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
    "NameList": [["Name", "@COMMA", "NameList"], ["Name"]],
    "ParameterList": [["Parameter", "@COMMA", "ParameterList"], ["Parameter"]],
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
    def addToTree(x):
        if len(x) > 1:
            if isinstance(x[-1], list):
                addToTree(x[-1])
        else:
            x.append(temp)
            parserOutput[:1].append(x)
            print(parserOutput)
            return

    if secondItem != None:
        temp = [item, str(secondItem)]
    else:
        temp = [item]
    if len(parserOutput) == 1:
        parserOutput.append(temp)
        return
    addToTree(parserOutput)
    return


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
        checkStatement()

        # This may need to be changed to parseTreeInput[currentIndex + 1]
        if parseTreeInput[currentIndex] != "EOF":
            checkProgram()
        else:
            print("Finished Parsing")

    def checkStatement():
        global currentIndex
        addToParseTree("Statement")
        print(parserOutput)

        function = checkFunctionDeclaration()
        if function:
            return
        assignment = checkAssignment()
        if assignment:
            return
            '''
        beginAssignment = re.match("IDENT:.+", parseTreeInput[currentIndex])
        if beginAssignment:
            currentIndex += 1
            findTreeValue(parseTreeInput, currentIndex, "Assignment")
            return
            '''

        xPrint = checkPrint()
        if xPrint:
            return
        else:
            print("Syntax Error")
            exit()

    def checkFunctionDeclaration():
        global currentIndex
        if parseTreeInput[currentIndex] == "FUNCTION":
            currentIndex += 1
        else:
            return False
        addToParseTree("Function Declaration")
        checkName()
        checkFunctionParams()
        if parseTreeInput[currentIndex] == "LBRACE":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
        else:
            print("Missing left brace after function declaration")
            exit()
        checkFunctionBody()
        if parseTreeInput[currentIndex] == "RBRACE":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
        else:
            print("Missing right brace after function declaration")
            exit()
        return True

    def checkFunctionParams():
        global currentIndex
        if parseTreeInput[currentIndex] == "LPAREN":
            addToParseTree(str(parseTreeInput[currentIndex]))
            currentIndex += 1

            ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
            if ident:
                checkNameList()
        else:
            print("Missing Left Parentheses")
            exit()

        if parseTreeInput[currentIndex] == "RPAREN":
            addToParseTree(str(parseTreeInput[currentIndex]))
            currentIndex += 1
            return
        else:
            print("Missing Right Parentheses")
            exit()

    def checkFunctionBody():
        global currentIndex
        if parseTreeInput[currentIndex] == "RETURN":
            addToParseTree("Return")
            currentIndex += 1
            checkReturn()
            return
        checkProgram()
        checkReturn()
        return

    def checkReturn():
        global currentIndex
        addToParseTree(str(parseTreeInput[currentIndex]))
        checkParameterList()
        return

    def checkAssignment():
        global currentIndex
        single = checkSingleAssignment()
        if single:
            return True
        multiple = checkMultipleAssignment()
        if multiple:
            return True
        else:
            return False

    def checkSingleAssignment():
        global currentIndex
        if parseTreeInput[currentIndex] == "VAR":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
            checkName()
            if parseTreeInput[currentIndex] == "ASSIGN":
                addToParseTree(parseTreeInput[currentIndex])
                currentIndex += 1
                checkExpression()
                return True
            else:
                print("Assignment error")
                return False
        else:
            print("Missing 'var' identifier1")
            return False

    def checkMultipleAssignment():
        global currentIndex
        if parseTreeInput[currentIndex] == "VAR":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
            checkNameList()
            if parseTreeInput[currentIndex] == "ASSIGN":
                addToParseTree(parseTreeInput[currentIndex])
                currentIndex += 1
                checkFunctionCall()
                return True
            else:
                print("Assignment error3")
                return False
        else:
            print("Missing 'var' identifier2")
            return False

    def checkPrint():
        global currentIndex
        if parseTreeInput[currentIndex] == "PRINT":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
            checkExpression()
            return True
        else:
            return False

    def checkNameList():
        global currentIndex
        name = checkName()
        if name:
            if parseTreeInput[currentIndex] == "COMMA":
                addToParseTree(parseTreeInput[currentIndex])
                currentIndex += 1
                name2 = checkNameList()
                if name2:
                    return True
                else:
                    print("Extraneous comma")
                    return False
            else:
                return True
        else:
            print("Namelist error")
            return False

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
            addToParseTree(str(parseTreeInput[currentIndex]))
            currentIndex += 1
            return True
        if parseTreeInput == "SUB" or parseTreeInput == "ADD":
            addToParseTree(str(parseTreeInput[currentIndex]))
            currentIndex += 1
            ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
            if ident:
                addToParseTree(str(parseTreeInput[currentIndex]))
                return True
            else:
                print("Name Error1")
                return False
        print("Name Error2")
        return False

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
