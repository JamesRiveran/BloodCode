import re
from BloodCodeCompiler.lexer.lexer import Lexer
from BloodCodeCompiler.parser.parser import Parser


def main():
    code = '''
    {
    Hunter c: Eileen;
    c => "Hola mundo";
    Hunter a, b: maria => 10;
    Insight (b == 10){
        a =>20;
    }
    }
    '''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    try:
        ast = parser.parse()
        print(ast)
    except Exception as e:
        print(f"Error: {e}")

    print(code)
if __name__ == "__main__":
    main()
 