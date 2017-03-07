import sys
import pprint
import json
import pprint

pp = pprint.PrettyPrinter(indent=1, depth=100)

def getName(token):
    '''Returns the string lexeme associated with an IDENT token, tok.
    '''
    colon_index = token.find(":")
    return token[colon_index+1:]


def getNumber(token):
    '''Returns the float lexeme associated with an NUMBER token, tok.
    '''
    colon_index = token.find(":")
    return float(token[colon_index+1:])

def raiseException(exception):
    raise Exception(exception)


def callFunction(*args):
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
    callFunction(parent[1][0], parent[1], scope)


def Statement1(parent, scope):
    callFunction(parent[1][0], parent[1], scope)


def Statement2(parent, scope):
    callFunction(parent[1][0], parent[1], scope)

# <FunctionDeclaration> -> FUNCTION <Name> LPAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
def FunctionDeclaration(parent, scope):
    '''
    1. Get function name.
    2. Get names of parameters.
    3. Get reference to function body subtree.
    4. In scope, bind the function's name to the following list:
        "foo": [['p1', 'p2', 'p3'], [FunctionBodySubtree]]
        where foo is the function names, p1, p2, p2 are the parameters and
        FunctionBodySubtree represents the partial parse tree that holds the
        FunctionBody0 expansion. This would correspond to the following code:
        function foo(p1, p2, p3) { [the function body] }
    #Bonus: check for return value length at declaration time
    '''

# <FunctionParams> -> RPAREN | <NameList> RPAREN
def FunctionParams0(parent, scope):
    pass


def FunctionParams1(parent, scope):
    pass

# <FunctionBody> -> <Return> | <Program> <Return>
def FunctionBody0(parent, scope):
    callFunction(parent[1][0], parent[1], scope)


def FunctionBody1(parent, scope):
    callFunction(parent[1][0], parent[1], scope)
    callFunction(parent[2][0], parent[2], scope)

# <Return> -> RETURN <ParameterList>
def Return(parent, scope):
    pass

# <Assignment> -> <SingleAssignment> | <MultipleAssignment>
def Assignment0(parent, scope):
    callFunction(parent[1][0], parent[1], scope)


def Assignment1(parent, scope):
    callFunction(parent[1][0], parent[1], scope)

# <SingleAssignment> -> VAR <Name> ASSIGN <Expression>
def SingleAssignment(parent, scope):
    pass

# <MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
def MultipleAssignment(parent, scope):
    pass

# <Print> -> PRINT <Expression>
def Print(parent, scope):
    pass

# <NameList> -> <Name> COMMA <NameList> | <Name>
def NameList0(parent, scope):
    pass


def NameList1(parent, scope):
    callFunction(parent[1][0], parent[1], scope)

# <ParameterList> -> <Parameter> COMMA <ParameterList> | <Parameter>
def ParameterList0(parent, scope):
    pass


def ParameterList1(parent, scope):
    callFunction(parent[1][0], parent[1], scope)

# <Parameter> -> <Expression> | <Name>
def Parameter0(parent, scope):
    callFunction(parent[1][0], parent[1], scope)


def Parameter1(parent, scope):
    callFunction(parent[1][0], parent[1], scope)

# <Expression> -> <Term> ADD <Expression> | <Term> SUB <Expression> | <Term>
def Expression0(parent, scope):
    pass


def Expression1(parent, scope):
    pass

# <Term> -> <Factor> MULT <Term> | <Factor> DIV <Term> | <Factor>
def Term0(parent, scope):
    pass


def Term1(parent, scope):
    pass

# <Factor> -> <SubExpression> EXP <Factor> | <SubExpression> | <FunctionCall> | <Value> EXP <Factor> | <Value>
def Factor0(parent, scope):
    pass


def Factor1(parent, scope):
    pass


def Factor2(parent, scope):
    pass


def Factor3(parent, scope):
    pass


def Factor4(parent, scope):
    pass

# <FunctionCall> ->  <Name> LPAREN <FunctionCallParams> COLON <Number> | <Name> LPAREN <FunctionCallParams>
def FunctionCall0(parent, scope):
    pass


def FunctionCall1(parent, scope):
    pass

# <FunctionCallParams> ->  <ParameterList> RPAREN | RPAREN
def FunctionCallParams0(parent, scope):
    pass


def FunctionCallParams1(parent, scope):
    pass

# <SubExpression> -> LPAREN <Expression> RPAREN
def SubExpression(parent, scope):
    pass

# <Value> -> <Name> | <Number>
def Value0(parent, scope):
    callFunction(parent[1][0], parent[1], scope)


def Value1(parent, scope):
    callFunction(parent[1][0], parent[1], scope)

# <Name> -> IDENT | SUB IDENT | ADD IDENT
def Name0(parent, scope):
    pass


def Name1(parent, scope):
    pass

# <Number> -> NUMBER | SUB NUMBER | ADD NUMBER
def Number0(parent, scope):
    pass


def Number1(parent, scope):
    pass


def ReadInput():
    global outputFinal
    parserInput = sys.stdin.read()

    parseTree = json.loads(parserInput)
    pp.pprint(parseTree)

    # use None as scope, as we are starting globally under Program
    callFunction(parseTree[0], parseTree, None)

if __name__ == '__main__':
    ReadInput()
