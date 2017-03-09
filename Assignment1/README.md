# Quirk Interpreter: How Mine Works

Skip to the bottom to see how to run my interpreter

## Step 1: The Lexer (lexer.py)

This part is pretty straightforward. This python script reads the input from the quirk file. It converts lines of strings into tokens until it reaches the end of the file. The output of the lexer is a stream tokens, each usable by the grammar for the parse tree. Input that is not recognizeds by the tokenizer (%, &, #, etc.) will be ingored if it is isolated in its own line in the code. However, if invalid characters are found while being parsed, the appropriate error will be returned.


## Step 2: The Parser (parser.py)

The parser is much more complex. It is built from recursive functions, each of which step through the grammar one possible valid chunk at a time, until either a valid path is found or it finds no path. Our start node, "Program" is where every quirk program begins. From that point on, it makes its way down the recursive tree. If the grammar is valid when the program reaches the EOF token, our program has valid syntax! We output an AST, and use this for the interpreter. We still don't get anything valuable from it, but we know that we now can intrepret this quirk file, and see what our program has accomplished.


## Step 3: The Interpreter (interpreter.py)

For the interpreter, all of the information we need to know is in the AST that was given to us by the parser. It tells us where to go, when to do it, and what information we need. If the AST is correct, the interpreter should be able to traverse the tree to return and output the information at the correct time. The big thing to watch for in the interpreter is the scope. Although quirk is a simple language, it still upholds the properties of global and local scope, the norm found in most programming languages today.

## Changes I Made to the Grammar:

Quirk Grammar Tree as displayed on class repo:


<Program> -> <Statement> <Program> | <Statement>
<Statement> -> <FunctionDeclaration> | <Assignment> | <Print>
<FunctionDeclaration> -> FUNCTION <Name> LPAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
<FunctionParams> -> <NameList> RPAREN | RPAREN
<FunctionBody> -> <Program> <Return> | <Return>
<Return> -> RETURN <ParameterList>
<Assignment> -> <SingleAssignment> | <MultipleAssignment>
<SingleAssignment> -> VAR <Name> ASSIGN <Expression>
<MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
<Print> -> PRINT <Expression>
<NameList> -> <Name> COMMA <NameList> | <Name>
<ParameterList> -> <Parameter> COMMA <ParameterList> | <Parameter>
<Parameter> -> <Expression> | <Name>
<Expression> -> <Term> ADD <Expression> | <Term> SUB <Expression> | <Term>
<Term> -> <Factor> MULT <Term> | <Factor> DIV <Term> | <Factor>
<Factor> -> <SubExpression> EXP <Factor> | <SubExpression> | <FunctionCall> | <Value> EXP <Factor> | <Value>
<FunctionCall> ->  <Name> LPAREN <FunctionCallParams> COLON <Number> | <Name> LPAREN <FunctionCallParams>
<FunctionCallParams> ->  <ParameterList> RPAREN | RPAREN
<SubExpression> -> LPAREN <Expression> RPAREN
<Value> -> <Name> | <Number>
<Name> -> IDENT | SUB IDENT | ADD IDENT
<Number> -> NUMBER | SUB NUMBER | ADD NUMBER


Changes I made and why:

<FunctionParams> -> <NameList> RPAREN | RPAREN
to
<FunctionParams> -> RPAREN | <NameList> RPAREN

<FunctionBody> -> <Program> <Return> | <Return>
to
<FunctionBody> -> <Return> | <Program> <Return>

<FunctionCallParams> -> <ParameterList> RPAREN | RPAREN
to
<FunctionCallParams> -> RPAREN | <ParameterList> RPAREN

Both of these grammar trees follow similar patterns. Above, their second branch is short and simple, and should be checked first. In the case that they are checked first and returned False, there is little harm done, as checking for a “RPAREN” token or a Return statement is shorter than checking for NameLists and Programs.

## Running my Interpreter:

Make sure all 4 files (lexer.py, parser.py, interpreter.py, and teresInterpreter.py) are in the same directory. I have everything wrapped into one file (teresInterpreter.py), which is a shortcut to pipe the files together.

All you have to do is type:

    python3 teresInterpreter.py
    
and it will do all the work for you. However, this has only been tested on my system, and results may be different depending on the system. If you would like to bypass this,

You can also type:

    python3 lexer.py < testFile.q | python3 parser.py | python3 interpreter.py
    
## Known issues

I tried to catch all of the possible errors and throw exceptions for them. However, some may have slipped through, and may see a totally useless error in your command line if you have a syntax error.

Specific code comments are found in the .py files, relative to the exact code it describes.

### My testFile.q ??
The reason the test quirk file in my repo has such bad, terrible, ugly formatting is because I wanted to show how quirk works similar to Java and C, completely ignoring pretty much everything except whitespace. It works properly formatter, too.
