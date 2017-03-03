import sys
import re

specialCases = ["=-", "+-", "--", "*-", "/-", "^-", "-N", "(-", ")-"]

parseTreeInput = []
currentIndex = 0
parserOutput = [None]

# Grammar to use parser
# The @ symbol is a custom sybmol used to delineate quirk tokens from quirk grammar tree entries
# "|" branches have been replaced by nested lists
grammarDictionary = {
    "Program": [["Statement", "Program"], ["Statement"]],
    "Statement": [["FunctionDeclaration"], ["Assignment"], ["Print"]],
    "FunctionDeclaration": [["@FUNCTION", "Name", "@LPAREN", "FunctionParams", "@LBRACE", "FunctionBody", "@RBRACE"]],
    "FunctionParams": [["@RPAREN"], ["NameList", "@RPAREN"]],
    "FunctionBody": [["Return"], ["Program", "Return"]],
    "Return": [["@RETURN", "ParameterList"]],
    "Assignment": [["SingleAssignment"], ["MultipleAssignment"]],
    "SingleAssignment": [["@VAR", "Name", "@ASSIGN", "Expression"]],
    "MultipleAssignment": [["@VAR", "NameList", "@ASSIGN", "FunctionCall"]],
    "Print": [["@PRINT", "Expression"]],
    "NameList": [["Name", "@COMMA", "NameList"], ["Name"]],
    "ParameterList": [["Parameter", "@COMMA", "ParameterList"], ["Parameter"]],
    "Parameter": [["Expression"], ["Name"]],
    "Expression": [["Term", "@ADD", "Expression"], ["Term", "@SUB", "Expression"], ["Term"]],
    "Term": [["Factor", "@MULT", "Term"], ["Factor", "@DIV", "Term"], ["Factor"]],
    "Factor": [["SubExpression", "@EXP", "Factor"], ["SubExpression"], ["FunctionCall"], ["Value", "@EXP", "Factor"], ["Value"]],
    "FunctionCall": [["Name", "@LPAREN", "FunctionCallParams", "@COLON", "Number"], ["Name", "@LPAREN", "FunctionCallParams"]],
    "FunctionCallParams": [["@RPAREN"], ["ParameterList", "@RPAREN"]],
    "SubExpression": [["@LPAREN", "Expression", "@RPAREN"]],
    "Value": [["Name"], ["Number"]],
    "Name": [["@IDENT"], ["@SUB", "@IDENT"], ["@ADD", "@IDENT"]],
    "Number": [["@NUMBER"], ["@SUB", "@NUMBER"], ["@ADD", "@NUMBER"]]
}

def addToParseTree(item):
    def addToTree(x):
        if len(x) > 1:
            if isinstance(x[-1], list):
                addToTree(x[-1])
        else:
            x.append(temp)
            parserOutput[:1].append(x)
            #print(parserOutput)

    temp = [item]
    if len(parserOutput) == 1:
        parserOutput.append(temp)
        return
    addToTree(parserOutput)
    return


# function to print tokens from grammar structure
def isToken(parserOutputItem):
    pattern = "FUNCTION|LBRACE|RBRACE|LPAREN|RPAREN|RETURN|VAR|ASSIGN|PRINT|COMMA|ADD|SUB|MULT|DIV|EXP|COLON|IDENT:.+|NUMBER:.+"
    match = re.match(pattern, parserOutputItem)
    if match:
        return True
    return False

# main parse tree. All decision making is handled below for each piece of
# grammar

def checkProgram():
    global currentIndex
    if parserOutput[0] == None:
        parserOutput[0] = "Program"
    else:
        addToParseTree("Program")

    statement = checkStatement()
    if statement:
        program = checkProgram()
        if program:
            return True
        return True
    else:
        return False

def checkStatement():
    global currentIndex
    addToParseTree("Statement")
    function = checkFunctionDeclaration()
    if function:
        return True
    assignment = checkAssignment()
    if assignment:
        return True
    xPrint = checkPrint()
    if xPrint:
        return True
    return False

def checkFunctionDeclaration():
    global currentIndex
    if parseTreeInput[currentIndex] == "FUNCTION":
        addToParseTree(parseTreeInput[currentIndex])
        currentIndex += 1
        name = checkName()
        if name:
            ### currentIndex += 1
            if parseTreeInput[currentIndex] == "LPAREN":
                addToParseTree(parseTreeInput[currentIndex])
                currentIndex += 1
                functionParams = checkFunctionParams()
                if functionParams:
                    if parseTreeInput[currentIndex] == "LBRACE":
                        addToParseTree(parseTreeInput[currentIndex])
                        currentIndex += 1
                        functionBody = checkFunctionBody()
                        if functionBody:
                            if parseTreeInput[currentIndex] == "RBRACE":
                                addToParseTree(parseTreeInput[currentIndex])
                                currentIndex += 1
                                return True
                            else:
                                return False
                        else:
                            currentIndex -= 4
                            return False
                    else:
                        currentIndex -= 3
                        return False
                else:
                    currentIndex -= 3
                    return False
            else:
                currentIndex -= 2
                return False
        else:
            currentIndex -= 1
            return False
    return False

def checkFunctionParams():
    global currentIndex
    if parseTreeInput[currentIndex] == "RPAREN":
        addToParseTree(parseTreeInput[currentIndex])
        currentIndex += 1
        return True
    nameList = checkNameList()
    if nameList:
        if parseTreeInput[currentIndex] == "RPAREN":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
            return True
        else:
            return False
    return False

def checkFunctionBody():
    global currentIndex
    xReturn = checkReturn()
    if xReturn:
        return True
    program = checkProgram()
    if program:
        xReturn = checkReturn()
        if xReturn:
            return True
        else:
            return False
    return False

def checkReturn():
    global currentIndex
    if parseTreeInput[currentIndex] == "RETURN":
        addToParseTree(parseTreeInput[currentIndex])
        currentIndex += 1
        parameterList = checkParameterList()
        if parameterList:
            return True
        else:
            currentIndex -= 1
            return False
    return False

def checkAssignment():
    global currentIndex
    single = checkSingleAssignment()
    if single:
        return True
    multiple = checkMultipleAssignment()
    if multiple:
        return True
    return False

def checkSingleAssignment():
    global currentIndex
    if parseTreeInput[currentIndex] == "VAR":
        addToParseTree(parseTreeInput[currentIndex])
        currentIndex += 1
        name = checkName()
        if name:
            if parseTreeInput[currentIndex] == "ASSIGN":
                addToParseTree(parseTreeInput[currentIndex])
                currentIndex += 1
                expression = checkExpression()
                if expression:
                    return True
                else:
                    currentIndex -= 3
                    return False
            else:
                currentIndex -= 2
                return False
        else:
            currentIndex -= 1
            return False
    return False

def checkMultipleAssignment():
    global currentIndex
    if parseTreeInput[currentIndex] == "VAR":
        addToParseTree(parseTreeInput[currentIndex])
        currentIndex += 1
        nameList = checkNameList()
        if nameList:
            if parseTreeInput[currentIndex] == "ASSIGN":
                addToParseTree(parseTreeInput[currentIndex])
                currentIndex += 1
                functionCall = checkFunctionCall()
                if functionCall:
                    return True
                else:
                    currentIndex -= 3
                    return False
            else:
                currentIndex -= 2
                return False
        else:
            currentIndex -= 1
            return False
    return False

def checkPrint():
    global currentIndex
    if parseTreeInput[currentIndex] == "PRINT":
        addToParseTree(parseTreeInput[currentIndex])
        currentIndex += 1
        expression = checkExpression()
        if expression:
            return True
    return False

def checkNameList():
    global currentIndex
    name = checkName()
    if name:
        if parseTreeInput[currentIndex] == "COMMA":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
            nameList = checkNameList()
            if nameList:
                return True
            else:
                currentIndex -= 2
                return False
        return True
    return False

def checkParameterList():
    global currentIndex
    parameter = checkParameter()
    if parameter:
        if parseTreeInput[currentIndex] == "COMMA":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
            parameterList = checkParameterList()
            if parameterList:
                return True
            else:
                currentIndex -= 1
                return False
        return True
    return False

def checkParameter():
    global currentIndex
    expression = checkExpression()
    if expression:
        return True
    name = checkName()
    if name:
        return True
    return False

def checkExpression():
    global currentIndex
    term = checkTerm()
    if term:
        if parseTreeInput[currentIndex] == "ADD" or parseTreeInput[currentIndex] == "SUB":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
            expression = checkExpression()
            if expression:
                return True
            else:
                currentIndex -= 1
                return False
        return True
    return False

def checkTerm():
    global currentIndex
    factor = checkFactor()
    if factor:
        if parseTreeInput[currentIndex] == "MULT" or parseTreeInput[currentIndex] == "DIV":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
            term = checkTerm()
            if term:
                return True
            else:
                currentIndex -= 1
                return False
        return True
    return False

def checkFactor():
    global currentIndex
    subExpression = checkSubExpression()
    if subExpression:
        if parseTreeInput[currentIndex] == "EXP":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
            factor = checkFactor()
            if factor:
                return True
            else:
                currentIndex -= 1
                return False
        return True
    functionCall = checkFunctionCall()
    if functionCall:
        return True
    value = checkValue()
    if value:
        if parseTreeInput[currentIndex] == "EXP":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
            factor = checkFactor()
            if factor:
                return True
            else:
                currentIndex -= 1
                return False
        return True
    return False

def checkFunctionCall():
    global currentIndex
    name = checkName()
    if name:
        if parseTreeInput[currentIndex] == "LPAREN":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
            functionCallParams = checkFunctionCallParams()
            if functionCallParams:
                if parseTreeInput[currentIndex] == "COLON":
                    addToParseTree(parseTreeInput[currentIndex])
                    currentIndex += 1
                    number = checkNumber()
                    if number:
                        return True
                    else:
                        currentIndex -= 4
                        return False
                return True
            else:
                currentIndex -= 2
                return False
        else:
            currentIndex -= 1
            return False
    return False

def checkFunctionCallParams():
    global currentIndex
    if parseTreeInput[currentIndex] == "RPAREN":
        addToParseTree(parseTreeInput[currentIndex])
        currentIndex += 1
        return True
    parameterList = checkParameterList()
    if parameterList:
        if parseTreeInput[currentIndex] == "RPAREN":
            addToParseTree(parseTreeInput[currentIndex])
            currentIndex += 1
            return True
        else:
            return False
    return False

def checkSubExpression():
    global currentIndex
    if parseTreeInput[currentIndex] == "LPAREN":
        addToParseTree(parseTreeInput[currentIndex])
        currentIndex += 1
        expression = checkExpression()
        if expression:
            if parseTreeInput[currentIndex] == "RPAREN":
                addToParseTree(parseTreeInput[currentIndex])
                currentIndex += 1
                return True
            else:
                currentIndex -= 1
                return False
        else:
            currentIndex -= 1
            return False
    return False

def checkValue():
    global currentIndex
    name = checkName()
    if name:
        return True
    number = checkNumber()
    if number:
        return True
    return False

def checkName():
    global currentIndex
    ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
    if ident:
        addToParseTree(parseTreeInput[currentIndex])
        currentIndex += 1
        return True
    if parseTreeInput == "SUB" or parseTreeInput == "ADD":
        addToParseTree(parseTreeInput[currentIndex])
        currentIndex += 1
        ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
        if ident:
            addToParseTree(parseTreeInput[currentIndex])
            return True
        else:
            currentIndex -= 1
            return False
    return False

def checkNumber():
    global currentIndex
    number = re.match("NUMBER:.+", parseTreeInput[currentIndex])
    if number:
        addToParseTree(parseTreeInput[currentIndex])
        currentIndex += 1
        return True
    if parseTreeInput == "SUB" or parseTreeInput == "ADD":
        addToParseTree(parseTreeInput[currentIndex])
        currentIndex += 1
        number = re.match("NUMBER:.+", parseTreeInput[currentIndex])
        if number:
            addToParseTree(parseTreeInput[currentIndex])
            return True
        else:
            currentIndex -= 1
            return False
    return False

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

    validProgram = checkProgram()
    if validProgram:
        print(parserOutput)
        print("Valid quirk program")


if __name__ == '__main__':
    ReadInput()
