import re
from BloodCodeCompiler.lexer.lexer import Lexer
from BloodCodeCompiler.parser.parser import Parser
from BloodCodeCompiler.interpreter.interpreter import Interpreter

def main():
    code = '''
{
    Hunter a, b: maria => 11;
    a => "Hello, world!";
    Insight (Vileblood(b != 10)) {
        Pray ("B es igual a 10");
    } Madness {
        Pray ("B no es igual a 10");
    }
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
