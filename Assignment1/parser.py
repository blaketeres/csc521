import sys
import re

parseTreeInput = []
currentIndex = 0
parserOutput = [None]
outputFinal = []

# append subtree to immediate parent tree upon function returning True
# this will keep the order of the tree in tact, and eliminate incorrect leafs

'''
How My Parser Works:

Each function listed below traverses the grammar. Below are bits of code
that I use throughout the program and a small explanation. I am outlining
them here so that it is not repetitive and chunky to read throughout.

global currentIndex:
    This keeps the index position from getting caught in a local context.

currentIndex (+-)= 1:
    Manually maintaining the token position. Will be incremented and
    decremented as needed, depending on the return values of the leaf
    node function calls.

grammarType = checkGrammarType(parentTree):
    This function calls a child leaf in the grammar tree and returns a
    list consisting of a boolean value and the existing tree of the function
    that called it. This allows grammar to be checked, and the tree to maintain
    itself as the code traverses along.

if parseTreeInput[currentIndex] == "TOKEN":
    This checks to see if the token literal is in its correct position for
    the input quirk file to be accurate. If tokens are not found in their
    correct location, the program is found to have an error.

parentTree = addToParentTree(parentTree, "Return"):
    This function adds the value to the AST for our output.
    It is called relative to the position of the current node,
    and will append in order of traversal, only appending when nodes are
    returned as True.
'''

# This function handles tree formatting


def addToParentTree(parentTree, item, item2=None):
    if item2 != None:
        if not parentTree:
            parentTree = [item, item2]
        else:
            parentTree = [item, item2, parentTree]
    else:
        if not parentTree:
            parentTree = [item]
        else:
            parentTree = [item, parentTree]
    return parentTree

'''
Main parse tree. All decision making is handled below for each piece of
grammar. Every function below follows the same format, checking possible
leafs and returning True upon success, and False upon failure.
The program will exit if a possible path is not found before the
parser reaches the end of the input file
'''


def checkProgram(parentTree):
    global currentIndex
    statement = checkStatement(parentTree)
    if statement[0]:
        program = checkProgram(statement[1])
        if program[0]:
            parentTree = addToParentTree(program[1], "Program0")
            return [True, parentTree]
        parentTree = addToParentTree(statement[1], "Program1")
        return [True, parentTree]
    return [False, False]


def checkStatement(parentTree):
    global currentIndex
    function = checkFunctionDeclaration(parentTree)
    if function[0]:
        parentTree = addToParentTree(function[1], "Statement0")
        return [True, parentTree]
    assignment = checkAssignment(parentTree)
    if assignment[0]:
        parentTree = addToParentTree(assignment[1], "Statement1")
        return [True, parentTree]
    xPrint = checkPrint(parentTree)
    if xPrint[0]:
        parentTree = addToParentTree(xPrint[1], "Statement2")
        return [True, parentTree]
    return [False, False]


def checkFunctionDeclaration(parentTree):
    global currentIndex
    if parseTreeInput[currentIndex] == "FUNCTION":
        currentIndex += 1
        name = checkName(parentTree)
        if name[0]:
            if parseTreeInput[currentIndex] == "LPAREN":
                currentIndex += 1
                functionParams = checkFunctionParams(name[1])
                if functionParams[0]:
                    if parseTreeInput[currentIndex] == "LBRACE":
                        currentIndex += 1
                        functionBody = checkFunctionBody(functionParams[1])
                        if functionBody[0]:
                            if parseTreeInput[currentIndex] == "RBRACE":
                                currentIndex += 1
                                parentTree = addToParentTree(
                                    functionBody[1], "Function Declaration", parseTreeInput[currentIndex - 8])
                                return [True, parentTree]
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


def checkFunctionParams(parentTree):
    global currentIndex
    if parseTreeInput[currentIndex] == "RPAREN":
        currentIndex += 1
        parentTree = addToParentTree(parentTree, "FunctionParams0")
        return [True, parentTree]
    nameList = checkNameList(parentTree)
    if nameList[0]:
        if parseTreeInput[currentIndex] == "RPAREN":
            currentIndex += 1
            parentTree = addToParentTree(nameList[1], "FunctionParams1")
            return [True, parentTree]
        return [False, False]
    return [False, False]


def checkFunctionBody(parentTree):
    global currentIndex
    xReturn = checkReturn(parentTree)
    if xReturn[0]:
        parentTree = addToParentTree(xReturn[1], "FunctionBody0")
        return [True, parentTree]
    program = checkProgram(parentTree)
    if program[0]:
        xReturn = checkReturn(program[1])
        if xReturn[0]:
            parentTree = addToParentTree(xReturn[1], "FunctionBody1")
            return [True, parentTree]
        return [False, False]
    return [False, False]


def checkReturn(parentTree):
    global currentIndex
    if parseTreeInput[currentIndex] == "RETURN":
        currentIndex += 1
        parameterList = checkParameterList(parentTree)
        if parameterList[0]:
            parentTree = addToParentTree(parameterList[1], "Return")
            return [True, parentTree]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkAssignment(parentTree):
    global currentIndex
    single = checkSingleAssignment(parentTree)
    if single[0]:
        parentTree = addToParentTree(single[1], "Assignment0")
        return [True, parentTree]
    multiple = checkMultipleAssignment(parentTree)
    if multiple[0]:
        parentTree = addToParentTree(multiple[1], "Assignment1")
        return [True, parentTree]
    return [False, False]


def checkSingleAssignment(parentTree):
    global currentIndex
    if parseTreeInput[currentIndex] == "VAR":
        currentIndex += 1
        name = checkName(parentTree)
        if name[0]:
            if parseTreeInput[currentIndex] == "ASSIGN":
                currentIndex += 1
                expression = checkExpression(name[1])
                if expression[0]:
                    parentTree = addToParentTree(
                        expression[1], "SingleAssignment")
                    return [True, parentTree]
                currentIndex -= 3
                return [False, False]
            currentIndex -= 2
            return [False, False]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkMultipleAssignment(parentTree):
    global currentIndex
    if parseTreeInput[currentIndex] == "VAR":
        currentIndex += 1
        nameList = checkNameList(parentTree)
        if nameList[0]:
            if parseTreeInput[currentIndex] == "ASSIGN":
                currentIndex += 1
                functionCall = checkFunctionCall(name[1])
                if functionCall[0]:
                    parentTree = addToParentTree(
                        functionCall[1], "MultipleAssignment")
                    return [True, parentTree]
                currentIndex -= 3
                return [False, False]
            currentIndex -= 2
            return [False, False]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkPrint(parentTree):
    global currentIndex
    if parseTreeInput[currentIndex] == "PRINT":
        currentIndex += 1
        expression = checkExpression(parentTree)
        if expression[0]:
            parentTree = addToParentTree(expression[1], "Print")
            return [True, parentTree]
    return [False, False]


def checkNameList(parentTree):
    global currentIndex
    name = checkName(parentTree)
    if name[0]:
        if parseTreeInput[currentIndex] == "COMMA":
            currentIndex += 1
            nameList = checkNameList(name[1])
            if nameList[0]:
                parentTree = addToParentTree(nameList[1], "NameList0")
                return [True, parentTree]
            currentIndex -= 2
            return [False, False]
        parentTree = addToParentTree(name[1], "NameList1")
        return [True, parentTree]
    return [False, False]


def checkParameterList(parentTree):
    global currentIndex
    parameter = checkParameter(parentTree)
    if parameter[0]:
        if parseTreeInput[currentIndex] == "COMMA":
            currentIndex += 1
            parameterList = checkParameterList(parameter[1])
            if parameterList[0]:
                parentTree = addToParentTree(
                    parameterList[1], "ParameterList0")
                return [True, parentTree]
            currentIndex -= 1
            return [False, False]
        parentTree = addToParentTree(parameter[1], "ParameterList1")
        return [True, parentTree]
    return [False, False]


def checkParameter(parentTree):
    global currentIndex
    expression = checkExpression(parentTree)
    if expression[0]:
        parentTree = addToParentTree(expression[1], "Parameter0")
        return [True, parentTree]
    name = checkName(parentTree)
    if name[0]:
        parentTree = addToParentTree(name[1], "Parameter1")
        return [True, parentTree]
    return [False, False]


def checkExpression(parentTree):
    global currentIndex
    term = checkTerm(parentTree)
    if term[0]:
        if parseTreeInput[currentIndex] == "ADD" or parseTreeInput[currentIndex] == "SUB":
            currentIndex += 1
            expression = checkExpression(term[1])
            if expression[0]:
                parentTree = addToParentTree(expression[1], "Expression0")
                return [True, parentTree]
            currentIndex -= 1
            return [False, False]
        parentTree = addToParentTree(term[1], "Expression1")
        return [True, parentTree]
    return [False, False]


def checkTerm(parentTree):
    global currentIndex
    factor = checkFactor(parentTree)
    if factor[0]:
        if parseTreeInput[currentIndex] == "MULT" or parseTreeInput[currentIndex] == "DIV":
            currentIndex += 1
            term = checkTerm(factor[1])
            if term[0]:
                parentTree = addToParentTree(term[1], "Term0")
                return [True, parentTree]
            currentIndex -= 1
            return [False, False]
        parentTree = addToParentTree(factor[1], "Term1")
        return [True, parentTree]
    return [False, False]


def checkFactor(parentTree):
    global currentIndex
    subExpression = checkSubExpression(parentTree)
    if subExpression[0]:
        if parseTreeInput[currentIndex] == "EXP":
            currentIndex += 1
            factor = checkFactor(subExpression[1])
            if factor[0]:
                parentTree = addToParentTree(factor[1], "Factor0")
                return [True, parentTree]
            currentIndex -= 1
            return [False, False]
        parentTree = addToParentTree(subExpression[1], "Factor1")
        return [True, parentTree]
    functionCall = checkFunctionCall(parentTree)
    if functionCall[0]:
        parentTree = addToParentTree(functionCall[1], "Factor2")
        return [True, parentTree]
    value = checkValue(parentTree)
    if value[0]:
        if parseTreeInput[currentIndex] == "EXP":
            currentIndex += 1
            factor = checkFactor(value[1])
            if factor[0]:
                parentTree = addToParentTree(factor[1], "Factor3")
                return [True, parentTree]
            currentIndex -= 1
            return [False, False]
        parentTree = addToParentTree(value[1], "Factor4")
        return [True, parentTree]
    return [False, False]


def checkFunctionCall(parentTree):
    global currentIndex
    name = checkName(parentTree)
    if name[0]:
        if parseTreeInput[currentIndex] == "LPAREN":
            currentIndex += 1
            functionCallParams = checkFunctionCallParams(name[1])
            if functionCallParams[0]:
                if parseTreeInput[currentIndex] == "COLON":
                    currentIndex += 1
                    number = checkNumber(functionCallParams[1])
                    if number[0]:
                        parentTree = addToParentTree(
                            number[1], "FunctionCall0")
                        return [True, parentTree]
                    currentIndex -= 3
                    return [False, False]
                parentTree = addToParentTree(
                    functionCallParams[1], "FunctionCall1")
                return [True, parentTree]
            currentIndex -= 2
            return [False, False]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkFunctionCallParams(parentTree):
    global currentIndex
    if parseTreeInput[currentIndex] == "RPAREN":
        currentIndex += 1
        parentTree = addToParentTree(parentTree, "FunctionCallParams0")
        return [True, parentTree]
    parameterList = checkParameterList(parentTree)
    if parameterList[0]:
        if parseTreeInput[currentIndex] == "RPAREN":
            currentIndex += 1
            parentTree = addToParentTree(
                parameterList[1], "FunctionCallParams1")
            return [True, parentTree]
        return [False, False]
    return [False, False]


def checkSubExpression(parentTree):
    global currentIndex
    if parseTreeInput[currentIndex] == "LPAREN":
        currentIndex += 1
        expression = checkExpression(parentTree)
        if expression[0]:
            if parseTreeInput[currentIndex] == "RPAREN":
                currentIndex += 1
                parentTree = addToParentTree(expression[1], "SubExpression")
                return [True, parentTree]
            currentIndex -= 1
            return [False, False]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkValue(parentTree):
    global currentIndex
    name = checkName(parentTree)
    if name[0]:
        parentTree = addToParentTree(name[1], "Value0")
        return [True, parentTree]
    number = checkNumber(parentTree)
    if number[0]:
        parentTree = addToParentTree(number[1], "Value1")
        return [True, parentTree]
    return [False, False]


def checkName(parentTree):
    global currentIndex
    ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
    if ident:
        currentIndex += 1
        parentTree = addToParentTree(
            parentTree, "Name0", parseTreeInput[currentIndex - 1])
        return [True, parentTree]
    if parseTreeInput[currentIndex] == "SUB" or parseTreeInput[currentIndex] == "ADD":
        currentIndex += 1
        ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
        if ident:
            currentIndex += 1
            parentTree = addToParentTree(
                parentTree, "Name1", parseTreeInput[currentIndex - 1])
            return [True, parentTree]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkNumber(parentTree):
    global currentIndex
    number = re.match("NUMBER:.+", parseTreeInput[currentIndex])
    if number:
        currentIndex += 1
        parentTree = addToParentTree(
            parentTree, "Number0", parseTreeInput[currentIndex - 1])
        return [True, parentTree]
    if parseTreeInput[currentIndex] == "SUB" or parseTreeInput[currentIndex] == "ADD":
        currentIndex += 1
        number = re.match("NUMBER:.+", parseTreeInput[currentIndex])
        if number:
            currentIndex += 1
            parentTree = addToParentTree(
                parentTree, "Number1", parseTreeInput[currentIndex - 1])
            return [True, parentTree]
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

    output = checkProgram(outputFinal)
    print(output[-1])
    if parseTreeInput[currentIndex] == "EOF":
        print("\nParsing OK\n")
    else:
        print("\nError\n")

if __name__ == '__main__':
    ReadInput()
