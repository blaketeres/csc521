import os

if __name__ == '__main__':
    os.system("python3 lexer.py < testFile.q | python3 parser.py | python3 interpreter.py")
