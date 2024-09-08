import re
from BloodCodeCompiler.lexer.lexer import Lexer
from BloodCodeCompiler.parser.parser import Parser
from BloodCodeCompiler.interpreter.interpreter import Interpreter
from BloodCodeCompiler.semantic_analyzer.SemanticAnalyzer import SemanticAnalyzer, SemanticError
from BloodCodeCompiler.semantic_analyzer.TypeEnviroment import TypeEnvironment


def main():
    code = '''
    HuntersDream {
        GreatOnes print_names(a:Eileen, b:Eileen):Rom {
            Pray(a);
        }
        Hunter x: Eileen => "Hola mundo";
        Pray(x); 
        print_names("Maria","Gehrman");
    }
    '''
    env = TypeEnvironment();
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    print("Código fuente:")
    print(code)
    
    try:
        ast = parser.parse()
        print("AST:", ast)
        analyzer = SemanticAnalyzer(env)
        analyzer.analyze(ast)
        interpreter = Interpreter(env)
        interpreter.execute(ast)
        print("Contexto:", interpreter.context)
    except SemanticError as e:
        print(e)  # Imprime solo el mensaje del error semántico sin la traza
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
