import re
from BloodCodeCompiler.lexer.lexer import Lexer
from BloodCodeCompiler.parser.parser import Parser
from BloodCodeCompiler.interpreter.interpreter import Interpreter

def main():
    code = '''
    HuntersDream {
        Hunter x: Blood => 8 + (15 / (3 + 2) - 4 * 2) * (6 + 8 / (3 - 1)) - 7 * (9 - 5 / (8 - 6));
        Pray(x); 
    }

    '''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    print("Código fuente:")
    print(code)
    
    try:
        ast = parser.parse()
        #print("AST:", ast)
        
        # Ejecutar el AST con el intérprete
        interpreter = Interpreter()
        interpreter.execute(ast)
        print("Contexto:", interpreter.context)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
