import sys
import re

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

grammarType = checkGrammarType(parentTree):
    This function calls a child leaf in the grammar tree and returns a
    list consisting of a boolean value and the existing tree of the function
    that called it. This allows grammar to be checked, and the tree to maintain
    itself as the code traverses along.

if parseTreeInput[currentIndex] == "TOKEN":
    This checks to see if the token literal is in its correct position for
    the input quirk file to be accurate. If tokens are not found in their
    correct location, the program is found to have an error.

subTree = addToParentTree(parentTree, "Return"):
    This function adds the value to the AST for our output.
    It is called relative to the position of the current node,
    and will append in order of traversal, only appending when nodes are
    returned as True.
'''

# This function handles tree formatting
def addToParentTree(parentTree, item, item2 = None):
    if item2 != None:
        if not parentTree:
            output = [item, item2]
        else:
            output = [[item, item2], parentTree]
    else:
        if not parentTree:
            output = [item]
        else:
            output = [item, parentTree]
    return output

'''
The main parsing functions are found below. All decision making is handled below for each piece of
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
            subTree = ["Program", statement[1], program[1]]
            #subTree = addToParentTree(program[1], "Program0")
            return [True, subTree]
        subTree = ["Program", statement[1]]
        #subTree = addToParentTree(statement[1], "Program1")
        return [True, subTree]
    return [False, False]


def checkStatement(parentTree):
    global currentIndex
    function = checkFunctionDeclaration(parentTree)
    if function[0]:
        subTree = ["Statement0", function[1]]
        #subTree = addToParentTree(function[1], "Statement0")
        return [True, subTree]
    assignment = checkAssignment(parentTree)
    if assignment[0]:
        subTree = ["Statement1", assignment[1]]
        #subTree = addToParentTree(assignment[1], "Statement1")
        return [True, subTree]
    xPrint = checkPrint(parentTree)
    if xPrint[0]:
        subTree = ["Statement2", xPrint[1]]
        #subTree = addToParentTree(xPrint[1], "Statement2")
        return [True, subTree]
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
                                subTree = ["FunctionDeclaration", "FUNCTION", name[1], "LPAREN", functionParams[1], "LBRACE", functionBody[1], "RBRACE"]
                                #subTree = addToParentTree(functionBody[1], "Function Declaration", "FUNCTION")
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


def checkFunctionParams(parentTree):
    global currentIndex
    if parseTreeInput[currentIndex] == "RPAREN":
        currentIndex += 1
        subTree = ["FunctionParams0", "RPAREN"]
        #subTree = addToParentTree(parentTree, "FunctionParams0", "RPAREN")
        return [True, subTree]
    nameList = checkNameList(parentTree)
    if nameList[0]:
        if parseTreeInput[currentIndex] == "RPAREN":
            currentIndex += 1
            subTree = ["FunctionParams1", nameList[1], "RPAREN"]
            #subTree = addToParentTree(nameList[1], "FunctionParams1", "RPAREN")
            return [True, subTree]
        return [False, False]
    return [False, False]


def checkFunctionBody(parentTree):
    global currentIndex
    xReturn = checkReturn(parentTree)
    if xReturn[0]:
        subTree = ["FunctionBody0", xReturn[1]]
        #subTree = addToParentTree(xReturn[1], "FunctionBody0")
        return [True, subTree]
    program = checkProgram(parentTree)
    if program[0]:
        xReturn = checkReturn(program[1])
        if xReturn[0]:
            subTree = ["FunctionBody1", program[1], xReturn[1]]
            #subTree = addToParentTree(xReturn[1], "FunctionBody1")
            return [True, subTree]
        return [False, False]
    return [False, False]


def checkReturn(parentTree):
    global currentIndex
    if parseTreeInput[currentIndex] == "RETURN":
        currentIndex += 1
        parameterList = checkParameterList(parentTree)
        if parameterList[0]:
            subTree = ["Return", "RETURN", parameterList[1]]
            #subTree = addToParentTree(parameterList[1], "Return", "RETURN")
            return [True, subTree]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkAssignment(parentTree):
    global currentIndex
    single = checkSingleAssignment(parentTree)
    if single[0]:
        subTree = ["Assignment0", single[1]]
        #subTree = addToParentTree(single[1], "Assignment0")
        return [True, subTree]
    multiple = checkMultipleAssignment(parentTree)
    if multiple[0]:
        subTree = ["Assignment1", multiple[1]]
        #subTree = addToParentTree(multiple[1], "Assignment1")
        return [True, subTree]
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
                    subTree = ["SingleAssignment", "VAR", name[1], "ASSIGN", expression[1]]
                    #subTree = addToParentTree(expression[1], "SingleAssignment")
                    return [True, subTree]
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
                    subTree = ["MultipleAssignment", "VAR", nameList[1], "ASSIGN", functionCall[1]]
                    #subTree = addToParentTree(functionCall[1], "MultipleAssignment")
                    return [True, subTree]
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
            subTree = ["Print", "PRINT", expression[1]]
            #subTree = addToParentTree(expression[1], "Print")
            return [True, subTree]
    return [False, False]


def checkNameList(parentTree):
    global currentIndex
    name = checkName(parentTree)
    if name[0]:
        if parseTreeInput[currentIndex] == "COMMA":
            currentIndex += 1
            nameList = checkNameList(name[1])
            if nameList[0]:
                subTree = ["NameList0", name[1], "COMMA", nameList[1]]
                #subTree = addToParentTree(nameList[1], "NameList0")
                return [True, subTree]
            currentIndex -= 2
            return [False, False]
        subTree = ["NameList1", name[1]]
        #subTree = addToParentTree(name[1], "NameList1")
        return [True, subTree]
    return [False, False]


def checkParameterList(parentTree):
    global currentIndex
    parameter = checkParameter(parentTree)
    if parameter[0]:
        if parseTreeInput[currentIndex] == "COMMA":
            currentIndex += 1
            parameterList = checkParameterList(parameter[1])
            if parameterList[0]:
                subTree = ["ParameterList0", parameter[1], "COMMA", parameterList[1]]
                #subTree = addToParentTree(parameterList[1], "ParameterList0")
                return [True, subTree]
            currentIndex -= 1
            return [False, False]
        subTree = ["ParameterList1", parameter[1]]
        #subTree = addToParentTree(parameter[1], "ParameterList1")
        return [True, subTree]
    return [False, False]


def checkParameter(parentTree):
    global currentIndex
    expression = checkExpression(parentTree)
    if expression[0]:
        subTree = ["Parameter0", expression[1]]
        #subTree = addToParentTree(expression[1], "Parameter0")
        return [True, subTree]
    name = checkName(parentTree)
    if name[0]:
        subTree = ["Parameter1", name[1]]
        #subTree = addToParentTree(name[1], "Parameter1")
        return [True, subTree]
    return [False, False]


def checkExpression(parentTree):
    global currentIndex
    term = checkTerm(parentTree)
    if term[0]:
        if parseTreeInput[currentIndex] == "ADD" or parseTreeInput[currentIndex] == "SUB":
            token = parseTreeInput[currentIndex]
            currentIndex += 1
            expression = checkExpression(term[1])
            if expression[0]:
                subTree = ["Expression0", term[1], token, expression[1]]
                #subTree = addToParentTree(expression[1], "Expression0")
                return [True, subTree]
            currentIndex -= 1
            return [False, False]
        subTree = ["Expression1", term[1]]
        #subTree = addToParentTree(term[1], "Expression1")
        return [True, subTree]
    return [False, False]


def checkTerm(parentTree):
    global currentIndex
    factor = checkFactor(parentTree)
    if factor[0]:
        if parseTreeInput[currentIndex] == "MULT" or parseTreeInput[currentIndex] == "DIV":
            token = parseTreeInput[currentIndex]
            currentIndex += 1
            term = checkTerm(factor[1])
            if term[0]:
                subTree = ["Term0", factor[1], token, term[1]]
                #subTree = addToParentTree(term[1], "Term0")
                return [True, subTree]
            currentIndex -= 1
            return [False, False]
        subTree = ["Term1", factor[1]]
        #subTree = addToParentTree(factor[1], "Term1")
        return [True, subTree]
    return [False, False]


def checkFactor(parentTree):
    global currentIndex
    subExpression = checkSubExpression(parentTree)
    if subExpression[0]:
        if parseTreeInput[currentIndex] == "EXP":
            currentIndex += 1
            factor = checkFactor(subExpression[1])
            if factor[0]:
                subTree = ["Factor0", subExpression[1], "EXP", factor[1]]
                #subTree = addToParentTree(factor[1], "Factor0")
                return [True, subTree]
            currentIndex -= 1
            return [False, False]
        subTree = ["Factor1", subExpression[1]]
        #subTree = addToParentTree(subExpression[1], "Factor1")
        return [True, subTree]
    functionCall = checkFunctionCall(parentTree)
    if functionCall[0]:
        subTree = ["Factor2", functionCall[1]]
        #subTree = addToParentTree(functionCall[1], "Factor2")
        return [True, subTree]
    value = checkValue(parentTree)
    if value[0]:
        if parseTreeInput[currentIndex] == "EXP":
            currentIndex += 1
            factor = checkFactor(value[1])
            if factor[0]:
                subTree = ["Factor3", value[1], "EXP", factor[1]]
                #subTree = addToParentTree(factor[1], "Factor3")
                return [True, subTree]
            currentIndex -= 1
            return [False, False]
        subTree = ["Factor4", value[1]]
        #subTree = addToParentTree(value[1], "Factor4")
        return [True, subTree]
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
                        subTree = ["FunctionCall0", name[1], "LPAREN", functionCallParams[1], "COLON", number[1]]
                        #subTree = addToParentTree(number[1], "FunctionCall0")
                        return [True, subTree]
                    currentIndex -= 3
                    return [False, False]
                subTree = ["FunctionCall1", name[1], "LPAREN", functionCallParams[1]]
                #subTree = addToParentTree(functionCallParams[1], "FunctionCall1")
                return [True, subTree]
            currentIndex -= 2
            return [False, False]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkFunctionCallParams(parentTree):
    global currentIndex
    if parseTreeInput[currentIndex] == "RPAREN":
        subTree = ["FunctionCallParams0", "RPAREN"]
        currentIndex += 1
        #subTree = addToParentTree(parentTree, "FunctionCallParams0")
        return [True, subTree]
    parameterList = checkParameterList(parentTree)
    if parameterList[0]:
        if parseTreeInput[currentIndex] == "RPAREN":
            subTree = ["FunctionCallParams1", parameterList[1], "RPAREN"]
            currentIndex += 1
            #subTree = addToParentTree(parameterList[1], "FunctionCallParams1")
            return [True, subTree]
        return [False, False]
    return [False, False]


def checkSubExpression(parentTree):
    global currentIndex
    if parseTreeInput[currentIndex] == "LPAREN":
        currentIndex += 1
        expression = checkExpression(parentTree)
        if expression[0]:
            if parseTreeInput[currentIndex] == "RPAREN":
                subTree = ["SubExpression", "LPAREN", expression[1], "RPAREN"]
                currentIndex += 1
                #subTree = addToParentTree(expression[1], "SubExpression")
                return [True, subTree]
            currentIndex -= 1
            return [False, False]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkValue(parentTree):
    global currentIndex
    name = checkName(parentTree)
    if name[0]:
        subTree = ["Value0", name[1]]
        #subTree = addToParentTree(name[1], "Value0")
        return [True, subTree]
    number = checkNumber(parentTree)
    if number[0]:
        subTree = ["Value1", number[1]]
        #subTree = addToParentTree(number[1], "Value1")
        return [True, subTree]
    return [False, False]


def checkName(parentTree):
    global currentIndex
    ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
    if ident:
        subTree = ["Name0", parseTreeInput[currentIndex]]
        currentIndex += 1
        #subTree = addToParentTree(parentTree, "Name0", parseTreeInput[currentIndex - 1])
        return [True, subTree]
    if parseTreeInput[currentIndex] == "SUB" or parseTreeInput[currentIndex] == "ADD":
        currentIndex += 1
        ident = re.match("IDENT:.+", parseTreeInput[currentIndex])
        if ident:
            subTree = ["Name0", parseTreeInput[currentIndex - 1], parseTreeInput[currentIndex]]
            currentIndex += 1
            #subTree = addToParentTree(parentTree, "Name1", parseTreeInput[currentIndex - 1])
            return [True, subTree]
        currentIndex -= 1
        return [False, False]
    return [False, False]


def checkNumber(parentTree):
    global currentIndex
    number = re.match("NUMBER:.+", parseTreeInput[currentIndex])
    if number:
        subTree = ["Number0", parseTreeInput[currentIndex]]
        currentIndex += 1
        #subTree = addToParentTree(parentTree, "Number0", parseTreeInput[currentIndex - 1])
        return [True, subTree]
    if parseTreeInput[currentIndex] == "SUB" or parseTreeInput[currentIndex] == "ADD":
        currentIndex += 1
        number = re.match("NUMBER:.+", parseTreeInput[currentIndex])
        if number:
            subTree = ["Number1", parseTreeInput[currentIndex - 1], parseTreeInput[currentIndex]]
            currentIndex += 1
            ##subTree = addToParentTree(parentTree, "Number1", parseTreeInput[currentIndex - 1])
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

    output = checkProgram([])
    print(output[-1])
    if parseTreeInput[currentIndex] == "EOF":
        print("\nParsing OK\n")
    else:
        print("\nError\n")

if __name__ == '__main__':
    ReadInput()
