import re
from BloodCodeCompiler.lexer.lexer import Lexer
from BloodCodeCompiler.parser.parser import Parser
from BloodCodeCompiler.interpreter.interpreter import Interpreter
from BloodCodeCompiler.semantic_analyzer.SemanticAnalyzer import SemanticAnalyzer, SemanticError
from BloodCodeCompiler.semantic_analyzer.TypeEnviroment import TypeEnvironment


def main():
    code = '''
    {
        GreatOnes sum(a: Maria, num2:Maria): Maria {
            Pray("hello hunter");
        }
        GreatOnes hello(): Rom {
            Pray("hello hunter");
        }
        Hunter a: Maria => 5;
        Hunter b: Maria => 10;
        Eyes(b);
        Pray(b);
        Pray(a);
        Pray(sum(10,10));
        hello();
    }
    '''
    env = TypeEnvironment();
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
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
