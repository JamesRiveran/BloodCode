import re
from BloodCodeCompiler.lexer.lexer import Lexer
from BloodCodeCompiler.parser.parser import Parser
from BloodCodeCompiler.interpreter.interpreter import Interpreter

def main():
    code = '''
{
    Hunter abc: Maria[3];
    abc[0] => 5;
    abc[1] => 10;
    Pray(abc[1]);
}


    '''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    print(code)
    try:
        ast = parser.parse()
        print("AST:", ast)
        
        # Ejecutar el AST con el intérprete
        interpreter = Interpreter()
        interpreter.execute(ast)
        print("Contexto:", interpreter.context)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
