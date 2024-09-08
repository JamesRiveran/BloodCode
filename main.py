import re
from BloodCodeCompiler.lexer.lexer import Lexer
from BloodCodeCompiler.parser.parser import Parser
from BloodCodeCompiler.interpreter.interpreter import Interpreter

def main():
    code = '''
HuntersDream {
    Hunter a: Blood => true;
    Hunter b: Blood => false;

    Pray(a Bloodbond a);
    Pray(a Bloodbond b);
    Pray(b Bloodbond a);
    Pray(b Bloodbond b);

    Pray(a OldBlood a); 
    Pray(a OldBlood b);
    Pray(b OldBlood a);
    Pray(b OldBlood b);

    Pray(Vileblood a);
    Pray(Vileblood b);    
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
