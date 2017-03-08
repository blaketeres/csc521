import sys
import re
import json

parseTreeInput = []
currentIndex = 0

# append subtree to immediate parent tree upon function returning True
# this will keep the order of the tree in tact, and eliminate incorrect leafs

'''
How My Parser Works:

Each function listed below traverses the grammar. Below are bits of code
that I use throughout the program and a small explanation. I am outlining
them here so that comments are not repetitive and chunky to read throughout.

global currentIndex:
    This keeps the index position from getting caught in a local context.

currentIndex (+-)= 1:
    Manually maintaining the token position. Will be incremented and
    decremented as needed, depending on the return values of the leaf
    node function calls.

grammarType = checkGrammarType():
    This function calls a child leaf in the grammar tree and returns a
    list consisting of a boolean value and the existing tree of the function
    that called it. This allows grammar to be checked, and the tree to maintain
    itself as the code traverses along.

if parseTreeInput[currentIndex] == "TOKEN":
    This checks to see if the token literal is in its correct position for
    the input quirk file to be accurate. If tokens are not found in their
    correct location, the program is found to have an error.

subTree = [SUBTREE CONTENTS]
    This creates the proper subtree to be returned if a branch is found
    to be successful.
'''

'''
The main parsing functions are found below. All decision making is handled below for each piece of
grammar. Every function below follows the same format, checking possible
leafs and returning True upon success, and False upon failure.
The program will exit if a possible path is not found before the
parser reaches the end of the input file
'''

def checkProgram():
    global currentIndex
    statement = checkStatement()
    if statement[0]:
        program = checkProgram()
        if program[0]:
            subTree = ["Program0", statement[1], program[1]]
            return[True, subTree]
        subTree = ["Program1", statement[1]]
        return [True, subTree]
    return [False, False]


def checkStatement():
    global currentIndex
    function = checkFunctionDeclaration()
    if function[0]:
        subTree = ["Statement0", function[1]]
        return [True, subTree]
    assignment = checkAssignment()
    if assignment[0]:
        subTree = ["Statement1", assignment[1]]
        return [True, subTree]
    xPrint = checkPrint()
    if xPrint[0]:
        subTree = ["Statement2", xPrint[1]]
        return [True, subTree]
    return [False, False]


def checkFunctionDeclaration():
    global currentIndex
    if parseTreeInput[currentIndex] == "FUNCTION":
        currentIndex += 1
        name = checkName()
        if name[0]:
            if parseTreeInput[currentIndex] == "LPAREN":
                currentIndex += 1
                functionParams = checkFunctionParams()
                if functionParams[0]:
                    if parseTreeInput[currentIndex] == "LBRACE":
                        currentIndex += 1
                        functionBody = checkFunctionBody()
                        if functionBody[0]:
                            if parseTreeInput[currentIndex] == "RBRACE":
                                currentIndex += 1
                                subTree = ["FunctionDeclaration", "FUNCTION", name[1], "LPAREN", functionParams[1], "LBRACE", functionBody[1], "RBRACE"]
                                return [True, subTree]
                            currentIndex -= 4
                            return [False, False]
                        currentIndex -= 4
                        return [False, False]
                    currentIndex -= 3
                    return [False, False]
                currentIndex -= 3
                return [False, False]
            currentIndex -= 2
            return [False, False]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkFunctionParams():
    global currentIndex
    if parseTreeInput[currentIndex] == "RPAREN":
        currentIndex += 1
        subTree = ["FunctionParams0", "RPAREN"]
        return [True, subTree]
    nameList = checkNameList()
    if nameList[0]:
        if parseTreeInput[currentIndex] == "RPAREN":
            currentIndex += 1
            subTree = ["FunctionParams1", nameList[1], "RPAREN"]
            return [True, subTree]
        return [False, False]
    return [False, False]


def checkFunctionBody():
    global currentIndex
    xReturn = checkReturn()
    if xReturn[0]:
        subTree = ["FunctionBody0", xReturn[1]]
        return [True, subTree]
    program = checkProgram()
    if program[0]:
        xReturn = checkReturn()
        if xReturn[0]:
            subTree = ["FunctionBody1", program[1], xReturn[1]]
            return [True, subTree]
        return [False, False]
    return [False, False]


def checkReturn():
    global currentIndex
    if parseTreeInput[currentIndex] == "RETURN":
        currentIndex += 1
        parameterList = checkParameterList()
        if parameterList[0]:
            subTree = ["Return", "RETURN", parameterList[1]]
            return [True, subTree]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkAssignment():
    global currentIndex
    single = checkSingleAssignment()
    if single[0]:
        subTree = ["Assignment0", single[1]]
        return [True, subTree]
    multiple = checkMultipleAssignment()
    if multiple[0]:
        subTree = ["Assignment1", multiple[1]]
        return [True, subTree]
    return [False, False]


def checkSingleAssignment():
    global currentIndex
    if parseTreeInput[currentIndex] == "VAR":
        currentIndex += 1
        name = checkName()
        if name[0]:
            if parseTreeInput[currentIndex] == "ASSIGN":
                currentIndex += 1
                expression = checkExpression()
                if expression[0]:
                    subTree = ["SingleAssignment", "VAR", name[1], "ASSIGN", expression[1]]
                    return [True, subTree]
                currentIndex -= 3
                return [False, False]
            currentIndex -= 2
            return [False, False]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkMultipleAssignment():
    global currentIndex
    if parseTreeInput[currentIndex] == "VAR":
        currentIndex += 1
        nameList = checkNameList()
        if nameList[0]:
            if parseTreeInput[currentIndex] == "ASSIGN":
                currentIndex += 1
                functionCall = checkFunctionCall()
                if functionCall[0]:
                    subTree = ["MultipleAssignment", "VAR", nameList[1], "ASSIGN", functionCall[1]]
                    return [True, subTree]
                currentIndex -= 3
                return [False, False]
            currentIndex -= 2
            return [False, False]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkPrint():
    global currentIndex
    if parseTreeInput[currentIndex] == "PRINT":
        currentIndex += 1
        expression = checkExpression()
        if expression[0]:
            subTree = ["Print", "PRINT", expression[1]]
            return [True, subTree]
    return [False, False]


def checkNameList():
    global currentIndex
    name = checkName()
    if name[0]:
        if parseTreeInput[currentIndex] == "COMMA":
            currentIndex += 1
            nameList = checkNameList()
            if nameList[0]:
                subTree = ["NameList0", name[1], "COMMA", nameList[1]]
                return [True, subTree]
            currentIndex -= 2
            return [False, False]
        subTree = ["NameList1", name[1]]
        return [True, subTree]
    return [False, False]


def checkParameterList():
    global currentIndex
    parameter = checkParameter()
    if parameter[0]:
        if parseTreeInput[currentIndex] == "COMMA":
            currentIndex += 1
            parameterList = checkParameterList()
            if parameterList[0]:
                subTree = ["ParameterList0", parameter[1], "COMMA", parameterList[1]]
                return [True, subTree]
            currentIndex -= 1
            return [False, False]
        subTree = ["ParameterList1", parameter[1]]
        return [True, subTree]
    return [False, False]


def checkParameter():
    global currentIndex
    expression = checkExpression()
    if expression[0]:
        subTree = ["Parameter0", expression[1]]
        return [True, subTree]
    name = checkName()
    if name[0]:
        subTree = ["Parameter1", name[1]]
        return [True, subTree]
    return [False, False]


def checkExpression():
    global currentIndex
    term = checkTerm()
    if term[0]:
        if parseTreeInput[currentIndex] == "ADD" or parseTreeInput[currentIndex] == "SUB":
            token = parseTreeInput[currentIndex]
            currentIndex += 1
            expression = checkExpression()
            if expression[0]:
                subTree = ["Expression0", term[1], token, expression[1]]
                return [True, subTree]
            currentIndex -= 1
            return [False, False]
        subTree = ["Expression1", term[1]]
        return [True, subTree]
    return [False, False]


def checkTerm():
    global currentIndex
    factor = checkFactor()
    if factor[0]:
        if parseTreeInput[currentIndex] == "MULT" or parseTreeInput[currentIndex] == "DIV":
            token = parseTreeInput[currentIndex]
            currentIndex += 1
            term = checkTerm()
            if term[0]:
                subTree = ["Term0", factor[1], token, term[1]]
                return [True, subTree]
            currentIndex -= 1
            return [False, False]
        subTree = ["Term1", factor[1]]
        return [True, subTree]
    return [False, False]


def checkFactor():
    global currentIndex
    subExpression = checkSubExpression()
    if subExpression[0]:
        if parseTreeInput[currentIndex] == "EXP":
            currentIndex += 1
            factor = checkFactor()
            if factor[0]:
                subTree = ["Factor0", subExpression[1], "EXP", factor[1]]
                return [True, subTree]
            currentIndex -= 1
            return [False, False]
        subTree = ["Factor1", subExpression[1]]
        return [True, subTree]
    functionCall = checkFunctionCall()
    if functionCall[0]:
        subTree = ["Factor2", functionCall[1]]
        return [True, subTree]
    value = checkValue()
    if value[0]:
        if parseTreeInput[currentIndex] == "EXP":
            currentIndex += 1
            factor = checkFactor()
            if factor[0]:
                subTree = ["Factor3", value[1], "EXP", factor[1]]
                return [True, subTree]
            currentIndex -= 1
            return [False, False]
        subTree = ["Factor4", value[1]]
        return [True, subTree]
    return [False, False]


def checkFunctionCall():
    global currentIndex
    name = checkName()
    if name[0]:
        if parseTreeInput[currentIndex] == "LPAREN":
            currentIndex += 1
            functionCallParams = checkFunctionCallParams()
            if functionCallParams[0]:
                if parseTreeInput[currentIndex] == "COLON":
                    currentIndex += 1
                    number = checkNumber()
                    if number[0]:
                        subTree = ["FunctionCall0", name[1], "LPAREN", functionCallParams[1], "COLON", number[1]]
                        return [True, subTree]
                    currentIndex -= 3
                    return [False, False]
                subTree = ["FunctionCall1", name[1], "LPAREN", functionCallParams[1]]
                return [True, subTree]
            currentIndex -= 2
            return [False, False]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkFunctionCallParams():
    global currentIndex
    if parseTreeInput[currentIndex] == "RPAREN":
        subTree = ["FunctionCallParams0", "RPAREN"]
        currentIndex += 1
        return [True, subTree]
    parameterList = checkParameterList()
    if parameterList[0]:
        if parseTreeInput[currentIndex] == "RPAREN":
            subTree = ["FunctionCallParams1", parameterList[1], "RPAREN"]
            currentIndex += 1
            return [True, subTree]
        return [False, False]
    return [False, False]


def checkSubExpression():
    global currentIndex
    if parseTreeInput[currentIndex] == "LPAREN":
        currentIndex += 1
        expression = checkExpression()
        if expression[0]:
            if parseTreeInput[currentIndex] == "RPAREN":
                subTree = ["SubExpression", "LPAREN", expression[1], "RPAREN"]
                currentIndex += 1
                return [True, subTree]
            currentIndex -= 1
            return [False, False]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkValue():
    global currentIndex
    name = checkName()
    if name[0]:
        subTree = ["Value0", name[1]]
        return [True, subTree]
    number = checkNumber()
    if number[0]:
        subTree = ["Value1", number[1]]
        return [True, subTree]
    return [False, False]


def checkName():
    global currentIndex
    ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
    if ident:
        subTree = ["Name0", parseTreeInput[currentIndex]]
        currentIndex += 1
        return [True, subTree]
    if parseTreeInput[currentIndex] == "SUB" or parseTreeInput[currentIndex] == "ADD":
        currentIndex += 1
        ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
        if ident:
            subTree = ["Name0", parseTreeInput[currentIndex - 1], parseTreeInput[currentIndex]]
            currentIndex += 1
            return [True, subTree]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkNumber():
    global currentIndex
    number = re.match("NUMBER:.+", parseTreeInput[currentIndex])
    if number:
        subTree = ["Number0", parseTreeInput[currentIndex]]
        currentIndex += 1
        return [True, subTree]
    if parseTreeInput[currentIndex] == "SUB" or parseTreeInput[currentIndex] == "ADD":
        currentIndex += 1
        number = re.match("NUMBER:.+", parseTreeInput[currentIndex])
        if number:
            subTree = ["Number1", parseTreeInput[currentIndex - 1], parseTreeInput[currentIndex]]
            currentIndex += 1
            return [True, subTree]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def ReadInput():
    global outputFinal
    tokens = sys.stdin.readlines()

    # loop through lines in quirk file
    for token in tokens:
        # convert tokens to python string
        x = str(token)

        # remove extraneous \n
        y = x.replace("\n", "")
        parseTreeInput.append(y)
        
    serializedParseTree = json.dumps(checkProgram()[-1])
    if parseTreeInput[currentIndex] == "EOF":
        sys.stdout.write(serializedParseTree)
    else:
        exit()

if __name__ == '__main__':
    ReadInput()
