import sys
import pprint
import json
import ast

def lookupInScopeStack(name, scope):
    '''Returns values (including declared functions!) from the scope.
    name - A string value holding the name of a bound variable or function.
    scope - The scope that holds names to value binding for variables and
        functions.
    returns - the value associated with the name in scope.
    '''
    #turn this on for better debugging
    #print("lookup_in_scope_stack() "+ str(name))
    if name in scope:
        return scope[name]
    else:
        if "__parent__" in scope:
            return lookup_in_scope_stack(name, scope["__parent__"])
        else:
            return None

def getName(token):
    '''Returns the string lexeme associated with an IDENT token, tok.
    '''
    colon_index = token.find(":")
    return token[colon_index+1:]


def getNumber(token):
    '''
    Attempts to return the right data type for numbes
    so that everything is not defaulted to a float
    '''
    def tryeval(val):
        try:
            val = ast.literal_eval(val)
        except ValueError:
            pass
        return val

    colon_index = token.find(":")
    return tryeval((token[colon_index+1:]))

def raiseException(exception):
    '''custom error raising function
    '''
    raise Exception(exception)


def callFunction(*args):
    '''calls a global function based on its name and scope
    '''
    name = args[0]
    parent = args[1]
    scope = args[2]
    return globals()[name](parent, scope)


# <Program> -> <Statement> <Program> | <Statement>
def Program0(parent, scope):
    callFunction(parent[1][0], parent[1], scope)
    callFunction(parent[2][0], parent[2], scope)


def Program1(parent, scope):
    callFunction(parent[1][0], parent[1], scope)

# <Statement> -> <FunctionDeclaration> | <Assignment> | <Print>
def Statement0(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)


def Statement1(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)


def Statement2(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)

# <FunctionDeclaration> -> FUNCTION <Name> LPAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
def FunctionDeclaration(parent, scope):
    # Get the function name
    functionName = getName(parent[2][1])

    # get names of parameters
    functionParams = (callFunction(parent[4][0], parent[4], scope))

    # remove extraneous information in list
    if functionParams:
        functionParams = functionParams[1::2]

    # get function body
    functionBody = parent[6]

    # bind function to scope
    scope[functionName] = [functionParams, functionBody]

# <FunctionParams> -> RPAREN | <NameList> RPAREN
def FunctionParams0(parent, scope):
    return


def FunctionParams1(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)


# <FunctionBody> -> <Return> | <Program> <Return>
def FunctionBody0(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)


def FunctionBody1(parent, scope):
    # run the thing that needs to be returned
    program = callFunction(parent[1][0], parent[1], scope)

    # get the return value
    xReturn = callFunction(parent[2][0], parent[2], scope)
    return xReturn

# <Return> -> RETURN <ParameterList>
def Return(parent, scope):
    return callFunction(parent[2][0], parent[2], scope)

# <Assignment> -> <SingleAssignment> | <MultipleAssignment>
def Assignment0(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)


def Assignment1(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)

# <SingleAssignment> -> VAR <Name> ASSIGN <Expression>
def SingleAssignment(parent, scope):
    name = callFunction(parent[2][0], parent[2], scope)[-1]
    # checks is variable has already been declared
    if name in scope:
        if lookupInScopeStack(name, scope) == scope[name]:
            x = str(name)
            errorMessage = "Variable " + x + " cannot be redefined"
            raise Exception(errorMessage)

    expression = callFunction(parent[4][0], parent[4], scope)
    if isinstance(expression, list):
        scope[name] = expression[0]
        return
    scope[name] = expression
    return

# <MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
def MultipleAssignment(parent, scope):
    '''This function converts a nested list of paramaters
    to a single-depth list of function paramaters
    '''
    def unNestList(paramList, out):
        for item in paramList:
            if isinstance(item, list):
                unNestList(paramList[1], out)
            else:
                out.append(item)
        return out

    nameList = callFunction(parent[2][0], parent[2], scope)[1::2]
    functionCall = callFunction(parent[4][0], parent[4], scope)
    returnValues = unNestList(functionCall, [])

    '''
    Check to see if variable is already in scope
    and other various error checking
    '''
    for i in range(len(nameList)):
        if nameList[i] in scope.keys():
            errorMessage = "Variable " + "'" + str(nameList[i]) + "'" " is already defined"
            raiseException(errorMessage)
    if len(nameList) > len(returnValues):
        raiseException("Invalid # of return values")
    if len(nameList) < len(returnValues):
        raiseException("Invalid # of variables to assign")
    for i, item in enumerate(returnValues):
        scope[nameList[i]] = returnValues[i]
    return functionCall

# <Print> -> PRINT <Expression>
def Print(parent, scope):
    expression = callFunction(parent[2][0], parent[-1], scope)
    if expression == None:
        errorMessage = "Cannot print undefined variable " + "'" + getName(parent[2][1][1][1][1][1]) + "'"
        raiseException(errorMessage)

    '''Prints the output using the python print() function
    '''
    if isinstance(expression, list):
        expression = expression[0]
    print(expression)
    return

# <NameList> -> <Name> COMMA <NameList> | <Name>
def NameList0(parent, scope):
    n1 = callFunction(parent[1][0], parent[1], scope)
    n2 = callFunction(parent[3][0], parent[3], scope)
    return n1 + n2


def NameList1(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)

# <ParameterList> -> <Parameter> COMMA <ParameterList> | <Parameter>
def ParameterList0(parent, scope):
    p1 = callFunction(parent[1][0], parent[1], scope)
    p2 = callFunction(parent[3][0], parent[3], scope)
    return [p1, p2]

def ParameterList1(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)

# <Parameter> -> <Expression> | <Name>
def Parameter0(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)


def Parameter1(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)

# <Expression> -> <Term> ADD <Expression> | <Term> SUB <Expression> | <Term>
def Expression0(parent, scope):
    term = callFunction(parent[1][0], parent[1], scope)
    operator = parent[2]
    expression = callFunction(parent[3][0], parent[3], scope)
    if operator == "ADD":
        try:
            return term[0] + expression
        except:
            return term + expression
    try:
        return term[0] - expression
    except:
        return term - expression

def Expression1(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)

# <Term> -> <Factor> MULT <Term> | <Factor> DIV <Term> | <Factor>
def Term0(parent, scope):
    factor = callFunction(parent[1][0], parent[1], scope)
    operator = parent[2]
    term = callFunction(parent[3][0], parent[3], scope)
    if operator == "MULT":
        try:
            return factor[0] * term
        except:
            return factor * term
    try:
        return factor[0] / term
    except:
        return factor / term


def Term1(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)

# <Factor> -> <SubExpression> EXP <Factor> | <SubExpression> | <FunctionCall> | <Value> EXP <Factor> | <Value>
def Factor0(parent, scope):
    subExpression = callFunction(parent[1][0], parent[1], scope)
    factor = callFunction(parent[3][0], parent[3], scope)
    return subExpression ** factor

def Factor1(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)


def Factor2(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)

def Factor3(parent, scope):
    value = callFunction(parent[1][0], parent[1], scope)
    factor = callFunction(parent[3][0], parent[3], scope)
    return value ** factor

def Factor4(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)

# <FunctionCall> -> <Name> LPAREN <FunctionCallParams> COLON <Number> | <Name> LPAREN <FunctionCallParams>
def FunctionCall0(parent, scope):
    '''This function converts a nested list of paramaters
    to a single-depth list of function paramaters
    '''
    def unNestList(paramList, out):
        if len(paramList) > 1:
            for item in paramList:
                if not isinstance(item, list):
                    out.append(item)
                else:
                    unNestList(item, out)
        return out

    '''Get function name'''
    name = getName(parent[1][1])

    '''Get function body'''
    functionBody = scope[name][1]

    '''Get function paramaters'''
    functionCallParams = callFunction(parent[3][0], parent[3], scope)

    '''Get total number of paramaters needed for function'''
    numRequiredParams = len(scope[name][0])

    '''Raise exception if invalid # of params'''
    if len(functionCallParams) != numRequiredParams:
        raiseException("Incorrect number of function paramaters")

    '''Get indexed number'''
    indexNumber = callFunction(parent[5][0], parent[5], scope)

    '''Creat New Scope'''
    newScope = {}

    '''Find number of required variables'''
    numVariables = 0
    for i, item in enumerate(scope[name][0]):
        variable = functionCallParams[i]
        newScope[scope[name][0][i]] = variable
        numVariables += 1
    newScope[name] = scope[name]
    nestedReturnValues = callFunction(newScope[name][1][0], newScope[name][1], newScope)
    output = unNestList(nestedReturnValues, [])[indexNumber]
    if not isinstance(output, list):
        finalOutput = []
        for i in range(numVariables):
            finalOutput.append(output)
        return finalOutput
    return output


def FunctionCall1(parent, scope):
    name = getName(parent[1][1])
    functionBody = scope[name][1]
    functionCallParams = callFunction(parent[3][0], parent[3], scope)
    if scope[name][0] == None:
        numRequiredParams = 0
    else:
        numRequiredParams = len(scope[name][0])
    if len(functionCallParams) != numRequiredParams:
        raiseException("Incorrect number of function paramaters")
    newScope = {}
    if scope[name][0] != None:
        for i, item in enumerate(scope[name][0]):
            variable = functionCallParams[i]
            newScope[scope[name][0][i]] = variable
    newScope[name] = scope[name]
    return callFunction(newScope[name][1][0], newScope[name][1], newScope)

# <FunctionCallParams> -> RPAREN | <ParameterList> RPAREN
def FunctionCallParams0(parent, scope):
    return []

def FunctionCallParams1(parent, scope):
    '''This function converts a nested list of paramaters
    to a single-depth list of function paramaters
    '''
    def unNestList(paramList, out):
        if len(paramList) > 1:
            for item in paramList:
                if not isinstance(item, list):
                    out.append(item)
                else:
                    unNestList(item, out)
        return out

    params = callFunction(parent[1][0], parent[1], scope)
    if isinstance(params, list):
        params = unNestList(params, [])
        return params
    return [params]

# <SubExpression> -> LPAREN <Expression> RPAREN
def SubExpression(parent, scope):
    return callFunction(parent[2][0], parent[2], scope)

# <Value> -> <Name> | <Number>
def Value0(parent, scope):
    value = callFunction(parent[1][0], parent[1], scope)
    if value[0] == None:
        errorMessage = "Undefined variable " + "'" + value[1] + "'"
        raiseException(errorMessage)
    return value[0]


def Value1(parent, scope):
    return callFunction(parent[1][0], parent[1], scope)


# <Name> -> IDENT | SUB IDENT | ADD IDENT
def Name0(parent, scope):
    name = getName(parent[1])
    return [lookupInScopeStack(name, scope), name]


def Name1(parent, scope):
    operator = parent[1]
    name = getName(parent[2])
    if operator == "SUB":
        return [-lookupInScopeStack(name, scope), name]
    if operator == "ADD":
        return [lookupInScopeStack(name, scope), name]

# <Number> -> NUMBER | SUB NUMBER | ADD NUMBER
def Number0(parent, scope):
    return getNumber(parent[1])


def Number1(parent, scope):
    token = parent[1]
    if token == "SUB":
        return -getNumber(parent[2])
    else:
        return getNumber(parent[2])


def ReadInput():
    global outputFinal
    parserInput = sys.stdin.read()
    parseTree = json.loads(parserInput)

    # use empty scope, as we are starting globally under Program
    callFunction(parseTree[0], parseTree, {})

if __name__ == '__main__':
    ReadInput()
